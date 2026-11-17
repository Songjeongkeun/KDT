# [85일차] A2C와 n-step Return으로 배우는 동기식 Actor-Critic

A2C(Advantage Actor-Critic)는 여러 환경에서 모은 경험과 **Advantage**를 이용해 Actor와 Critic을 함께 학습하는 알고리즘이다. 에피소드가 끝날 때까지 기다리지 않고 일정한 길이의 경험을 모은 뒤, 관측한 보상과 미래 가치의 추정치를 결합해 갱신한다.

이번에는 CartPole 환경 4개에서 각각 5스텝씩 경험을 수집하는 A2C를 구현한다. n-step Return을 역순으로 계산하는 방법, 에피소드 경계 처리, 세 가지 손실의 역할과 실제 학습 그래프를 연결해 살펴본다.

> `5_A2C_A3C_PPO.ipynb`에 저장된 설명·코드·실행 결과를 기준으로 작성했다. 파일명과 달리 현재 노트북에는 **A2C까지만 구현**되어 있으며 A3C·PPO 설명과 구현은 없다. 82~84일차의 REINFORCE와 한 단계 Actor-Critic은 짧게 복습하고 새로 추가된 A2C 흐름을 중심으로 정리한다.
>
> 코드의 핵심 계산은 원본을 유지했다. 문서에서는 사용하지 않는 import를 제외하고 주석과 줄바꿈을 정리했으며, 장치 선택 부분에 `hasattr(torch, "xpu")` 확인을 추가했다. 원본 노트북은 수정하지 않았다. 학습 수치와 그래프는 재학습 결과가 아니라 **노트북에 저장된 결과**다.

---

## 1. REINFORCE에서 A2C로 이어지는 흐름

| 방식 | 학습에 사용하는 신호 | 경험을 모으는 단위 |
| --- | --- | --- |
| REINFORCE | 에피소드에서 관측한 실제 리턴 | 기본 형태에서는 에피소드 종료까지 |
| 한 단계 Actor-Critic | 즉시 보상과 다음 상태 가치로 만든 TD 목표 | 한 번의 상태 전이 |
| 이번 A2C | 여러 환경의 짧은 Rollout과 n-step 목표 | 환경 수 × Rollout 길이 |

Actor는 정책 $\pi(a\mid s)$를 학습하고 Critic은 상태 가치 $V(s)$를 학습한다. Critic은 실제 미래를 알고 있는 것이 아니라 **앞으로 받을 할인 누적 보상을 예측**한다.

```text
REINFORCE
에피소드 수집 -> 실제 리턴 계산 -> 정책 갱신

한 단계 Actor-Critic
한 번 이동 -> 보상 + 다음 가치 -> 정책·가치 갱신

이번 A2C
여러 환경에서 T번 이동 -> n-step 목표 계산 -> 경험을 합쳐 갱신
```

REINFORCE의 Monte Carlo 리턴은 변동성이 클 수 있고, Actor-Critic의 Bootstrap에는 가치 추정 오차가 들어간다. A2C도 가치 추정에 의존하므로 여러 환경을 사용한다는 이유만으로 학습 성공이 보장되지는 않는다.

이 문서의 $r_t$는 코드처럼 **시각 $t$에 행동한 뒤 받은 보상**을 뜻한다. 보상 첨자를 $r_{t+1}$로 쓰는 교재와는 표기만 다르다.

---

## 2. A2C의 핵심: 같은 정책으로 경험을 모아 함께 갱신한다

이번 구현의 설정은 다음과 같다.

```text
환경 수 N = 4
Rollout 길이 T = 5

환경 0: 경험 0 -> 경험 1 -> 경험 2 -> 경험 3 -> 경험 4
환경 1: 경험 0 -> 경험 1 -> 경험 2 -> 경험 3 -> 경험 4
환경 2: 경험 0 -> 경험 1 -> 경험 2 -> 경험 3 -> 경험 4
환경 3: 경험 0 -> 경험 1 -> 경험 2 -> 경험 3 -> 경험 4
                         |
                         v
                총 4 × 5 = 20개 전이
                         |
                         v
               하나의 손실로 신경망 갱신
```

각 환경에서 출발 상태와 진행 상황이 다르므로 하나의 환경만 연속해서 실행할 때보다 다양한 경험을 모을 수 있다. 다만 경험 사이의 상관관계가 완전히 없어지는 것은 아니다.

**동기식**이라는 말은 같은 정책으로 정해진 양의 경험을 모으고, 이를 합쳐 한 번 갱신한다는 뜻이다. 각 환경마다 서로 다른 신경망을 학습하는 구조가 아니다.

### 여러 환경과 실제 병렬 실행은 다르다

원본은 환경들을 Python 리스트에 저장하고 다음처럼 순서대로 실행한다.

```python
for i, env in enumerate(envs):
    ns, r, terminated, truncated, _ = env.step(int(actions[i].item()))
```

따라서 **상태와 정책 추론은 배치로 처리하지만 환경 실행은 순차적**이다. 별도의 멀티프로세스나 비동기 환경 실행을 구현한 코드는 아니다.

---

## 3. n-step Return과 Bootstrap

### 한 단계 TD 목표

종료되지 않은 상태에서 한 단계 TD 목표는 다음과 같다.

$$
G_t^{(1)}=r_t+\gamma V(s_{t+1}).
$$

한 번 관측한 보상 뒤의 미래는 Critic의 예측으로 대신한다.

### n-step Return

중간에 에피소드가 끝나지 않았을 때는 보상을 $n$개 관측한 뒤 그 이후의 미래 가치를 붙일 수 있다.

$$
G_t^{(n)}
=r_t+\gamma r_{t+1}+\cdots+\gamma^{n-1}r_{t+n-1}
+\gamma^nV(s_{t+n}).
$$

| 구성 | 의미 |
| --- | --- |
| 앞의 보상 항들 | 직접 관측한 보상 |
| $\gamma^nV(s_{t+n})$ | 아직 관측하지 않은 미래 보상의 추정치 |
| $n$ | 실제 보상을 포함하는 전이의 개수이며, 신경망 층 수가 아님 |

이처럼 **현재의 추정치를 학습 목표 일부로 사용하는 것**을 Bootstrapping이라고 한다.

```text
상태 s0 --보상 r0--> s1 --보상 r1--> s2 --보상 r2--> s3
        직접 관측        직접 관측        직접 관측      |
                                                       v
                                                미래 가치 V(s3)
```

관측 보상을 더 많이 사용하면 Critic에 의존하기 시작하는 시점이 뒤로 밀린다. 하지만 $n$이 커질수록 무조건 더 좋다는 뜻은 아니다. 관측 리턴의 변동과 Bootstrap 추정 오차 사이의 균형이 달라진다.

---

## 4. 숫자로 계산하는 3-step Return

노트북의 예제는 다음과 같다.

```text
r0 = 1, r1 = 1, r2 = 1
gamma = 0.9
V(s3) = 5
V(s0) = 4
```

세 번 행동하며 실제 받은 보상의 단순 합은 $1+1+1=3$이다. 하지만 학습 목표는 미래 추정치도 포함한다.

$$
\begin{aligned}
G_0^{(3)}
&=1+0.9\times1+0.9^2\times1+0.9^3\times5\\
&=1+0.9+0.81+3.645\\
&=6.355.
\end{aligned}
$$

현재 상태 가치 예측과 비교하면 다음과 같다.

$$
\widehat A_0=G_0^{(3)}-V(s_0)=6.355-4=2.355.
$$

**실제로 보상 6.355를 받았다는 뜻은 아니다.** 관측한 보상과 Critic의 미래 예측을 합쳐 만든 목표가 6.355라는 의미다.

### 역순 계산 코드

```python
gamma = 0.9
rewards = [1.0, 1.0, 1.0]
bootstrap_value = 5.0

running = bootstrap_value
for r in reversed(rewards):
    running = r + gamma * running

print("3-step return:", round(running, 3))
print("advantage:", round(running - 4.0, 3))
```

실행 결과:

```text
3-step return: 6.355
advantage: 2.355
```

| 역순 계산 | 계산 | 결과 |
| --- | --- | ---: |
| 마지막 보상 | $1+0.9\times5$ | 5.5 |
| 그 앞의 보상 | $1+0.9\times5.5$ | 5.95 |
| 첫 번째 보상 | $1+0.9\times5.95$ | 6.355 |

미래 쪽 결과를 먼저 구하면 그 앞의 목표를 반복해서 계산할 수 있다.

---

## 5. Advantage는 무엇을 비교하는가?

이론적인 Advantage와 이번 코드의 추정치는 다음처럼 구분한다.

$$
A^\pi(s,a)=Q^\pi(s,a)-V^\pi(s),
\qquad
\widehat A_t=G_t^{(n)}-V(s_t).
$$

| 추정 Advantage | 해석 | Actor의 갱신 신호 |
| --- | --- | --- |
| 양수 | 새로 만든 목표가 현재 예상보다 높음 | 선택한 행동의 확률을 높이는 방향 |
| 음수 | 새로 만든 목표가 현재 예상보다 낮음 | 선택한 행동의 확률을 낮추는 방향 |
| 0에 가까움 | 현재 예상과 목표가 비슷함 | 해당 표본의 신호가 작음 |

노트북의 점수 비유를 적용하면, 예상 70점에 목표 90점이면 $+20$, 목표 50점이면 $-20$이다. n-step 목표에는 Critic의 추정도 들어가므로 “실제 최종 성적”과 완전히 같은 개념은 아니다.

신경망은 여러 표본을 함께 사용하고 공통 특징층도 공유한다. 따라서 양수 표본 하나가 있다고 해당 행동의 확률이 매 갱신 후 반드시 증가한다고 단정하지는 않는다.

---

## 6. Actor·Critic·Entropy를 합친 손실

이번 코드의 전체 손실은 다음과 같다.

$$
L=L_{\text{actor}}+c_vL_{\text{critic}}-c_eH.
$$

$$
L_{\text{actor}}
=-\mathbb E\left[\log\pi(a_t\mid s_t)\,
\operatorname{stopgrad}(\widehat A_t)\right],
$$

$$
L_{\text{critic}}
=\mathbb E\left[\bigl(V(s_t)-G_t^{(n)}\bigr)^2\right],
\qquad
H=\mathbb E\left[H\bigl(\pi(\cdot\mid s_t)\bigr)\right].
$$

여기서 기대값 표기는 구현상 모은 표본들의 `.mean()`에 해당한다. Critic 목표 $G_t^{(n)}$는 이번 역전파에서 상수로 취급한다.

| 항목 | 역할 | 원본 기본값 |
| --- | --- | ---: |
| Actor 손실 | Advantage에 따라 행동 분포 조정 | 계수 1 |
| Critic 손실 | 현재 가치 예측을 목표에 가깝게 조정 | `value_coef=0.5` |
| Entropy 보너스 | 행동 분포가 너무 일찍 한쪽으로 치우치는 것을 억제 | `entropy_coef=0.01` |

### Entropy 앞에 마이너스가 붙는 이유

최적화기는 손실을 줄인다. 따라서 `-entropy_coef * entropy_bonus`는 다른 항이 같을 때 **Entropy가 커지는 방향**을 선호하게 만든다.

$$
H(\pi)=-\sum_a\pi(a\mid s)\log\pi(a\mid s).
$$

두 행동이 각각 50%이면 Entropy는 $\log2\approx0.693$이다. 한 행동으로 완전히 몰리면 0이다. 그렇다고 최종 목표가 계속 무작위로 행동하는 것은 아니다. 보상 개선과 탐색 유지를 함께 조정하는 항이다.

### `.detach()`는 어디에 사용하는가?

```python
advantage = target_t - value_t

actor_loss = -(logp_t * advantage.detach()).mean()
critic_loss = advantage.square().mean()
```

Actor에서는 Advantage를 고정된 평가 신호로 사용한다. Critic에서는 `value_t`를 미분해야 하므로 Advantage를 분리하지 않는다. 단, `target_t`는 앞에서 이미 분리되어 있다.

```text
Actor 손실 -> log_prob -> Actor 출력층 + 공통 특징층
Critic 손실 -> value   -> Critic 출력층 + 공통 특징층
```

`.detach()`가 두 신경망의 모든 파라미터를 완전히 독립시키는 것은 아니다. 공통 특징층은 두 손실의 영향을 함께 받는다.

---

## 7. 실행 준비와 장치 선택

이후 코드 블록은 이 절부터 순서대로 실행하는 구성을 따른다.

```python
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from torch import nn
from torch.distributions import Categorical
import gymnasium as gym

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
elif torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif hasattr(torch, "xpu") and torch.xpu.is_available():
    DEVICE = torch.device("xpu")
else:
    DEVICE = torch.device("cpu")

print(DEVICE)


def set_seed(seed=2026):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.backends.mps.is_available():
        torch.mps.manual_seed(seed)
```

노트북에 저장된 장치 출력:

```text
mps
```

CUDA, MPS, XPU 사용 가능 여부에 따라 선택되는 장치가 다르다. `mps`가 모든 컴퓨터에서 출력되는 것은 아니다. 시드를 고정해도 장치나 라이브러리 버전이 달라지면 장기 학습 결과까지 완전히 동일하다고 보장할 수는 없다.

노트북의 `time`, `math`, `copy`, `deque`, `F`, `Normal`은 현재 A2C 코드에서 사용하지 않으므로 위 import에서는 제외했다.

---

## 8. CartPole과 신경망의 입력·출력

CartPole은 카트를 움직여 막대가 쓰러지지 않도록 유지하는 환경이다. 이번 예제는 `CartPole-v1`의 기본 보상을 사용한다.

| 구분 | 내용 |
| --- | --- |
| 관측값 4개 | 카트 위치, 카트 속도, 막대 각도, 막대 각속도 |
| 행동 2개 | 0: 왼쪽으로 힘 적용, 1: 오른쪽으로 힘 적용 |
| 기본 보상 | 실행한 스텝마다 +1, 종료 스텝 포함 |
| 시간 제한 | 최대 500스텝 |

따라서 기본 보상에서 에피소드 점수는 유지한 스텝 수와 연결된다. 환경 세부 사항은 [Gymnasium CartPole 문서](https://gymnasium.farama.org/environments/classic_control/cart_pole/)에서 확인할 수 있다.

### 공통 특징층과 두 출력층

```python
class DiscreteActorCritic(nn.Module):
    def __init__(self, obs_dim=4, n_actions=2, hidden=128):
        super().__init__()
        self.body = nn.Sequential(
            nn.Linear(obs_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.actor = nn.Linear(hidden, n_actions)
        self.critic = nn.Linear(hidden, 1)

    def forward(self, states):
        features = self.body(states)
        logits = self.actor(features)
        values = self.critic(features).squeeze(-1)
        return logits, values
```

```text
상태 [N, 4]
    |
    v
Linear(4, 128) -> Tanh -> Linear(128, 128) -> Tanh
                                      |
                       +--------------+--------------+
                       |                             |
                       v                             v
              Actor: Linear(128, 2)         Critic: Linear(128, 1)
                       |                             |
                       v                             v
                 Logits [N, 2]               [N, 1] -> [N]
```

`.squeeze(-1)`은 마지막 크기 1인 차원만 제거한다. 배치가 1이어도 배치 차원까지 없애지 않기 위해 차원을 지정한다.

### Shape 확인

```python
net_test = DiscreteActorCritic().to(DEVICE)
logits, values = net_test(torch.zeros(4, 4, device=DEVICE))
print("logits:", logits.shape, "values:", values.shape)
```

노트북에 저장된 출력:

```text
logits: torch.Size([4, 2]) values: torch.Size([4])
```

상태 4개에 대해 행동 점수는 각각 2개, 상태 가치는 각각 1개다.

---

## 9. 서로 다른 환경 4개 만들기

```python
def make_envs(n=4, name="CartPole-v1", seed=2026):
    envs = [gym.make(name) for _ in range(n)]
    states = []

    for i, env in enumerate(envs):
        env.action_space.seed(seed + i)
        state, _ = env.reset(seed=seed + i)
        states.append(state)

    return envs, np.asanyarray(states, dtype=np.float32)
```

각 환경에는 `seed + i`를 사용한다. 초기 상태가 똑같은 환경을 여러 개 복제하는 대신 서로 다른 난수 흐름으로 경험을 수집한다.

| 반환값 | 내용 |
| --- | --- |
| `envs` | CartPole 환경 객체 4개를 가진 리스트 |
| `states` | 각 환경의 현재 상태를 모은 `(4, 4)` 배열 |

`action_space.seed()`는 행동 공간 자체의 난수 생성기에 적용된다. 이번 행동 선택은 `env.action_space.sample()`이 아니라 PyTorch의 `Categorical.sample()`로 하므로, 행동 선택 재현성에는 PyTorch 시드도 관여한다.

---

## 10. 한 번의 Rollout에서 모으는 값

Rollout은 현재 정책으로 환경을 실행하며 모으는 짧은 경험 묶음이다. 이번에는 다음 값을 시점별로 저장한다.

| 이름 | 저장하는 내용 | 한 시점의 Shape |
| --- | --- | --- |
| `logps` | 실제 선택한 행동의 로그 확률 | `[N]` |
| `vals` | 현재 상태의 가치 예측 | `[N]` |
| `rewards` | 환경에서 받은 즉시 보상 | `[N]` |
| `bootstraps` | 실제 종료를 반영한 다음 상태 가치 | `[N]` |
| `boundaries` | 실제 종료 또는 시간 제한에 따른 에피소드 경계 | `[N]` |
| `entropies` | 행동 분포의 Entropy | `[N]` |

### 행동 선택

```python
x = torch.as_tensor(states, dtype=torch.float32, device=DEVICE)
logits, value = model(x)
dist = Categorical(logits=logits)
actions = dist.sample()

logps.append(dist.log_prob(actions))
vals.append(value)
entropies.append(dist.entropy())
```

`Categorical(logits=logits)`는 정규화 전 점수로 이산 확률 분포를 만든다. 별도로 Softmax를 적용하지 않아도 된다. `sample()`은 행동 번호, `log_prob()`는 선택한 행동의 로그 확률을 반환한다. [PyTorch Categorical 문서](https://docs.pytorch.org/docs/stable/distributions.html#torch.distributions.categorical.Categorical)

`argmax()`로 가장 큰 행동만 고르는 코드와 달리, 현재 확률에 따라 다른 행동을 시도할 수 있다. 행동 추출 자체를 미분하는 것이 아니라 **선택된 행동의 로그 확률**을 통해 Actor를 학습한다.

---

## 11. `terminated`와 `truncated`를 따로 다루는 이유

환경은 다음과 같이 값을 반환한다.

```python
ns, r, terminated, truncated, _ = env.step(action)
boundary = bool(terminated or truncated)
```

| 경우 | 환경 리셋 | 다음 가치로 Bootstrap |
| --- | --- | --- |
| 종료되지 않음 | 하지 않음 | 사용 |
| `terminated=True` | 함 | 사용하지 않음 |
| `terminated=False`, `truncated=True` | 함 | 리셋 전 마지막 관측의 가치 사용 |

이 구분은 이번 코드의 목표 계산에서 중요하다. **리셋해야 한다는 사실**과 **미래 가치가 0이라는 판단**은 같지 않다. 외부 시간 제한으로 잘린 경우에는 마지막 상태 이후의 가치를 추정한다. 실제 종료 상태에서는 미래 가치를 붙이지 않는다. [Gymnasium 시간 제한 처리 문서](https://gymnasium.farama.org/tutorials/gymnasium_basics/handling_time_limits/)

### 리셋하기 전에 마지막 관측을 보존한다

```python
bs.append((ns, bool(terminated)))

if boundary:
    completed.append(float(episode_scores[i]))
    episode_scores[i] = 0.0
    ns, _ = env.reset()

next_states.append(ns)
```

```text
환경이 반환한 마지막 관측 ns
    |
    +-> bs에 보존 -> 이전 에피소드의 Bootstrap 계산
    |
    +-> 경계이면 reset() -> 새 관측을 다음 행동 입력으로 사용
```

시간 제한이 발생했는데 리셋된 새 에피소드의 초기 상태 가치를 이전 에피소드 목표에 붙이면 서로 다른 에피소드가 섞인다. 그래서 두 관측을 구분해서 저장한다.

### 실제 종료인 환경의 Bootstrap만 0으로 만든다

```python
with torch.no_grad():
    _, bootstrap_values = model(bootstrap_x)
    true_terminal = torch.tensor(
        [float(item[1]) for item in bs], device=DEVICE
    )
    bootstrap_values = bootstrap_values * (1.0 - true_terminal)
```

```text
다음 가치 예측:   [12, 8, 15, 20]
실제 종료 여부:  [ 0, 1,  0,  0]
최종 Bootstrap: [12, 0, 15, 20]
```

`torch.no_grad()`는 다음 가치를 이번 갱신의 고정 목표로 사용하기 위한 것이다.

---

## 12. 에피소드가 섞이지 않게 Return을 역순으로 계산하기

원본에서 중요한 부분은 다음 세 줄이다.

```python
running = torch.where(boundaries[t], bootstraps[t], running)
running = rewards[t] + gamma * running
targets[t] = running
```

`torch.where(조건, 참일 때 값, 거짓일 때 값)`는 환경별로 값을 선택한다.

| 현재 전이의 상태 | `running`으로 선택할 값 |
| --- | --- |
| 에피소드 경계가 아님 | 뒤에서 계산해 온 Return |
| 실제 종료 | 현재 전이의 Bootstrap 0 |
| 시간 제한 | 현재 전이의 리셋 전 마지막 상태 가치 |

### 경계를 무시하면 생기는 문제

```text
Rollout 시점:     t=0       t=1       t=2       t=3       t=4
에피소드:        <----- 에피소드 A ----->|<-- 에피소드 B -->
실제 종료:                            True
```

역순으로 계산하면 처음에는 B의 보상이 `running`에 들어 있다. A의 마지막 전이인 `t=2`를 만났을 때 이를 끊어 주지 않으면 B의 보상을 A가 받을 미래 보상처럼 더하게 된다.

원본은 `boundaries[t]`가 참이면 `running`을 그 전이의 Bootstrap으로 바꿔 이 연결을 끊는다.

### 숫자로 확인하기

설명을 위해 만든 경계 처리 예제다. 보상은 `[1, 1, 100]`이고, 두 번째 전이에서 실제 종료되어 마지막 100은 새 에피소드의 보상이라고 하자.

```python
rewards = [1.0, 1.0, 100.0]
boundaries = [False, True, False]
bootstraps = [0.0, 0.0, 0.0]
gamma = 0.9

running = bootstraps[-1]
targets = [None] * len(rewards)

for t in reversed(range(len(rewards))):
    if boundaries[t]:
        running = bootstraps[t]
    running = rewards[t] + gamma * running
    targets[t] = running

print([round(value, 3) for value in targets])
```

실행 결과:

```text
[1.9, 1.0, 100.0]
```

A의 첫 목표는 $1+0.9\times1=1.9$다. 새 에피소드의 보상 100은 들어가지 않는다. 두 번째 전이가 실제 종료가 아니라 시간 제한이고 마지막 가치가 5였다면 그 위치의 목표는 $1+0.9\times5=5.5$가 된다.

### 모든 표본이 5-step 목표를 쓰는 것은 아니다

경계 없는 5스텝 Rollout에서도 첫 표본은 보상 5개, 두 번째는 4개, 마지막은 1개와 Bootstrap을 사용한다.

```text
t=0: r0 + gamma*r1 + ... + gamma^4*r4 + gamma^5*V(s5)
t=1: r1 + gamma*r2 + ... + gamma^3*r4 + gamma^4*V(s5)
...
t=4: r4 + gamma*V(s5)
```

즉, `rollout_steps=5`는 한 번에 모으는 길이이며, **모든 표본에 항상 보상 5개를 넣는다는 뜻은 아니다.** 에피소드가 중간에 끝나면 해당 목표의 길이는 더 짧아진다.

---

## 13. A2C 학습 함수

앞에서 설명한 처리를 연결한 코드다. 원본과 같은 학습 흐름을 유지하고 긴 주석을 줄였다.

```python
def train_a2c(
    updates=300, n_envs=4, rollout_steps=5, seed=2026,
    gamma=0.99, lr=7e-4, value_coef=0.5,
    entropy_coef=0.01, print_every=50,
):
    set_seed(seed)
    envs, states = make_envs(n_envs, seed=seed)
    model = DiscreteActorCritic().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    episode_scores = np.zeros(n_envs, dtype=np.float64)
    completed = []
    history = []

    try:
        for update in range(1, updates + 1):
            logps, vals, rewards, bootstraps = [], [], [], []
            boundaries, entropies = [], []

            for t in range(rollout_steps):
                x = torch.as_tensor(
                    states, dtype=torch.float32, device=DEVICE
                )
                logits, value = model(x)
                dist = Categorical(logits=logits)
                actions = dist.sample()
                logps.append(dist.log_prob(actions))
                vals.append(value)
                entropies.append(dist.entropy())

                next_states, rs, bs, ends = [], [], [], []
                for i, env in enumerate(envs):
                    ns, r, terminated, truncated, _ = env.step(
                        int(actions[i].item())
                    )
                    episode_scores[i] += float(r)
                    boundary = bool(terminated or truncated)
                    rs.append(float(r))
                    ends.append(boundary)

                    # 리셋 전 관측과 실제 종료 여부를 보존한다.
                    bs.append((ns, bool(terminated)))
                    if boundary:
                        completed.append(float(episode_scores[i]))
                        episode_scores[i] = 0.0
                        ns, _ = env.reset()
                    next_states.append(ns)

                bootstrap_x = torch.as_tensor(
                    np.asanyarray(
                        [item[0] for item in bs], dtype=np.float32
                    ),
                    device=DEVICE,
                )
                with torch.no_grad():
                    _, bootstrap_values = model(bootstrap_x)
                    true_terminal = torch.tensor(
                        [float(item[1]) for item in bs], device=DEVICE
                    )
                    bootstrap_values = (
                        bootstrap_values * (1.0 - true_terminal)
                    )

                rewards.append(torch.tensor(
                    rs, dtype=torch.float32, device=DEVICE
                ))
                bootstraps.append(bootstrap_values)
                boundaries.append(torch.tensor(
                    ends, dtype=torch.bool, device=DEVICE
                ))
                states = np.asanyarray(next_states, dtype=np.float32)

            # 에피소드 경계를 반영하며 목표를 역순으로 계산한다.
            running = bootstraps[-1]
            targets = [None] * rollout_steps
            for t in reversed(range(rollout_steps)):
                running = torch.where(
                    boundaries[t], bootstraps[t], running
                )
                running = rewards[t] + gamma * running
                targets[t] = running

            target_t = torch.stack(targets).detach()
            value_t = torch.stack(vals)
            logp_t = torch.stack(logps)
            entropy_t = torch.stack(entropies)
            advantage = target_t - value_t

            actor_loss = -(logp_t * advantage.detach()).mean()
            critic_loss = advantage.square().mean()
            entropy_bonus = entropy_t.mean()
            loss = (
                actor_loss + value_coef * critic_loss
                - entropy_coef * entropy_bonus
            )

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 0.5)
            optimizer.step()

            recent = (
                float(np.mean(completed[-20:])) if completed else np.nan
            )
            history.append({
                "update": update,
                "episodes_done": len(completed),
                "recent20_reward": recent,
                "loss": float(loss.item()),
            })
            if update % print_every == 0:
                print(
                    f"A2C update {update:4d}/{updates} "
                    f"| 종료 에피소드 {len(completed):4d} "
                    f"| 최근20 평균 {recent:7.2f}"
                )
    finally:
        for env in envs:
            env.close()

    return model, pd.DataFrame(history), completed
```

### 학습률과 배치 설정

| 인자 | 기본값 | 역할 |
| --- | ---: | --- |
| `updates` | 300 | 신경망 갱신 횟수 |
| `n_envs` | 4 | 경험을 모으는 환경 수 |
| `rollout_steps` | 5 | 한 갱신 전 각 환경에서 실행할 전이 수 |
| `gamma` | 0.99 | 미래 보상의 할인율 |
| `lr` | 0.0007 | Adam 학습률 |
| `value_coef` | 0.5 | Critic 손실 비중 |
| `entropy_coef` | 0.01 | Entropy 보너스 비중 |
| `print_every` | 50 | 갱신 횟수 기준 로그 출력 간격 |

`n_envs`와 `rollout_steps`는 양의 정수라는 전제로 작성된 예제다. 이 함수는 기본 신경망과 CartPole의 차원에 맞춰져 있으므로 환경 이름만 다른 문제로 바꾼다고 입력·출력 차원이 자동 조정되지는 않는다.

---

## 14. Tensor Shape와 역전파 흐름

환경이 4개이고 Rollout 길이가 5이면 시점별 리스트를 `torch.stack()`으로 묶은 Shape는 다음과 같다.

| Tensor | Shape | 의미 |
| --- | --- | --- |
| 한 번의 상태 입력 | `[4, 4]` | 환경 4개 × 관측 4개 |
| 한 번의 Logits | `[4, 2]` | 환경 4개 × 행동 2개 |
| `target_t` | `[5, 4]` | 시점 5개 × 환경 4개의 목표 |
| `value_t` | `[5, 4]` | 각 시점·환경의 가치 예측 |
| `logp_t` | `[5, 4]` | 각 시점·환경에서 선택한 행동의 로그 확률 |
| `entropy_t` | `[5, 4]` | 각 행동 분포의 Entropy |
| `advantage` | `[5, 4]` | 목표와 가치 예측의 차이 |

`.mean()`은 20개 전이 전체에 대한 평균을 계산한다. 각 환경이 한 에피소드를 끝낼 때까지 기다리는 것은 아니다.

### Gradient Clipping

```python
optimizer.zero_grad()
loss.backward()
nn.utils.clip_grad_norm_(model.parameters(), 0.5)
optimizer.step()
```

`zero_grad()`는 이전 경사를 지우고, `backward()`는 이번 손실의 경사를 구한다. 그 뒤 전체 파라미터 경사의 Norm이 너무 크면 크기를 제한한 다음 가중치를 갱신한다.

여기의 `0.5`는 보상이나 손실 값을 0.5 이하로 자른다는 뜻이 아니다. Gradient Clipping도 학습의 안정적 수렴이나 성능 보장을 대신하지는 않는다.

이번 함수는 매 갱신마다 새 Rollout을 수집한다. 과거 경험을 오래 저장해 재사용하는 Replay Buffer나 타깃 신경망은 없다.

---

## 15. 실제 학습 실행과 환경 스텝 수

원본에서 실행한 호출은 다음과 같다.

```python
a2c_model, a2c_hist, a2c_scores = train_a2c(
    updates=3000,
    n_envs=4,
    rollout_steps=5,
    seed=2026,
    print_every=50,
)
```

함수 기본값은 `updates=300`이지만 실제 호출은 **3000회**다.

$$
\text{총 환경 전이 수}
=3000\times4\times5
=60{,}000.
$$

| 설정 | 환경 전이 수 |
| --- | ---: |
| 함수 기본값 300회 | 6,000 |
| 노트북의 실제 호출 3000회 | 60,000 |

원본의 함수 위 주석에 있는 6,000은 기본값 300회에 대한 계산이다. 저장된 3000회 학습 결과에 대해서는 60,000으로 읽어야 한다.

### 반환되는 값

| 이름 | 내용 |
| --- | --- |
| `a2c_model` | 모든 갱신을 마친 마지막 모델 |
| `a2c_hist` | 갱신별 번호, 종료 에피소드 수, 최근 보상 평균, 손실을 기록한 DataFrame |
| `a2c_scores` | 모든 환경에서 종료된 에피소드들의 총보상 리스트 |

중간 최고 성능 모델을 별도로 저장하는 코드가 없으므로 `a2c_model`이 최고 점수 시점의 모델이라는 보장은 없다.

---

## 16. 저장된 학습 결과 읽기

노트북의 전체 출력 중 대표적인 지점을 정리하면 다음과 같다.

| Update | 종료된 에피소드 수 | 최근 20개 에피소드 평균 보상 |
| ---: | ---: | ---: |
| 50 | 32 | 30.45 |
| 500 | 313 | 36.15 |
| 1000 | 511 | 60.05 |
| 1500 | 704 | 50.20 |
| 2000 | 864 | 86.05 |
| 2300 | 941 | 102.55 |
| 2500 | 958 | 191.55 |
| 2700 | 970 | 273.35 |
| 2800 | 975 | 318.50 |
| 2900 | 987 | 256.80 |
| 2950 | 1004 | 99.60 |
| 3000 | 1037 | 25.00 |

**이 값들은 학습 과정에서 수집한 결과다. 별도 평가 결과가 아니다.**

### `최근20 평균`의 정확한 의미

```python
recent = float(np.mean(completed[-20:])) if completed else np.nan
```

환경 4개에서 **가장 최근에 종료된 에피소드 최대 20개**의 보상을 평균한다. 최근 20번의 Update 평균이나 각 환경에서 20개씩 뽑은 평균이 아니다.

처음에 종료된 에피소드가 20개보다 적으면 그만큼만 평균한다. 아직 종료된 에피소드가 없으면 `NaN`이다. 새 에피소드가 끝나지 않은 Update에서는 같은 최근 평균이 반복 기록될 수 있다.

### 점수가 올랐다가 다시 떨어졌다

저장된 출력에서 2800회에는 최근 평균이 318.50이었지만 마지막 3000회에는 25.00으로 떨어졌다. 따라서 “학습이 안정적으로 완료되었다”거나 “CartPole을 해결했다”고 결론 내릴 수 없다.

학습률, 정책 분포의 변화, 가치 추정 오차, 탐색 등 여러 요인이 영향을 줄 수 있다. 하지만 현재 저장된 자료만으로 **급락 원인을 특정할 수는 없다.** Actor·Critic 손실, Entropy, 별도 평가 점수 등이 함께 기록되어 있지 않기 때문이다. `history`에 있는 것은 이 세 항을 합한 전체 손실이다.

또한 50회 간격의 출력에 나타난 수치만으로 전체 Update 중 정확한 최고점을 단정하지 않는다. 그래프에는 출력 간격 사이의 변화도 포함되어 있다.

---

## 17. 학습 그래프

노트북의 그래프 코드는 다음과 같다.

```python
plt.figure(figsize=(9, 3.5))
plt.plot(a2c_hist["update"], a2c_hist["recent20_reward"])
plt.xlabel("A2C update")
plt.ylabel("Recent 20 episode reward")
plt.title("A2C training progress (not evaluation)")
plt.grid(alpha=0.3)
plt.show()
```

아래 이미지는 원본 노트북에 저장된 `plt.show()` 출력이다. 새로 학습하거나 임의의 값으로 그린 그래프가 아니다.

![원본 노트북의 A2C 학습 보상 그래프](</Users/songjeong-geun/Desktop/데스크탑 - 송정근의 MacBook Air/데스크탑 /KDT/강의 정리/images/85일차/a2c-training-progress.png>)

| 구간 | 관찰되는 흐름 |
| --- | --- |
| 초반 | 비교적 낮은 보상에서 등락을 반복 |
| 중후반 | 최근 평균 보상이 점차 증가 |
| 2500회 이후 | 200~300 이상 구간으로 상승 |
| 마지막 구간 | 보상이 급격하게 하락 |

그래프의 가로축은 **에피소드 수가 아니라 Update 수**다. 세로축도 성공률이나 정확도가 아니라 최근 종료된 에피소드들의 평균 누적 보상이다.

마지막 모델을 고정한 평가 코드와 영상은 현재 노트북에 없다. 따라서 이 그래프만으로 새로운 초기 상태에서의 최종 성능을 판정하지 않는다.

---

## 18. 자주 헷갈리는 내용

| 질문 | 정리 |
| --- | --- |
| 환경 4개가 각각 다른 모델을 학습하는가? | 아니다. 하나의 공통 모델로 행동하고 경험을 합쳐 갱신한다. |
| 환경이 실제로 동시에 실행되는가? | 이 구현의 `env.step()`은 Python 반복문으로 순서대로 실행된다. |
| Update 3000은 3000에피소드인가? | 아니다. 신경망 갱신 3000회이며 종료된 에피소드는 저장 결과에서 총 1037개다. |
| 5스텝이면 모든 목표가 5-step인가? | 아니다. Rollout 내 위치와 경계에 따라 실제 목표 길이가 달라진다. |
| 시간 제한이 걸리면 미래 가치도 0인가? | 이번 구현은 실제 종료와 구분하고 리셋 전 관측으로 Bootstrap한다. |
| `no_grad()`는 모델을 평가 모드로 바꾸는가? | 아니다. 경사 추적을 끄는 것이며 `model.eval()`과는 다르다. |
| Entropy가 크면 보상도 반드시 큰가? | 아니다. 행동의 불확실성·분산 정도를 나타내는 별도 항이다. |
| 최근 평균이 한 번 높았으니 마지막 모델도 좋은가? | 아니다. 저장된 결과는 후반 급락을 보여 주며 최고 모델도 별도 보존하지 않는다. |
| A3C와 PPO도 구현되어 있는가? | 현재 제공된 노트북에는 없다. |

---

## 19. 핵심 정리

1. A2C는 같은 정책으로 여러 환경의 짧은 경험을 수집하고, 합쳐서 동기식으로 갱신한다.
2. n-step Return은 직접 관측한 보상과 Critic이 예측한 미래 가치를 결합한 학습 목표다.
3. Advantage는 이 목표가 현재 가치 예측보다 얼마나 좋은지 나타내는 추정 신호다.
4. 실제 종료, 외부 시간 제한, 새 에피소드의 시작을 구분해야 목표에 다른 에피소드의 보상이 섞이지 않는다.
5. Actor·Critic·Entropy 항은 서로 다른 역할을 하며 Gradient 경로를 구분해서 사용한다.
6. 저장된 학습 결과는 상승 후 급락했다. 학습 기록과 고정 정책의 평가 결과는 구분해야 한다.

> A2C의 구현에서 핵심은 환경을 여러 개 만드는 것만이 아니다. **경험을 어떤 길이로 모으고, 에피소드 경계에서 미래 가치를 어떻게 처리하며, 그 목표로 Actor와 Critic을 어떻게 갱신하는지** 이해하는 것이 중요하다.
