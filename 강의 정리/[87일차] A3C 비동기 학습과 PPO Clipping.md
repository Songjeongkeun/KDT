# [87일차] A3C 비동기 학습과 PPO Clipping

A3C는 여러 Worker가 각자 환경을 실행하고 계산한 경사로 공유 모델을 갱신하는 Actor-Critic 방식이다. PPO는 행동 확률이 이전 정책에서 얼마나 변했는지 비교하고, 정책을 유리한 방향으로 과도하게 바꿔 얻는 추가 이득을 목적함수에서 제한한다.

이번에는 **A3C의 Global·Local Network, 공유 메모리와 프로세스 통신**, 그리고 **PPO의 확률 비율과 Clipping 계산**을 정리한다. A2C, n-step Return, Advantage, Actor·Critic 손실의 기본 원리는 85일차에서 다뤘으므로 반복 설명은 줄인다.

> 정리 범위는 `5_A2C_A3C_PPO.ipynb`의 A3C·PPO 부분과 `5_A3C예제.py`다. A3C는 실행 가능한 학습 코드까지 있지만, PPO는 개념과 목적함수의 숫자 계산까지이며 전체 학습 루프는 없다.
>
> 학습 통계는 같은 폴더에 있는 `a3c_scores.npy`를 읽어 계산했다. 해당 기록이 현재 코드와 같은 버전에서 만들어졌는지 확인할 실행 메타데이터는 없으므로, **이번에 재학습한 결과가 아니라 저장된 기록의 분석**으로 구분한다. 원본 코드·노트북·모델 파일은 변경하지 않았다.

---

## 1. A2C와 A3C의 차이

| 구분 | 85일차 A2C | 이번 A3C 예제 |
| --- | --- | --- |
| 경험 수집 | 여러 환경의 정해진 길이 경험을 모음 | 각 Worker가 자기 환경에서 수집 |
| 갱신 시점 | 모은 경험을 합쳐 한 번 갱신 | 각 Worker가 준비되면 공유 모델 갱신 |
| 신경망 | 함께 사용하는 정책·가치 모델 | 공유 Global Network와 Worker별 Local Network |
| 환경 실행 구현 | 환경 리스트를 순차적으로 `step()` | 프로세스를 나눠 실행 |
| Worker 사이 장벽 | 같은 갱신 단위로 경험을 모음 | 모든 Worker가 같은 시점까지 기다리지 않음 |

```text
A2C
환경 0: 경험 수집 ---+
환경 1: 경험 수집 ---+-> 합친 배치 -> 한 번 갱신
환경 2: 경험 수집 ---+

A3C
Worker 0: 경험 -> 경사 계산 -----> Global 갱신
Worker 1:    경험 -> 경사 계산 -------> Global 갱신
Worker 0:              경험 -> 경사 계산 -----> Global 갱신
```

비동기는 모든 Worker의 Rollout이 끝날 때까지 기다리는 공통 장벽이 없다는 뜻이다. **어떤 컴퓨터에서나 A2C보다 빠르다는 뜻은 아니다.** 프로세스 생성 비용, CPU 자원, 공유 모델 갱신의 경쟁 등에 영향을 받는다.

### 이번 예제는 잠금 없는 갱신이 아니다

원본의 `optimizer.step()`은 `with lock:` 안에 있다. 환경 실행과 Local 경사 계산은 병렬로 진행할 수 있지만, **Global 갱신은 한 번에 한 Worker만 수행**한다.

```text
Worker 0: 환경·경사 계산 -> [Lock 획득 -> Global 갱신 -> 해제]
Worker 1: 환경·경사 계산 ------> 기다림 -> [Global 갱신]
```

이 구조도 공통 Rollout 완료 장벽은 없으므로 비동기적인 Worker 진행을 사용한다. 다만 모든 공유 쓰기를 잠금 없이 동시에 수행하는 구현과는 구분해야 한다.

---

## 2. Global Network와 Local Network

### Global Network

모든 Worker가 함께 개선하는 모델이다. 학습이 끝난 뒤 최종 모델로 저장하는 대상도 Global Network다.

### Local Network

각 Worker가 상태를 입력하고 행동을 선택하며, 손실과 경사를 계산하는 복사본이다. Global 파라미터를 가져온 뒤 일정 길이의 경험을 수집한다.

```text
                     Global Network
                   공유 파라미터 저장
                    ^             ^
           Local 경사             Local 경사
                    |             |
              Local Net 0     Local Net 1
                    |             |
                 환경 0          환경 1
```

Local Network가 경험을 모으는 사이 다른 Worker가 Global을 갱신할 수 있다. 따라서 Local에서 계산한 경사는 적용 시점의 Global 파라미터보다 **조금 오래된 파라미터**에 기반할 수 있다.

Lock이 경사 계산 자체까지 막는 것은 아니므로 이러한 지연이 없어지는 것은 아니다. 이번 코드는 Global에 경사를 적용한 뒤 Local을 다시 Global 값으로 맞춘다.

---

## 3. A3C 예제의 전체 흐름

```text
main()
  |
  +-> Global Network와 SharedAdam 생성
  +-> 공유 메모리 설정
  +-> Lock과 Queue 생성
  +-> Worker 프로세스 2개 시작
  |
  +-> 각 Worker
  |     Global 파라미터 가져오기
  |       -> 최대 20스텝 경험 수집
  |       -> 목표·손실 계산
  |       -> Local에서 역전파
  |       -> Lock 안에서 Global 갱신
  |       -> Local 파라미터 동기화
  |       -> 에피소드 종료 시 Queue에 점수 전달
  |
  +-> 부모 프로세스
        점수 수집
          -> 400개 결과마다 모델 복사·평가
          -> 최고 평가 모델 저장
          -> Worker 종료 대기
          -> 기록·최종 모델 저장 및 통계 분석
```

신경망이 주고받는 것은 Q표가 아니라 파라미터와 경사다. 에피소드 점수는 학습과 별도로 부모 프로세스에 보고한다.

---

## 4. 실행 준비와 CPU 기반 구조

원본에서 사용하는 모듈은 다음과 같다.

```python
import torch.multiprocessing as mp
import random
from queue import Empty

import numpy as np
import torch
from torch import nn
from torch.distributions import Categorical
import gymnasium as gym
```

이번 예제에는 `.to("cuda")`나 `.to("mps")`가 없다. 모델과 Tensor를 **CPU에 두고 공유 메모리를 사용하는 구현**이다. 이전의 장치 선택 코드를 그대로 넣어 GPU·MPS에 옮기는 것은 이 예제의 실행 방식을 단순히 바꾸는 작업이 아니다.

`torch.multiprocessing`는 Python의 프로세스 실행 기능에 Tensor 공유 지원을 결합한다. 공유 메모리와 프로세스별 Gradient의 차이는 [PyTorch 멀티프로세싱 문서](https://docs.pytorch.org/docs/stable/notes/multiprocessing.html)에서 확인할 수 있다.

### 예제 파일로 실행하기

```bash
python3 "5_A3C예제.py"
```

프로세스가 새로 모듈을 불러오는 `spawn` 방식을 사용하므로 예제처럼 클래스와 Worker 함수를 파일의 최상위에 두고, 실행 시작점은 `__main__` 가드로 보호한다. 모듈을 바꾸는 것만으로 모든 직렬화 오류가 해결되는 것은 아니다.

---

## 5. 신경망 구조와 Shape

원본의 `Net`은 CartPole에 맞춰 입력 4개와 행동 2개를 사용한다.

```python
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.body = nn.Sequential(
            nn.Linear(4, 64),
            nn.ReLU(),
        )
        self.actor = nn.Linear(64, 2)
        self.critic = nn.Linear(64, 1)

    def forward(self, x):
        h = self.body(x)
        return self.actor(h), self.critic(h).squeeze(-1)
```

| 구분 | Shape |
| --- | --- |
| Worker가 전달하는 상태 하나 | `[4]` |
| Actor Logits | `[2]` |
| Critic 가치 | 스칼라 Tensor |
| 길이 T인 Rollout의 `values`를 Stack | `[T]` |
| `logps`, `targets`, `advantages` | `[T]` |

85일차 A2C는 시점마다 환경 여러 개를 배치로 입력했다. 이번 Worker는 **자기 환경의 상태 하나씩** 처리한다. `n_steps=20`은 신경망의 배치 환경 수가 아니라 한 Worker가 한 갱신 전 수집하는 최대 전이 수다.

---

## 6. 모델을 공유 메모리에 두기

```python
global_net = Net()
global_net.share_memory()
```

프로세스별로 Global이라는 이름의 완전히 독립된 파라미터를 갖는 것이 아니라, 같은 파라미터의 저장 공간을 참조하도록 준비한다.

반면 각 Worker 안에서 만드는 `local = Net()`은 독립된 계산용 모델이다.

```python
with lock:
    local.load_state_dict(global_net.state_dict())
```

이 코드는 **값을 복사해 맞추는 작업**이지 Local의 파라미터 저장 공간까지 Global과 공유시키는 코드가 아니다. Local은 자기 계산 그래프로 경사를 구한다.

---

## 7. SharedAdam이 필요한 이유

Adam은 파라미터뿐 아니라 과거 경사의 이동평균과 갱신 횟수 같은 내부 상태를 가진다. 이번 코드는 그 상태 Tensor도 공유하도록 `SharedAdam`을 정의한다.

```python
class SharedAdam(torch.optim.Adam):
    def __init__(self, params, lr=0.0003):
        super().__init__(params, lr=lr)
        for group in self.param_groups:
            for p in group["params"]:
                state = self.state[p]
                state["step"] = torch.zeros(
                    (), dtype=torch.float32
                ).share_memory_()
                state["exp_avg"] = torch.zeros_like(p).share_memory_()
                state["exp_avg_sq"] = torch.zeros_like(p).share_memory_()
```

| 상태 | 역할 |
| --- | --- |
| `step` | 해당 파라미터의 갱신 횟수 |
| `exp_avg` | 경사의 일차 모멘트 추정 |
| `exp_avg_sq` | 경사 제곱의 이동평균 추정 |

```text
공유 파라미터 + 공유 Adam 상태
              |
              v
어떤 Worker가 갱신해도 같은 최적화 이력을 이어서 사용
```

Optimizer 객체의 모든 Python 속성이 하나로 합쳐지는 것은 아니다. 이 구현은 필요한 **상태 Tensor의 저장 공간**을 공유하고, 접근은 Lock으로 제어한다.

또한 Adam 내부의 상태 이름을 직접 설정하는 예제이므로, 모든 Optimizer와 모든 설정에 그대로 적용되는 범용 클래스라고 보지는 않는다.

---

## 8. Worker의 초기화와 경험 수집

원본 Worker의 주요 설정은 다음과 같다.

```python
def worker(
    rank, global_net, optimizer, lock, queue,
    episodes=2000, gamma=0.99, n_steps=20,
):
    torch.manual_seed(100 + rank)
    random.seed(100 + rank)
    env = gym.make("CartPole-v1")
    local = Net()
    # 이후 에피소드와 Rollout 반복이 이어진다.
```

`rank`는 Worker를 구분하는 번호다. 이번에는 0과 1을 사용한다. 환경 초기화에는 `1000 + rank * 100 + ep`를 사용한다.

서로 다른 시드 설정을 사용하지만, 프로세스가 실행되고 Lock을 얻는 순서까지 고정한 것은 아니다. 동일한 시드로 다시 실행하더라도 비동기 학습 결과가 완전히 같다고 보장하기 어렵다.

### 최대 20스텝을 수집한다

```python
logps, values, rewards, entropies = [], [], [], []

for _ in range(n_steps):
    x = torch.tensor(obs, dtype=torch.float32)
    logits, v = local(x)
    dist = Categorical(logits=logits)
    a = dist.sample()

    nxt, r, terminated, truncated, _ = env.step(a.item())
    logps.append(dist.log_prob(a))
    values.append(v)
    entropies.append(dist.entropy())
    rewards.append(r)

    score += r
    obs = nxt
    done = terminated or truncated
    if done:
        break
```

20스텝 전에 에피소드가 끝나면 그 시점까지만 수집한다. 끝나지 않았다면 해당 경험으로 한 번 갱신하고 같은 에피소드를 계속 진행한다. 따라서 **한 에피소드 안에 여러 번의 Global 갱신**이 일어날 수 있다.

---

## 9. 목표와 손실 계산에서 이어지는 부분

n-step Return의 원리는 85일차와 같다. 새로 볼 부분은 **각 Worker가 자기 Rollout에 대해서 따로 계산한다는 것**이다.

```python
with torch.no_grad():
    bootstrap = (
        0.0 if terminated
        else local(torch.tensor(obs, dtype=torch.float32))[1].item()
    )

targets = []
R = bootstrap
for r in reversed(rewards):
    R = r + gamma * R
    targets.insert(0, R)
```

실제 종료에서는 Bootstrap을 0으로 두고, 시간 제한으로 잘렸다면 마지막 관측의 가치를 사용한다. 이번 Rollout은 에피소드 경계를 만나면 바로 끝내므로, 그 안에 다음 에피소드 보상이 섞이지 않는다.

노트북의 새 숫자 예시는 보상 `[1, 1, 1]`, Bootstrap 2, 할인율 0.9일 때 Return 4.168이다. 현재 가치가 3이면 추정 Advantage는 1.168이다. 출력의 `1.1680000000000001`은 부동소수점 표현 차이다.

### 손실의 기본 구조는 A2C와 같다

```python
targets = torch.tensor(targets, dtype=torch.float32)
values = torch.stack(values)
logps = torch.stack(logps)
advantages = targets - values

actor_loss = -(logps * advantages.detach()).mean()
critic_loss = advantages.square().mean()
entropy_bonus = torch.stack(entropies).mean()

loss = actor_loss + 0.5 * critic_loss - 0.01 * entropy_bonus
```

A3C의 핵심 차이는 손실식이 완전히 새로워졌다는 데 있지 않다. **이 손실을 계산하는 Worker가 여러 개이고, 그 경사를 공유 파라미터에 반영하는 방식**이 달라진다.

---

## 10. Local 경사를 Global로 전달하기

원본에서 가장 중요한 갱신 부분이다.

```python
local.zero_grad()
loss.backward()
torch.nn.utils.clip_grad_norm_(local.parameters(), 5)

with lock:
    optimizer.zero_grad()
    for gp, lp in zip(global_net.parameters(), local.parameters()):
        gp.grad = (
            lp.grad.detach().clone()
            if lp.grad is not None else None
        )

    optimizer.step()
    local.load_state_dict(global_net.state_dict())
```

| 단계 | 의미 |
| --- | --- |
| `local.zero_grad()` | 이전 Local 계산의 경사 제거 |
| `loss.backward()` | Local 모델에서 경사 계산 |
| Gradient Clipping | Local 경사의 전체 Norm 제한 |
| `optimizer.zero_grad()` | 이번 Global 갱신에 사용할 경사 초기화 |
| `gp.grad = ...` | Local에서 구한 경사를 Global 파라미터의 Gradient에 연결 |
| `optimizer.step()` | 공유 파라미터와 Adam 상태 갱신 |
| `load_state_dict()` | 갱신된 파라미터를 Local로 가져옴 |

파라미터 데이터가 공유된다는 이유만으로 Local의 `.grad`가 Global에 자동 전달되지는 않는다. 그래서 코드에 명시적인 경사 복사가 있다.

`.detach().clone()`은 Local 계산 그래프에서 분리된 경사 값의 복사본을 만든다. `optimizer.step()`은 이 값을 이용해 Global을 갱신한다. 이 예제에서는 Parent가 경사를 받아 학습하는 것이 아니라 **각 Worker가 Lock 안에서 직접 공유 Optimizer를 사용**한다.

---

## 11. `spawn`, Process, Lock, Queue

원본의 시작 설정과 Worker 생성 부분이다.

```python
mp.set_start_method("spawn", force=True)
torch.manual_seed(2026)
global_net = Net()
global_net.share_memory()

optimizer = SharedAdam(global_net.parameters(), lr=0.0003)
lock = mp.Lock()
queue = mp.Queue()

workers = [
    mp.Process(
        target=worker,
        args=(i, global_net, optimizer, lock, queue),
    )
    for i in range(2)
]

for p in workers:
    p.start()
```

| 도구 | 역할 |
| --- | --- |
| `spawn` | 새 Python 프로세스를 만들어 실행 |
| `Process` | Worker 함수를 별도 프로세스에서 실행 |
| `Lock` | 공유 파라미터의 복사·갱신 구간 보호 |
| `Queue` | Worker의 에피소드 완료 기록을 부모에게 전달 |

Worker는 에피소드가 끝날 때 다음 기록을 넣는다.

```python
queue.put((rank, ep + 1, score))
```

Queue에 넣는 것은 **보상 기록**이다. 이 코드에서 경사는 Queue로 전달하지 않는다.

### `__main__` 가드

```python
if __name__ == "__main__":
    main()
```

새 프로세스가 모듈을 불러올 때 `main()`을 다시 무조건 실행하지 않도록 한다. 프로세스 생성 코드가 가드 밖에 있으면 자식이 다시 자식을 생성하려는 문제가 생길 수 있다.

---

## 12. 4000개 결과와 4000번 갱신은 다르다

이번 설정은 Worker 2개가 각각 2000에피소드를 실행한다.

$$
2\times2000=4000\text{개의 에피소드 기록}.
$$

한 에피소드가 여러 Rollout으로 나뉠 수 있으므로 **Global 갱신 횟수가 4000이라는 뜻은 아니다.** 총 환경 스텝 수도 에피소드 길이에 따라 달라진다.

부모 프로세스는 다음과 같이 결과를 수집한다.

```python
records = []
for _ in range(4000):
    try:
        record = queue.get(timeout=180)
    except Empty:
        raise RuntimeError(
            "Worker 결과 대기 시간 초과. Worker 오류를 확인하세요."
        )
    records.append(record)
```

이 순서는 Worker 번호순이나 에피소드 번호순이 아니라 **Queue에서 받은 순서**다. 한 Worker의 10번째 기록 다음에 다른 Worker의 8번째 기록이 올 수 있다.

`timeout=180`은 180초 안에 다음 기록을 받지 못하면 예외를 내는 장치다. Worker의 모든 오류를 즉시 발견하거나 원인을 자동으로 분석하는 코드는 아니다.

---

## 13. 학습 중 모델을 복사해서 평가하기

부모는 결과를 400개 받을 때마다 Global을 복사해 10에피소드 평가한다.

```python
if len(records) % checkpoint_interval == 0:
    with lock:
        snapshot = Net()
        snapshot.load_state_dict(global_net.state_dict())

    mean_score = evaluate(snapshot, episodes=10)
```

잠금 안에서는 일관된 파라미터 복사만 수행한다. 평가 전체를 잠금 안에 넣지는 않으므로, 평가하는 동안에도 Worker의 학습이 진행될 수 있다.

따라서 `Collected 400`은 부모가 400개 결과를 받았다는 뜻이지, Global이 정확히 전체 400번째 에피소드의 마지막 갱신에 멈춰 있다는 뜻은 아니다.

### 최고 평가 모델 보관

```python
if mean_score > best_score:
    best_score = mean_score
    best_at = len(records)
    torch.save(snapshot.state_dict(), "a3c_best.pt")
```

여기서 “최고”는 **정기적으로 수행한 10에피소드 평가 평균이 가장 높은 복사본**이라는 뜻이다. 모든 순간의 모델을 평가한 것은 아니다.

이전 A2C에서는 최고 시점의 모델을 별도로 저장하지 않았다. 이번 예제는 마지막 모델의 성능이 중간보다 나빠질 가능성에 대비해 최고 평가 체크포인트도 보관한다.

---

## 14. 평가에서는 행동을 어떻게 고르는가?

원본 평가 함수의 핵심은 다음과 같다.

```python
@torch.no_grad()
def evaluate(net, episodes=10, seed=30000):
    env = gym.make("CartPole-v1")
    net.eval()
    scores = []
    try:
        for ep in range(episodes):
            obs, _ = env.reset(seed=seed + ep)
            done = False
            score = 0.0
            while not done:
                x = torch.tensor(obs, dtype=torch.float32)
                logits, _ = net(x)
                action = int(logits.argmax().item())
                obs, reward, terminated, truncated, _ = env.step(action)
                score += reward
                done = terminated or truncated
            scores.append(score)
    finally:
        env.close()
    return float(np.mean(scores))
```

| 구분 | 학습 | 평가 |
| --- | --- | --- |
| 행동 선택 | `Categorical.sample()` | 최대 Logit의 `argmax()` |
| 정책 | 확률적으로 행동 | 주어진 상태에서 결정적으로 행동 |
| 경사 계산 | 함 | `no_grad()`로 하지 않음 |
| 환경 초기화 시드 | Worker·에피소드에 따라 설정 | 30000부터 설정 |

`eval()`이 자동으로 `argmax()` 행동을 고르는 것은 아니다. 행동 선택은 코드의 `argmax()`가 결정하고, `eval()`과 `no_grad()`는 각각 모델 모드와 경사 추적을 제어한다.

마지막에는 최종 모델과 최고 체크포인트를 각각 30에피소드 평가한다. 다만 10회 평가와 30회 평가가 같은 시작 시드를 사용하므로 앞의 10개 시드가 겹친다. **완전히 새로운 독립 평가 집합**이라고 부르지는 않는다.

---

## 15. 저장되는 파일과 종료 처리

| 파일 | 내용 |
| --- | --- |
| `a3c_scores.npy` | `(Worker 번호, Worker의 에피소드 번호, 보상)` 기록 |
| `a3c_cartpole.pt` | 학습 종료 후 Global의 `state_dict` |
| `a3c_best.pt` | 정기 평가 평균이 가장 높았던 Snapshot의 `state_dict` |

이 이름들은 상대 경로이므로 실행한 터미널의 **현재 작업 폴더**에 저장된다. Python 파일이 있는 위치로 무조건 저장되는 것은 아니다.

`state_dict`만 저장하므로 Net 클래스 정의와 학습 설정을 전부 담은 완전한 재개 체크포인트는 아니다. 공유 Adam 상태, Worker 진행 상태, 난수 상태까지 저장한 것도 아니다.

### Worker 정리

```python
for p in workers:
    p.join(timeout=30)
for p in workers:
    if p.is_alive():
        p.terminate()
        p.join()
```

먼저 정상 종료를 기다리고, 남아 있는 프로세스는 강제로 종료한 뒤 회수한다. `finally`에 있어 결과 수집 중 예외가 나더라도 정리 과정을 시도한다.

이 설정에서는 Worker당 2000, Worker 수 2, 결과 수집 4000이 서로 맞춰져 있다. 에피소드 수나 Worker 수를 바꿀 때 이 숫자들을 따로 남겨 두면 결과를 덜 읽거나 계속 기다리는 문제가 생길 수 있다.

---

## 16. 저장된 4000개 학습 기록 분석

같은 폴더의 `a3c_scores.npy`를 확인한 결과 Shape은 `(4000, 3)`, 자료형은 `float64`였다. Worker별 에피소드 번호는 각각 1~2000까지 있었다.

첫 행들의 예시는 다음과 같다.

```text
Worker  Episode  Reward
   0       1      19
   1       1      40
   0       2      19
   1       2      34
   1       3      27
```

### Worker별로 분리한 뒤 에피소드 순서로 정렬한다

```python
import numpy as np

records = np.load("a3c_scores.npy", allow_pickle=False)

for rank in [0, 1]:
    data = records[records[:, 0] == rank]
    data = data[np.argsort(data[:, 1])]
    scores = data[:, 2]

    print(f"Worker {rank}")
    print("처음 100회 평균:", scores[:100].mean())
    print("중간 100회 평균:", scores[950:1050].mean())
    print("마지막 100회 평균:", scores[-100:].mean())
    print("최고 점수:", scores.max())
```

저장된 기록에서 계산한 결과:

| Worker | 처음 100회 평균 | 중간 100회 평균 | 마지막 100회 평균 | 최고 단일 점수 |
| --- | ---: | ---: | ---: | ---: |
| 0 | 24.46 | 110.83 | 114.08 | 500 |
| 1 | 25.56 | 97.02 | 115.80 | 500 |

`scores[950:1050]`은 0부터 시작하는 인덱스이므로 **951~1050번째 에피소드 100개**다.

두 Worker 모두 초반보다 마지막 100회 평균이 높았다. 하지만 최고 한 번의 500점이 모든 평가에서 500점을 유지한다는 뜻은 아니다. 중간에 하락한 구간도 있어 안정적으로 최고 성능에 수렴했다고 단정하지 않는다.

### 마지막 10개 기록의 평균

원본의 다음 코드는 Queue 수집 순서의 마지막 10개를 평균한다.

```python
np.mean([x[2] for x in records[-10:]])
```

해당 저장 파일에서 값은 **133.6**이다. 이것은 각 Worker의 마지막 10회 평균도 아니고, `evaluate()`로 측정한 최종 모델 점수도 아니다.

이번 정리에서는 새 학습을 수행하거나 `.pt` 체크포인트를 재평가하지 않았다. 최고 체크포인트의 실제 평가 평균과 선택 시점을 이 기록만으로 복원할 수는 없어 숫자를 임의로 덧붙이지 않는다.

---

## 17. PPO가 다루려는 문제

이제 노트북의 PPO 부분으로 넘어간다. PPO는 **Proximal Policy Optimization**의 약자다. 이번 자료에서 설명하는 것은 Clipping 목적함수를 사용하는 PPO-Clip이다.

정책을 갱신하면서 행동 확률이 너무 크게 달라지면, 이전 정책으로 수집한 경험을 바탕으로 새 정책을 개선하는 과정이 불안정해질 수 있다.

```text
경험 수집 당시: 오른쪽 확률 40%
큰 갱신 이후:  오른쪽 확률 95%
```

PPO-Clip은 정책 변화에 따른 추가 이득을 목적함수에서 제한해 과도한 변화를 억제하려 한다. **파라미터나 실제 행동 확률에 절대적인 변경 한도를 강제하는 코드는 아니다.** 이 차이는 [PPO 공식 설명](https://spinningup.openai.com/en/latest/algorithms/ppo.html)에서도 강조한다.

제공된 노트북에는 이 원리와 숫자 예제까지만 있다. PPO용 경험 수집, 미니배치 반복 갱신, 전체 학습 함수가 구현되어 있는 것은 아니다.

---

## 18. 이전 정책과 현재 정책의 확률 비율

PPO는 수집 당시 실제 선택한 행동의 확률을 비교한다.

$$
r_t(\theta)
=\frac{\pi_\theta(a_t\mid s_t)}
{\pi_{\theta_{\mathrm{old}}}(a_t\mid s_t)}.
$$

| 부분 | 의미 |
| --- | --- |
| 분모 | 경험을 수집한 당시 정책의 행동 확률 |
| 분자 | 현재 갱신 중인 정책의 같은 행동 확률 |
| $r_t=1$ | 확률이 같음 |
| $r_t>1$ | 해당 행동의 확률 증가 |
| $r_t<1$ | 해당 행동의 확률 감소 |

여기의 $r_t$는 **확률 비율**을 뜻한다. 앞의 환경 보상에도 흔히 같은 문자를 쓰므로 문맥으로 구분해야 한다.

### 40%에서 60%로 바뀌었다면

```python
old_probability = 0.4
new_probability = 0.6
ratio = new_probability / old_probability
print(f"확률 비율: {ratio:.2f}, 이전 대비 변화: {(ratio - 1) * 100:.0f}%")
```

실행 결과:

```text
확률 비율: 1.50, 이전 대비 변화: 50%
```

40%에서 60%는 **20%포인트 증가**이면서 상대적으로는 **50% 증가**다. 확률이 150%가 되었다는 뜻은 아니다.

행동이 여러 개라도 여기서는 실제로 수집한 행동 $a_t$에 대한 확률을 비교한다. 분모를 갱신할 때마다 새 정책의 값으로 바꾸면 경험 수집 당시 정책과의 비교라는 의미가 사라진다.

---

## 19. PPO Clipping 목적함수 읽기

노트북에 있는 목적함수는 다음과 같다.

$$
L^{\mathrm{CLIP}}(\theta)
=\mathbb E_t\left[
\min\left(
r_t(\theta)A_t,
\operatorname{clip}\bigl(r_t(\theta),1-\epsilon,1+\epsilon\bigr)A_t
\right)\right].
$$

이를 다음 순서로 읽는다.

1. 실제 확률 비율에 Advantage를 곱한다: $r_tA_t$.
2. 확률 비율을 지정 범위로 자른 뒤 Advantage를 곱한다.
3. 두 값 중 작은 것을 고른다.
4. 표본에 대해 평균하고 그 값을 크게 만드는 방향으로 정책을 갱신한다.

예를 들어 $\epsilon=0.2$이면 Clipping에 사용하는 비율 범위는 $[0.8,1.2]$다.

```text
비율 0.7 -> Clipping 값 0.8
비율 1.0 -> Clipping 값 1.0
비율 1.5 -> Clipping 값 1.2
```

최종 목적값은 잘린 항만 사용하는 것이 아니라 **원래 항과 잘린 항의 최솟값**이다. 특히 음수 Advantage에서는 곱한 뒤의 숫자 순서를 주의해야 한다.

여기의 $\epsilon$은 86일차 epsilon-greedy의 탐험 확률이 아니다. 이름이 비슷하지만 **정책 비율의 Clipping 폭**을 뜻한다.

---

## 20. 네 가지 경우를 코드로 계산하기

원본의 숫자 예제를 그대로 사용하되, 변수명 `clippied`를 문서에서는 `clipped`로 정리했다.

```python
import numpy as np

for ratio, advantage in [
    (1.5, 2),
    (0.7, 2),
    (1.5, -2),
    (0.7, -2),
]:
    raw = ratio * advantage
    clipped = np.clip(ratio, 0.8, 1.2) * advantage
    objective = min(raw, clipped)
    print(
        f"r={ratio:.1f}, A={advantage:+.0f}, "
        f"원래={raw:+.2f}, 잘린={clipped:+.2f}, PPO={objective:+.2f}"
    )
```

계산 결과:

```text
r=1.5, A=+2, 원래=+3.00, 잘린=+2.40, PPO=+2.40
r=0.7, A=+2, 원래=+1.40, 잘린=+1.60, PPO=+1.40
r=1.5, A=-2, 원래=-3.00, 잘린=-2.40, PPO=-3.00
r=0.7, A=-2, 원래=-1.40, 잘린=-1.60, PPO=-1.60
```

| 확률 변화 | Advantage | 선택되는 값 | 의미 |
| --- | ---: | ---: | --- |
| 증가, 비율 1.5 | +2 | +2.40 | 좋은 행동의 과도한 확률 증가에 따른 추가 이득 제한 |
| 감소, 비율 0.7 | +2 | +1.40 | 좋은 행동 확률을 낮춘 불리한 변화는 그대로 반영 |
| 증가, 비율 1.5 | -2 | -3.00 | 나쁜 행동 확률을 높인 불리한 변화는 그대로 반영 |
| 감소, 비율 0.7 | -2 | -1.60 | 나쁜 행동의 과도한 확률 감소에 따른 추가 이득 제한 |

**원본 주석의 숫자와 구분:** 세 번째·네 번째 경우를 설명한 주석의 `-1.40`, `-2.40`은 최종 PPO 값과 맞지 않는다. 실제 코드 계산과 저장된 출력은 각각 **-3.00, -1.60**이며 이 문서도 그 값을 사용한다. 원본 파일 자체는 수정하지 않았다.

---

## 21. 양수·음수 Advantage에서 제한 방향이 다른 이유

### Advantage가 양수라면

선택한 행동이 평균보다 좋다고 평가한 경우다. 비율을 높이면 목적값이 커지지만 $1+\epsilon$을 넘는 부분에는 그 표본의 추가 이득을 주지 않는다.

$$
A_t>0:\qquad
\ell_t=\min(r_t,1+\epsilon)A_t.
$$

반대로 좋은 행동의 확률을 낮추는 변화는 잘라서 유리하게 만들어 주지 않는다.

### Advantage가 음수라면

선택한 행동이 평균보다 나쁘다고 평가한 경우다. 확률을 낮추면 목적값이 덜 음수가 되어 커지지만 $1-\epsilon$보다 더 낮춰 얻는 추가 이득은 제한한다.

$$
A_t<0:\qquad
\ell_t=\max(r_t,1-\epsilon)A_t.
$$

여기서 `max`가 나온다고 원래 목적함수의 `min`이 바뀐 것은 아니다. 음수를 곱하면 크기 순서가 뒤집히기 때문에 같은 식을 정리하면 이 형태가 된다.

예를 들어 $A=-2$에서 비율 1의 목적값은 -2다. 비율을 0.8로 낮추면 -1.6이 되어 목적값이 **증가**한다. 음수 값에서는 절댓값이 줄어드는 것이 개선일 수 있다.

---

## 22. Clipping이 보장하지 않는 것

### 실제 행동 확률을 강제로 범위 안에 고정하지 않는다

이전 확률이 0.4이고 $\epsilon=0.2$라면 Clipping 계산에 대응하는 확률은 $0.4\times0.8=0.32$와 $0.4\times1.2=0.48$이다. 확률에 0.2를 직접 더하고 빼는 범위가 아니다.

그러나 새 확률을 이 구간으로 강제 대입하는 것은 아니다. 목적함수의 한 항에서 추가 이득을 제한할 뿐, 신경망의 다른 표본·손실·공유 파라미터 변화로 실제 비율이 범위 밖으로 갈 수 있다.

### 무조건 성능이 좋아진다는 보장도 아니다

이 목적함수만으로 모든 상태의 정책 변화나 실제 보상의 단조 증가가 보장되는 것은 아니다. Clipping은 정책 개선을 보다 보수적으로 유도하는 장치다.

### 손실에서는 부호를 바꾼다

위 $L^{\mathrm{CLIP}}$는 크게 만드는 목적값이다. 일반적인 손실 최소화 코드에서는 음수를 취한다.

```python
# ratio와 advantages가 준비된 경우의 정책 손실 계산 발췌다.
raw = ratio * advantages
clipped = torch.clamp(ratio, 1 - epsilon, 1 + epsilon) * advantages
actor_loss = -torch.minimum(raw, clipped).mean()
```

이 블록은 수식을 PyTorch로 옮긴 **보충 발췌**이며, 제공된 노트북에 완성된 PPO 학습 코드가 있다는 뜻은 아니다. 실제 학습에서는 수집 당시 정책 확률과 Advantage를 고정하는 경사 경로 등의 처리가 함께 필요하다.

---

## 23. A2C·A3C·PPO를 한눈에 비교하기

| 항목 | A2C | A3C | 이번 자료의 PPO-Clip |
| --- | --- | --- | --- |
| 공통 기반 | 정책과 가치 학습 | 정책과 가치 학습 | Advantage를 사용한 정책 개선 |
| 핵심 관심 | 경험을 모아 동기식 갱신 | 독립 Worker의 비동기적 진행 | 이전 정책 대비 변화의 추가 이득 제한 |
| 이 자료의 구현 | 85일차 CartPole 학습 | 멀티프로세스 CartPole 학습 | 확률 비율·Clipping 숫자 계산 |
| 구분해야 할 점 | 여러 환경이 곧 병렬 프로세스는 아님 | Lock을 사용해 Global 갱신은 직렬화 | Clipping이 실제 확률의 강제 상한은 아님 |

A3C는 주로 경험 수집과 갱신의 **실행 구조**, PPO-Clip은 정책 갱신의 **목적함수**에 초점을 둔다. 따라서 PPO를 사용한다는 이유만으로 프로세스가 하나여야 한다는 뜻은 아니며, 셋의 이름만으로 모든 구현 세부 사항이 결정되는 것도 아니다.

---

## 24. 핵심 정리

1. A3C는 각 Worker가 Local Network로 경험과 경사를 계산하고 Global을 함께 개선한다.
2. 이번 예제는 Global 파라미터와 Adam 상태를 공유하며, Global 갱신은 Lock으로 보호한다.
3. Queue에는 경사가 아니라 Worker별 에피소드 점수를 전달한다.
4. 학습 점수, 마지막 Queue 기록 평균, 고정 정책 평가, 최고 체크포인트 평가는 서로 다른 측정이다.
5. PPO-Clip은 이전·현재 정책의 선택 행동 확률 비율과 Advantage를 결합한다.
6. `min()`은 유리한 방향의 과도한 변화가 주는 추가 이득은 제한하고, 불리한 변화는 그대로 반영하는 역할을 한다.
7. 원본 PPO 주석의 일부 숫자는 계산과 달랐으며, 음수 Advantage의 최종 값은 -3.00과 -1.60이다.

> A3C에서는 **누가 어떤 파라미터로 경사를 계산하고 언제 공유 모델을 갱신하는지**, PPO에서는 **어떤 방향의 확률 변화에 추가 이득을 더 이상 주지 않는지**를 구분하는 것이 핵심이다.

## 참고한 원자료

- 제공된 `5_A2C_A3C_PPO.ipynb`의 A3C·PPO 설명과 예제.
- 제공된 `5_A3C예제.py`의 실제 구현.
- 같은 폴더의 `a3c_scores.npy`에 저장된 학습 기록.
- A3C의 배경은 [원 논문](https://arxiv.org/abs/1602.01783), PPO의 출처는 [PPO 논문](https://arxiv.org/abs/1707.06347)에서 확인할 수 있다. 이 문서는 해당 논문 전체의 해석이 아니라 제공된 실습 자료를 중심으로 정리한 것이다.
