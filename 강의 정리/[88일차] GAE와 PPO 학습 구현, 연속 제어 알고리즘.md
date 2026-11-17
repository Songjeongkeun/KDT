# [88일차] GAE와 PPO 학습 구현, 연속 제어 알고리즘

87일차에서는 PPO의 확률 비율과 Clipping 목적함수를 숫자로 확인했다. 이번에는 그 계산을 실제 학습으로 연결한다. **GAE로 Advantage를 추정하고, 수집한 경험을 여러 번 나누어 학습하는 PPO 루프**를 살펴본다.

핵심은 두 가지다. 먼저 시간 순서가 있는 경험으로 학습 신호를 만든다. 그다음 그 신호와 수집 당시 정책 정보를 고정한 채, 데이터를 섞어 여러 번 정책을 갱신한다.

---

## 1. 이번에 새로 연결되는 학습 흐름

```text
현재 정책으로 512번 행동
          |
          v
상태·행동·보상·기존 로그 확률·가치·종료 정보 저장
          |
          v
시간 순서대로 연결된 TD 오차로 GAE 계산
          |
          +-> Actor에 줄 Advantage
          +-> Critic에 줄 목표 가치
          |
          v
Advantage 정규화
          |
          v
512개 경험을 섞어서 128개씩 나눔
          |
          v
PPO 손실로 5 Epoch 학습
          |
          v
다시 새로운 정책으로 512번 행동
```



---

## 2. GAE가 필요한 이유

GAE(**Generalized Advantage Estimation**)는 여러 시점의 TD 오차를 가중합해 Advantage를 추정한다.

한 번의 행동 결과만 보면 그 순간의 보상과 Critic 예측에 크게 의존한다. 반대로 에피소드 끝까지의 리턴을 사용하면 더 많은 실제 보상을 반영하지만, 실행마다 결과가 크게 달라질 수 있다.

| 방식 | 참고하는 정보 | 주의할 점 |
| --- | --- | --- |
| 한 단계 TD 기반 추정 | 현재 보상과 다음 상태 가치 | Critic의 오차가 추정에 영향을 줌 |
| Monte Carlo 기반 추정 | 에피소드 끝까지 실제로 받은 보상 | 긴 궤적과 확률적 결과에 따른 변동성이 커질 수 있음 |
| GAE | 현재와 이후의 TD 오차를 가중합 | $\lambda$로 추정의 길이를 조정 |

GAE는 가치 근사와 TD 오차의 누적 길이를 조절해 **편향·분산 사이의 균형**을 다룬다. 

---

## 3. GAE의 두 단계: TD 오차와 그 누적

### 첫 번째: 각 시점의 TD 오차

종료되지 않은 전이에 대해 TD 오차는 다음과 같다.

$$
\delta_t=r_t+\gamma V(s_{t+1})-V(s_t).
$$

| 항목 | 의미 |
| --- | --- |
| $r_t$ | 행동 후 관측한 보상 |
| $V(s_t)$ | 행동 전 상태에 대한 기존 가치 예측 |
| $r_t+\gamma V(s_{t+1})$ | 한 단계 경험으로 만든 새 가치 목표 |
| $\delta_t$ | 새 목표가 기존 예측보다 얼마나 높거나 낮은가 |



### 두 번째: 이후의 TD 오차까지 가중합

에피소드 경계가 없다고 할 때 다음과 같이 쓸 수 있다.

$$
\widehat A_t
=\delta_t+(\gamma\lambda)\delta_{t+1}
+(\gamma\lambda)^2\delta_{t+2}+\cdots.
$$

```text
현재 TD 오차
  + 다음 TD 오차 × gamma × lambda
  + 두 단계 뒤 TD 오차 × (gamma × lambda)^2
  + ...
```

GAE는 미래 **보상만** 그대로 더하는 식이 아니다. 현재 예측과 한 단계 목표의 차이인 **TD 오차들**을 누적한다.

---

## 4. 할인율 gamma와 GAE lambda의 역할



| 값 | 주된 역할 |
| --- | --- |
| $\gamma$ | 목표로 삼는 할인 리턴에서 미래 보상의 중요도 조정 |
| $\lambda$ | Advantage 추정에서 이후 TD 오차를 얼마나 길게 섞을지 조정 |

원본의 기본값은 $\gamma=0.99$, $\lambda=0.95$다. 이후 한 단계 TD 오차의 가중치는 $0.99\times0.95=0.9405$, 두 단계 뒤는 $0.9405^2$가 된다.

### lambda가 0이면

$$
\widehat A_t=\delta_t.
$$

현재 시점의 한 단계 TD 오차만 사용한다. 일반적으로 변동성을 줄이는 데 유리할 수 있지만 가치 추정 오차의 영향을 받는다.

### lambda가 1에 가까우면

더 먼 미래의 TD 오차를 반영한다. 실제 에피소드 끝까지 포함하고 종료 가치를 0으로 두는 경우, $\lambda=1$에서는 리턴에서 현재 가치를 뺀 형태로 연결된다.

---

## 5. 원본의 `compute_gae()`

다음 함수는 원본 계산을 유지하고 주석과 줄바꿈을 정리한 것이다.

```python
import numpy as np


def compute_gae(
    rewards, values, next_values, terminated, boundaries,
    gamma=0.99, gae_lambda=0.95,
):
    rewards = np.asanyarray(rewards, dtype=np.float32)
    values = np.asanyarray(values, dtype=np.float32)
    next_values = np.asanyarray(next_values, dtype=np.float32)
    terminated = np.asanyarray(terminated, dtype=np.float32)
    boundaries = np.asanyarray(boundaries, dtype=np.float32)

    advantages = np.zeros_like(rewards)
    gae = 0.0

    for t in reversed(range(len(rewards))):
        delta = (
            rewards[t]
            + gamma * (1.0 - terminated[t]) * next_values[t]
            - values[t]
        )
        gae = (
            delta
            + gamma * gae_lambda * (1.0 - boundaries[t]) * gae
        )
        advantages[t] = gae

    return advantages, advantages + values
```

이번 PPO에서는 인자 하나하나가 길이 512인 1차원 배열에 해당한다.

| 인자 | 내용 |
| --- | --- |
| `rewards[t]` | 해당 전이의 보상 |
| `values[t]` | 경험 수집 당시 현재 상태 가치 |
| `next_values[t]` | 리셋 전 다음 관측의 가치 |
| `terminated[t]` | 환경의 실제 종료 여부 |
| `boundaries[t]` | 실제 종료 또는 시간 제한으로 에피소드가 끊겼는가 |

`np.float32` 배열로 바꾸면 리스트로 수집한 값을 수치 계산에 사용할 수 있다. `np.zeros_like(rewards)`는 보상 배열과 같은 Shape의 저장 공간을 만든다.

---

## 6. 왜 역순으로 계산하는가?

GAE의 재귀식은 다음과 같다.

$$
\widehat A_t=\delta_t+\gamma\lambda\widehat A_{t+1}
$$

앞 시점의 Advantage를 계산하려면 뒤 시점의 누적 결과가 필요하다. 그래서 마지막부터 계산한다.

```text
t=2: A2 = delta2
t=1: A1 = delta1 + gamma*lambda*A2
t=0: A0 = delta0 + gamma*lambda*A1
```

마지막 시점에서 `gae=0`으로 시작하지만, 마지막 전이의 미래 가치를 무조건 0으로 처리하는 것은 아니다. **다음 상태의 가치는 이미 `delta` 안에 `next_values[t]`로 들어 있다.** 0으로 두는 것은 수집 구간 밖의 추가 TD 오차 누적분이다.

---

## 7. 숫자로 따라가는 GAE 계산

이 절은 원본 함수의 동작을 확인하기 위해 추가한 보충 예제다. 에피소드 경계가 없는 세 전이를 생각한다.

```text
보상:          [1, 1, 1]
현재 가치:     [2, 3, 4]
다음 상태 가치: [3, 4, 5]
gamma = 0.9
lambda = 0.8
```

TD 오차는 각각 다음과 같다.

$$
\delta_0=1+0.9\times3-2=1.7,
$$

$$
\delta_1=1+0.9\times4-3=1.6,
\qquad
\delta_2=1+0.9\times5-4=1.5.
$$

$\gamma\lambda=0.72$이므로 역순 계산은 다음과 같다.

| 시점 | 계산 | GAE |
| --- | --- | ---: |
| 2 | $1.5$ | 1.5 |
| 1 | $1.6+0.72\times1.5$ | 2.68 |
| 0 | $1.7+0.72\times2.68$ | 3.6296 |

```python
advantages, returns = compute_gae(
    rewards=[1, 1, 1],
    values=[2, 3, 4],
    next_values=[3, 4, 5],
    terminated=[False, False, False],
    boundaries=[False, False, False],
    gamma=0.9,
    gae_lambda=0.8,
)

print("Advantage:", [round(float(x), 4) for x in advantages])
print("Critic 목표:", [round(float(x), 4) for x in returns])
```

검증한 출력:

```text
Advantage: [3.6296, 2.68, 1.5]
Critic 목표: [5.6296, 5.68, 5.5]
```

### `returns = advantages + values`는 무엇인가?

Advantage가 목표와 현재 가치의 차이라면, 현재 가치를 다시 더해 Critic이 따라갈 목표를 만든다.

$$
\widehat R_t=\widehat A_t+V_{\mathrm{old}}(s_t).
$$

예를 들어 첫 목표는 $3.6296+2=5.6296$이다. 여기서 `returns`는 GAE로 만든 **가치 학습 목표**이며, 실제 에피소드의 단순 보상 합이나 항상 끝까지 관측한 Monte Carlo 리턴을 뜻하지 않는다.

| 사용처 | 학습 신호 |
| --- | --- |
| Actor | `advantages`를 정규화한 값 |
| Critic | 정규화하지 않은 `advantages + values` |

---

## 8. 두 종료 마스크는 서로 다른 연결을 끊는다

85일차에서 실제 종료와 시간 제한을 구분했다. 이번 GAE에서는 그 구분이 **서로 다른 두 위치**에 사용된다.

$$
\delta_t=r_t+\gamma(1-\mathrm{terminated}_t)V(s_{t+1})-V(s_t),
$$

$$
\widehat A_t=\delta_t+
\gamma\lambda(1-\mathrm{boundary}_t)\widehat A_{t+1}.
$$

| 마스크 | 끊는 대상 |
| --- | --- |
| `terminated` | 실제 종료 이후의 미래 가치 Bootstrap |
| `boundaries` | 다음 에피소드에서 나온 TD 오차의 누적 연결 |

### 실제 종료

미래 가치를 0으로 만들고, 다음 에피소드의 TD 오차도 더하지 않는다.

### 시간 제한

리셋 전 마지막 상태의 미래 가치는 사용할 수 있다. 그러나 그다음 배열 위치에는 새 에피소드의 경험이 들어올 수 있으므로 TD 오차의 연결은 끊어야 한다.

```text
이전 에피소드 -------->| 새 에피소드
                시간 제한
                    |
                    +-> 마지막 관측의 가치: 사용
                    +-> 새 에피소드 TD 오차: 연결하지 않음
```

### 경계를 무시하지 않는지 확인하는 예제

보상 `[1, 1, 100]` 중 마지막 100은 새 에피소드의 보상이라고 하자. 두 번째 전이는 시간 제한으로 끝났고 그 마지막 관측의 가치는 5다. 세 번째 전이는 실제 종료다.

```python
advantages, returns = compute_gae(
    rewards=[1, 1, 100],
    values=[0, 0, 0],
    next_values=[0, 5, 0],
    terminated=[False, False, True],
    boundaries=[False, True, True],
    gamma=0.9,
    gae_lambda=0.8,
)
print([round(float(x), 4) for x in advantages])
```

검증한 출력:

```text
[4.96, 5.5, 100.0]
```

두 번째 전이의 목표는 $1+0.9\times5=5.5$다. 새 에피소드의 TD 오차 100은 이전 에피소드로 전달되지 않는다. 첫 값은 $1+0.72\times5.5=4.96$이다.

---

## 9. PPO에서 수집 당시 정보를 보관하는 이유

원본은 하나의 CartPole 환경에서 512개 전이를 모은다. 그동안 정책을 갱신하지 않으므로 한 Rollout은 같은 정책 파라미터로 수집한다.

```python
with torch.no_grad():
    logits, value = model(x)
    dist = Categorical(logits=logits)
    action = dist.sample()
    old_logp = dist.log_prob(action)
```

| 저장값 | 필요한 이유 |
| --- | --- |
| `states` | 같은 관측을 새 정책에 다시 입력하기 위해 |
| `actions` | 실제 실행한 행동의 새 확률을 계산하기 위해 |
| `old_logps` | 경험 수집 당시 정책과 비교하기 위해 |
| `values`, `next_values` | 수집 당시 Critic으로 GAE와 목표를 만들기 위해 |
| `rewards` | 실제 환경 보상 반영 |
| `terminals`, `boundaries` | Bootstrap과 에피소드 간 연결을 각각 처리 |

상태는 복사해서 보관한다.

```python
states.append(state.copy())
```

환경이 관측 배열을 재사용하거나 수정하는 경우에도 저장한 과거 관측이 함께 바뀌지 않도록 하는 방식이다.

### 다음 가치 계산은 리셋 전에 한다

원본은 `env.step()`이 반환한 `ns`로 `nv`를 계산하고 저장한 다음, 종료된 경우에만 `env.reset()`을 호출한다. 따라서 시간 제한이 발생해도 GAE에 새 에피소드 초기 상태의 가치를 잘못 넣지 않는다.

---

## 10. 512개 전이는 512개 에피소드가 아니다

```text
Rollout 길이: 512번의 행동

에피소드 A --끝-- 에피소드 B --끝-- 에피소드 C -- ...
<--------------------- 512개 전이 --------------------->
```

짧은 에피소드는 한 Rollout에 여러 개 들어갈 수 있고, 긴 에피소드는 여러 Rollout에 걸쳐 이어질 수 있다.

`score`는 바깥 Update 반복문 이전에 초기화된다. 그래서 Rollout 끝에서 에피소드가 아직 진행 중이면 다음 Update에서도 그 에피소드의 누적 보상을 이어 간다.

```python
score += float(r)
if terminated or truncated:
    scores.append(score)
    score = 0.0
    state, _ = env.reset()
```

학습 마지막에 끝나지 않은 에피소드의 일부 보상은 `scores`에 완성된 에피소드 점수로 추가되지 않는다.

---

## 11. 시간 순서 계산을 마친 뒤 데이터를 섞는다

GAE 계산에는 다음 시점과 에피소드 경계의 순서가 중요하다. 따라서 먼저 원래 시간 순서로 GAE를 계산한다.

```python
advantages, returns = compute_gae(
    rewards, values, next_values, terminals, boundaries,
    gamma=gamma, gae_lambda=gae_lambda,
)
```

그다음 상태, 행동, 이전 로그 확률, 목표, Advantage를 Tensor로 바꾼다.

| Tensor | 기본 Shape |
| --- | --- |
| `x_all` | `[512, 4]` |
| `a_all` | `[512]` |
| `old_lp_all` | `[512]` |
| `ret_all` | `[512]` |
| `adv_all` | `[512]` |

이제 각 전이의 목표가 결정되었으므로 공통 인덱스로 함께 섞어 미니배치를 만들 수 있다. **GAE 계산 전에 전이 순서를 무작위로 섞는 것과는 다르다.**

---

## 12. Advantage 정규화와 Critic 목표는 구분한다

원본은 Rollout 전체의 Advantage를 정규화한다.

```python
adv_all = (
    (adv_all - adv_all.mean())
    / (adv_all.std(unbiased=False) + 1e-8)
)
```

평균을 빼고 표준편차로 나누어 학습 신호의 크기를 조절한다. `1e-8`은 표준편차가 0인 경우에도 분모가 0이 되지 않도록 더하는 작은 값이다.

`unbiased=False`는 이번 배치의 분산을 계산할 때 원소 수 $N$으로 나누는 설정이다. $N-1$로 나누는 추정과 구분한다.

### 정규화 후 부호의 의미

원래 Advantage가 `[2, 4, 6, 8]`처럼 모두 양수여도 평균을 빼면 작은 두 값은 음수가 된다. 정규화 후 부호는 **그 Rollout의 평균 Advantage보다 큰지 작은지**라는 의미도 포함한다.

따라서 정규화된 값이 음수라는 이유만으로 실제 환경 보상도 음수였다고 해석하면 안 된다. 원래 `목표 - 가치` 값과 정규화된 정책 가중치는 구분한다.

### Critic 목표를 정규화된 Advantage로 다시 만들지 않는다

원본은 정규화 이전에 `returns = advantages + values`를 계산하고 이를 `ret_all`에 보관한다. Actor에 사용할 `adv_all`만 정규화한다.

```text
원래 GAE + 수집 당시 가치 -> Critic 목표, 그대로 고정
원래 GAE -> 평균·표준편차 정규화 -> Actor 가중치
```

정규화된 Advantage를 현재 가치에 다시 더해 Critic 목표로 삼는 코드가 아니다.

---

## 13. 같은 경험을 5 Epoch 학습하기

```python
for epoch in range(epochs):
    perm = torch.randperm(len(states), device=DEVICE)
    for start in range(0, len(states), minibatch_size):
        ids = perm[start:start + minibatch_size]
        # 같은 ids로 상태·행동·이전 확률·목표를 선택한다.
```

기본 설정에서는 다음과 같다.

```text
Rollout 512개
    |
    +-> Epoch 1: 순서 섞기 -> 128개씩 4번 갱신
    +-> Epoch 2: 순서 섞기 -> 128개씩 4번 갱신
    +-> Epoch 3: 순서 섞기 -> 128개씩 4번 갱신
    +-> Epoch 4: 순서 섞기 -> 128개씩 4번 갱신
    +-> Epoch 5: 순서 섞기 -> 128개씩 4번 갱신
```

한 Rollout의 각 표본을 5번 사용한다. 이전 정책으로 수집한 데이터를 현재 정책과 비교하는 정보와 Clipping 목적함수가 함께 쓰인다.

그렇다고 오래전 경험을 무제한으로 섞어 재사용하는 Replay Buffer 방식은 아니다. 이번 구현은 현재 Rollout을 정해진 Epoch만큼 학습한 뒤 새 경험을 수집한다.

---

## 14. 로그 확률의 차이에 지수를 취하는 이유

87일차에서 확률 비율 자체는 다뤘다. 실제 코드에서는 저장한 로그 확률을 이용한다.

```python
new_lp = dist.log_prob(a_all[ids])
ratio = torch.exp(new_lp - old_lp_all[ids])
```

로그의 성질에 의해 다음과 같다.

$$
\exp\bigl(\log\pi_{\mathrm{new}}-\log\pi_{\mathrm{old}}\bigr)
=\exp\left(\log\frac{\pi_{\mathrm{new}}}{\pi_{\mathrm{old}}}\right)
=\frac{\pi_{\mathrm{new}}}{\pi_{\mathrm{old}}}.
$$

`new_lp`는 현재 모델로 계산하므로 미분된다. `old_lp_all`은 경험 수집 당시 로그 확률을 숫자로 저장한 것이므로 이번 갱신에서는 고정된 비교 기준이다.

### Epoch가 바뀌어도 이전 확률은 바꾸지 않는다

5 Epoch 동안 바뀌는 것은 현재 모델과 `new_lp`다. `old_lp_all`, GAE, Critic 목표는 같은 Rollout에서 계산한 값을 유지한다.

만약 매번 `old_lp_all`을 현재 모델로 덮어쓰면 경험을 수집한 정책과의 변화량이 아니라 매 순간 새 기준과 비교하게 된다. 원본은 그렇게 하지 않는다.

---

## 15. PPO 손실에서 미분되는 값과 고정되는 값

미니배치의 핵심 계산은 다음과 같다.

```python
logits, pred_values = model(x_all[ids])
dist = Categorical(logits=logits)
new_lp = dist.log_prob(a_all[ids])
ratio = torch.exp(new_lp - old_lp_all[ids])

surrogate1 = ratio * adv_all[ids]
surrogate2 = torch.clamp(
    ratio, 1 - clip_eps, 1 + clip_eps
) * adv_all[ids]

actor_loss = -torch.min(surrogate1, surrogate2).mean()
critic_loss = F.mse_loss(pred_values, ret_all[ids])
entropy = dist.entropy().mean()
loss = actor_loss + value_coef * critic_loss - entropy_coef * entropy
```

| 구분 | Tensor |
| --- | --- |
| 현재 신경망을 통해 미분 | 새 Logits, 새 로그 확률, `pred_values`, Entropy |
| 이번 갱신의 고정된 자료 | 행동 번호, 이전 로그 확률, GAE, Critic 목표 |

GAE와 목표는 NumPy에서 계산한 뒤 새 Tensor로 만들었으므로 현재 모델의 계산 그래프에 연결되지 않는다. Actor 손실에 별도의 `advantages.detach()`가 없어도 해당 자료를 통해 Critic으로 미분되는 구조가 아니다.

### 두 종류의 Clipping

| 코드 | 제한하는 것 |
| --- | --- |
| `torch.clamp(ratio, ...)` | PPO 목적함수의 비교 항에 사용하는 확률 비율 |
| `clip_grad_norm_(..., 0.5)` | 역전파로 얻은 파라미터 경사의 전체 Norm |

서로 다른 단계의 장치다. 어느 쪽도 환경 보상을 잘라내는 코드가 아니다. PPO의 비율 Clipping이 실제 정책 변화를 절대적으로 막는 것도 아니라는 점은 87일차 설명과 같다.

---

## 16. `train_ppo()` 전체 구현

이 함수는 원본과 같은 계산 순서를 유지하고 주석과 줄바꿈을 정리했다. 실행 전에 노트북 앞부분의 `DEVICE`, `set_seed()`, `DiscreteActorCritic` 정의와 이번 문서의 `compute_gae()`를 먼저 실행해야 한다. 이미 정리한 신경망 정의는 여기서 반복하지 않는다.

필요한 이름은 다음과 같다.

```python
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions import Categorical
import gymnasium as gym
```

```python
def train_ppo(
    total_updates=100, rollout_steps=512, seed=2026,
    gamma=0.99, gae_lambda=0.95, lr=3e-4,
    clip_eps=0.2, epochs=5, minibatch_size=128,
    value_coef=0.5, entropy_coef=0.01, print_every=10,
):
    set_seed(seed)
    env = gym.make("CartPole-v1")
    env.action_space.seed(seed)
    state, _ = env.reset(seed=seed)
    model = DiscreteActorCritic().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scores, history = [], []
    score = 0.0

    try:
        for update in range(1, total_updates + 1):
            states, actions, old_logps = [], [], []
            values, rewards, next_values = [], [], []
            terminals, boundaries = [], []

            # 현재 정책으로 경험을 수집한다.
            for _ in range(rollout_steps):
                x = torch.as_tensor(
                    state, dtype=torch.float32, device=DEVICE
                ).unsqueeze(0)
                with torch.no_grad():
                    logits, value = model(x)
                    dist = Categorical(logits=logits)
                    action = dist.sample()
                    old_logp = dist.log_prob(action)

                ns, r, terminated, truncated, _ = env.step(
                    int(action.item())
                )
                nx = torch.as_tensor(
                    ns, dtype=torch.float32, device=DEVICE
                ).unsqueeze(0)
                with torch.no_grad():
                    _, nv = model(nx)

                states.append(state.copy())
                actions.append(int(action.item()))
                old_logps.append(float(old_logp.item()))
                values.append(float(value.item()))
                rewards.append(float(r))
                next_values.append(float(nv.item()))
                terminals.append(bool(terminated))
                boundaries.append(bool(terminated or truncated))

                score += float(r)
                state = ns
                if terminated or truncated:
                    scores.append(score)
                    score = 0.0
                    state, _ = env.reset()

            advantages, returns = compute_gae(
                rewards, values, next_values, terminals, boundaries,
                gamma=gamma, gae_lambda=gae_lambda,
            )

            x_all = torch.tensor(
                np.asanyarray(states), dtype=torch.float32, device=DEVICE
            )
            a_all = torch.tensor(actions, dtype=torch.long, device=DEVICE)
            old_lp_all = torch.tensor(
                old_logps, dtype=torch.float32, device=DEVICE
            )
            ret_all = torch.tensor(
                returns, dtype=torch.float32, device=DEVICE
            )
            adv_all = torch.tensor(
                advantages, dtype=torch.float32, device=DEVICE
            )
            adv_all = (
                (adv_all - adv_all.mean())
                / (adv_all.std(unbiased=False) + 1e-8)
            )

            # 같은 Rollout을 여러 Epoch 갱신한다.
            for epoch in range(epochs):
                perm = torch.randperm(len(states), device=DEVICE)
                for start in range(0, len(states), minibatch_size):
                    ids = perm[start:start + minibatch_size]
                    logits, pred_values = model(x_all[ids])
                    dist = Categorical(logits=logits)
                    new_lp = dist.log_prob(a_all[ids])
                    ratio = torch.exp(new_lp - old_lp_all[ids])

                    surrogate1 = ratio * adv_all[ids]
                    surrogate2 = torch.clamp(
                        ratio, 1 - clip_eps, 1 + clip_eps
                    ) * adv_all[ids]
                    actor_loss = -torch.min(
                        surrogate1, surrogate2
                    ).mean()
                    critic_loss = F.mse_loss(pred_values, ret_all[ids])
                    entropy = dist.entropy().mean()
                    loss = (
                        actor_loss + value_coef * critic_loss
                        - entropy_coef * entropy
                    )

                    optimizer.zero_grad()
                    loss.backward()
                    nn.utils.clip_grad_norm_(model.parameters(), 0.5)
                    optimizer.step()

            recent = (
                float(np.mean(scores[-20:])) if scores else np.nan
            )
            history.append({
                "update": update,
                "episodes_done": len(scores),
                "recent20_reward": recent,
            })
            if update % print_every == 0:
                print(
                    f"PPO update {update:3d}/{total_updates} "
                    f"| episodes {len(scores):4d} "
                    f"| 최근20 평균 {recent:7.2f}"
                )
    finally:
        env.close()

    return model, pd.DataFrame(history), scores
```

위 함수는 양수의 Rollout 길이·미니배치 크기와 정해진 CartPole 차원을 전제로 한 실습 코드다. 다른 환경으로 이름만 바꿔도 모델의 입력·출력이 자동으로 달라지는 것은 아니다.

---

## 17. Update, Epoch, 미니배치의 횟수 계산

같은 “학습 횟수”라는 말로 세 개를 혼동하기 쉽다.

| 이름 | 이번 구현에서의 의미 | 기본값 |
| --- | --- | ---: |
| `total_updates` | 경험 수집과 반복 학습을 합친 바깥 주기 | 100 |
| `rollout_steps` | 한 바깥 주기에 새로 얻는 환경 전이 수 | 512 |
| `epochs` | 같은 Rollout을 반복해 학습하는 횟수 | 5 |
| `minibatch_size` | 한 번의 손실·역전파에 사용하는 전이 수 | 128 |

총 환경 행동 수는 다음과 같다.

$$
100\times512=51{,}200.
$$

한 Epoch의 미니배치는 $512/128=4$개다. 따라서 Optimizer 갱신 횟수는 다음과 같다.

$$
100\times5\times4=2{,}000.
$$

```text
바깥 PPO Update: 100회
환경 행동:       51,200회
optimizer.step:  2,000회
종료 에피소드:    실행 결과에 따라 달라짐
```

미니배치 크기로 나누어떨어지지 않는 설정이라면 마지막 작은 배치도 실행되므로 한 Epoch의 배치 수는 올림으로 계산해야 한다. 위 2000회는 제공된 기본 설정에 대한 정확한 값이다.

---

## 18. 원본에 저장된 PPO 학습 결과

실행한 호출은 다음과 같다.

```python
ppo_model, ppo_hist, ppo_scores = train_ppo(
    total_updates=100,
    rollout_steps=512,
    seed=2026,
    print_every=10,
)
```

노트북에 저장된 출력:

| PPO Update | 종료 에피소드 수 | 최근 최대 20개 에피소드 평균 보상 |
| ---: | ---: | ---: |
| 10 | 191 | 22.45 |
| 20 | 350 | 40.85 |
| 30 | 474 | 45.85 |
| 40 | 559 | 68.15 |
| 50 | 632 | 43.55 |
| 60 | 689 | 94.20 |
| 70 | 746 | 88.80 |
| 80 | 800 | 121.85 |
| 90 | 850 | 108.30 |
| 100 | 898 | 99.10 |

초반보다 평균 보상이 높아진 구간이 있지만 계속 상승하지는 않는다. 50번째 Update에는 이전보다 낮아졌고, 마지막 평균도 80번째보다 낮다.

이 수치는 `Categorical.sample()`로 행동하면서 모은 **학습 중 기록**이다. 모델을 고정한 별도 평가의 결과가 아니다. 100번째 Update와 100번째 에피소드를 혼동하지 않는다.

### 마지막 다섯 기록

`ppo_hist.tail()`에 저장된 값은 다음과 같다.

| Update | 종료 에피소드 수 | 최근 평균 보상 |
| ---: | ---: | ---: |
| 96 | 877 | 108.95 |
| 97 | 883 | 121.00 |
| 98 | 886 | 138.20 |
| 99 | 893 | 124.75 |
| 100 | 898 | 99.10 |

마지막 모델이 이번 학습 중 가장 좋았던 모델이라는 보장은 없다. 이 PPO 함수에는 최고 모델 체크포인트 저장이나 별도 평가가 없다.

### 결과를 해석할 때의 범위

- 최근 평균은 최근 20번의 Update가 아니라 **가장 최근에 종료된 에피소드 최대 20개**의 평균이다.
- 끝난 에피소드가 새로 추가되지 않으면 같은 최근 평균이 다음 Update에도 기록될 수 있다.
- 기본 CartPole 보상은 유지한 스텝 수와 연결되지만, 이 기록만으로 환경을 안정적으로 해결했다고 말할 수는 없다.
- A2C와는 환경 전이 수, 갱신 횟수, 계산 구성이 다르므로 마지막 평균 하나만 비교해 알고리즘의 우열을 단정하지 않는다.

---

## 19. 핵심 정리

1. GAE는 TD 오차를 역순으로 누적하고 $\lambda$로 미래 오차의 반영 길이를 조절한다.
2. 실제 종료 마스크와 에피소드 경계 마스크는 서로 다른 연결을 끊는다.
3. GAE와 Critic 목표를 시간 순서대로 계산한 뒤, 경험을 섞어 미니배치로 학습한다.
4. 이전 로그 확률과 목표는 고정하고 현재 모델의 확률·가치만 새로 계산한다.
5. 기본 설정은 51,200개 환경 전이와 2000번의 Optimizer 갱신을 수행한다.
6. 저장된 마지막 최근 평균 보상은 99.10이며, 별도 정책 평가나 최고 체크포인트 결과와 구분한다.
