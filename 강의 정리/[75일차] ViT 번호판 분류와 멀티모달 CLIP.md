# [75일차] ViT 번호판 분류와 멀티모달 CLIP

실제 번호판 데이터를 전처리하고 사전 학습된 ViT에 네 개의 분류 Head를 연결하는 과정, 그리고 이미지와 텍스트를 함께 다루는 멀티모달 학습과 CLIP의 원리를 정리한다.

```text
번호판 이미지 분류
이미지 → ViT → 네 자리 숫자 예측

멀티모달 학습
이미지 + 텍스트 → 공통 의미 공간에서 관계 학습
```

---

## 1. 번호판 분류 실습 흐름

번호판 분류 모델의 전체 처리 과정은 다음과 같다.

```text
번호판 이미지와 JSON Annotation
            ↓
이미지 증강 및 정규화
            ↓
Dataset과 DataLoader
            ↓
사전 학습된 ViT Backbone
            ↓
공통 이미지 특징 벡터
            ↓
┌────────┬────────┬────────┬────────┐
│ Head 1 │ Head 2 │ Head 3 │ Head 4 │
│ 0~9    │ 0~9    │ 0~9    │ 0~9    │
└────────┴────────┴────────┴────────┘
            ↓
네 자리 숫자 예측
```

예를 들어 정답이 `1568`이라면 Label은 다음과 같이 표현한다.

```python
target = torch.tensor([1, 5, 6, 8])
```

하나의 모델이 네 개의 숫자를 동시에 예측하지만 각 자리에서는 `0~9` 중 하나만 선택한다. 따라서 네 개의 다중 클래스 분류 문제를 함께 학습하는 Multi-Head Classification 구조다.

---

## 2. ToTensor와 ToTensorV2

이미지 모델에 데이터를 입력하려면 PIL 이미지나 NumPy 배열을 PyTorch Tensor로 변환해야 한다.

### torchvision.transforms.ToTensor

`ToTensor()`는 PIL 이미지 또는 NumPy 배열을 Tensor로 변환한다.

```text
입력 차원:  H × W × C
출력 차원:  C × H × W

uint8 픽셀 범위
0~255 → 0~1
```

### albumentations.pytorch.ToTensorV2

`ToTensorV2()`는 Albumentations 전처리를 마친 NumPy 배열을 PyTorch Tensor로 변환한다.

```text
입력 차원:  H × W × C
출력 차원:  C × H × W
```

`ToTensorV2()` 자체는 일반적으로 픽셀 값을 자동으로 `0~1` 범위로 바꾸는 역할을 하지 않는다. 따라서 이번 코드에서는 앞 단계의 `A.Normalize()`가 픽셀 범위 변환과 정규화를 담당한다.

| 구분 | `ToTensor()` | `ToTensorV2()` |
|---|---|---|
| 주로 사용하는 라이브러리 | torchvision | Albumentations |
| 대표 입력 | PIL, NumPy | NumPy |
| 차원 변경 | HWC → CHW | HWC → CHW |
| uint8 값 처리 | 일반적으로 0~255 → 0~1 | 기본적으로 값 유지 |

---

## 3. Albumentations 이미지 전처리

학습 데이터에는 작은 기하학적 변화와 밝기 변화를 적용한다. 검증 데이터에는 무작위 증강을 적용하지 않고 크기 조정과 정규화만 수행한다.

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

IMAGE_SIZE = 224

train_transform = A.Compose([
    A.Affine(
        scale=(0.92, 1.08),
        translate_percent=(-0.04, 0.04),
        rotate=(-8, 8),
        shear=(-3, 3),
        border_mode=0,
        p=0.6,
    ),
    A.RandomBrightnessContrast(
        brightness_limit=0.15,
        contrast_limit=0.15,
        p=0.3,
    ),
    A.LongestMaxSize(max_size=IMAGE_SIZE),
    A.PadIfNeeded(
        min_height=IMAGE_SIZE,
        min_width=IMAGE_SIZE,
        border_mode=0,
    ),
    A.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    ),
    ToTensorV2(),
])

val_transform = A.Compose([
    A.LongestMaxSize(max_size=IMAGE_SIZE),
    A.PadIfNeeded(
        min_height=IMAGE_SIZE,
        min_width=IMAGE_SIZE,
        border_mode=0,
    ),
    A.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    ),
    ToTensorV2(),
])
```

### A.Affine

이미지의 크기, 위치, 회전, 기울기를 조금씩 바꾼다.

| 설정 | 의미 |
|---|---|
| `scale=(0.92, 1.08)` | 원본 크기의 92~108% 범위로 확대·축소 |
| `translate_percent=(-0.04, 0.04)` | 가로와 세로 위치를 최대 4% 정도 이동 |
| `rotate=(-8, 8)` | -8도부터 8도 사이로 회전 |
| `shear=(-3, 3)` | 이미지를 조금 기울임 |
| `p=0.6` | 60% 확률로 변환 적용 |

촬영 각도와 번호판 위치가 조금씩 달라지는 상황을 학습 데이터에 인위적으로 만들어 모델의 일반화 성능을 높인다.

### A.RandomBrightnessContrast

밝기와 대비를 무작위로 바꾼다. 햇빛, 그늘, 야간 조명처럼 촬영 환경이 달라지는 상황을 학습하는 데 도움이 된다.

### LongestMaxSize와 PadIfNeeded

번호판 이미지는 일반적으로 가로로 길다. 이미지를 바로 `224 × 224`로 강제 변환하면 숫자의 가로세로 비율이 달라질 수 있다.

```text
LongestMaxSize
가장 긴 변을 224로 맞추면서 원본 비율 유지
              ↓
PadIfNeeded
부족한 영역을 채워 최종 크기를 224 × 224로 맞춤
```

이 조합은 번호판의 비율을 유지하면서 ViT 입력 크기를 맞춘다.

### Normalize

사전 학습 모델이 사용한 ImageNet 평균과 표준편차에 맞춰 각 채널을 정규화한다.

```text
정규화된 값 = (픽셀 값 - 평균) / 표준편차
```

사전 학습 당시와 입력 데이터의 분포를 비슷하게 맞추기 위한 과정이다.

---

## 4. JSON Annotation Dataset 만들기

Annotation의 한 항목은 파일명과 네 자리 숫자 정답을 가진다.

```python
{
    "filename": "21구2298.jpg",
    "labels": "2298"
}
```

사용자 정의 Dataset은 이미지 파일을 읽고 문자열 정답을 네 개의 정수로 변환한다.

```python
class JsonDataset(Dataset):
    def __init__(self, image_dir, annotations, transform=None):
        self.image_dir = Path(image_dir)
        self.annotations = annotations
        self.transform = transform

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, index):
        item = self.annotations[index]
        image_path = self.image_dir / item["filename"]

        image = np.array(Image.open(image_path).convert("RGB"))
        target = torch.tensor(
            [int(number) for number in item["labels"]],
            dtype=torch.long,
        )

        if self.transform is not None:
            image = self.transform(image=image)["image"]

        return image, target
```

`"2298"`은 다음 과정을 거쳐 Tensor가 된다.

```text
"2298"
   ↓ 문자열 순회
['2', '2', '9', '8']
   ↓ int 변환
[2, 2, 9, 8]
   ↓ Tensor 변환
tensor([2, 2, 9, 8])
```

`CrossEntropyLoss`의 정답 클래스는 정수형이어야 하므로 `dtype=torch.long`을 사용한다.

---

## 5. DataLoader 구성

학습과 검증 Dataset에는 서로 다른 Transform을 적용한다.

```python
train_dataset = JsonDataset(
    IMAGE_DIR,
    train_annot,
    train_transform,
)

val_dataset = JsonDataset(
    IMAGE_DIR,
    val_annot,
    val_transform,
)

NUM_WORKERS = 0
BATCH_SIZE = 32
PIN_MEMORY = DEVICE.type == "cuda"

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=NUM_WORKERS,
    pin_memory=PIN_MEMORY,
    persistent_workers=(NUM_WORKERS > 0),
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=NUM_WORKERS,
    pin_memory=PIN_MEMORY,
    persistent_workers=(NUM_WORKERS > 0),
)
```

검증용 DataLoader에는 반드시 `val_dataset`을 전달해야 한다. 학습 Dataset을 사용하면 학습 데이터로 검증하게 되어 올바른 성능을 측정할 수 없다.

실행 결과 한 배치의 크기는 다음과 같다.

```text
images:  torch.Size([32, 3, 224, 224])
targets: torch.Size([32, 4])

예시 target: tensor([1, 5, 6, 8])
```

```text
images
32 : 한 배치의 이미지 수
3  : RGB 채널
224 × 224 : 이미지 크기

targets
32 : 한 배치의 정답 수
4  : 번호판의 네 자리 숫자
```



---

## 6. timm의 사전 학습 ViT 사용하기

직접 ViT 전체 구조를 다시 구현하지 않고 `timm` 라이브러리의 사전 학습 모델을 사용한다.

```python
import timm

MODEL_NAME = "vit_small_patch16_224"
```

모델 이름은 다음 정보를 나타낸다.

| 이름 | 의미 |
|---|---|
| `vit` | Vision Transformer |
| `small` | Small 크기의 ViT 모델 |
| `patch16` | 입력 이미지를 16 × 16 패치로 분할 |
| `224` | 기본 입력 크기 224 × 224 |

실행 결과에서 확인한 주요 구조는 다음과 같다.

```text
Patch Embedding
Conv2d(3, 384, kernel_size=16, stride=16)

Embedding 차원
384

Transformer Block
12개

각 Block의 MLP
384 → 1536 → 384
```

---

## 7. ViT Multi-Head Classifier

ViT Backbone 하나가 이미지 전체의 특징을 만들고, 네 개의 분류 Head가 각 자리 숫자를 예측한다.

```python
class ViTMultiHeadClassifier(nn.Module):
    def __init__(
        self,
        num_classes=10,
        num_heads_out=4,
        model_name=MODEL_NAME,
        pretrained=True,
        head_dropout=0.2,
    ):
        super().__init__()

        self.backbone = timm.create_model(
            model_name,
            pretrained=pretrained,
            num_classes=0,
        )

        feature_dim = self.backbone.num_features

        self.heads = nn.ModuleList([
            nn.Sequential(
                nn.LayerNorm(feature_dim),
                nn.Dropout(head_dropout),
                nn.Linear(feature_dim, num_classes),
            )
            for _ in range(num_heads_out)
        ])

    def forward(self, x):
        features = self.backbone(x)
        return [head(features) for head in self.heads]
```

### num_classes=0

`timm.create_model()`에 `num_classes=0`을 전달하면 원래 모델의 분류기를 제거하고 Backbone의 특징 벡터를 반환한다.

```text
기존 ViT
이미지 → Backbone → 기존 분류기

이번 모델
이미지 → Backbone → 특징 벡터 → 사용자 정의 Head 4개
```

### nn.ModuleList

일반 Python 리스트 대신 `nn.ModuleList`를 사용해야 네 개의 Head가 PyTorch 모델의 하위 모듈로 등록된다. 그래야 각 Head의 파라미터가 다음 작업에 포함된다.

- `model.parameters()` 조회
- Optimizer 업데이트
- Device 이동
- 모델 저장과 불러오기

### Head 내부 구조

```text
ViT 특징 벡터 384차원
        ↓
LayerNorm
        ↓
Dropout(0.2)
        ↓
Linear(384, 10)
        ↓
숫자 0~9에 대한 logits
```

---

## 8. 모델 출력 확인

가상 이미지 두 장을 모델에 입력해 Head별 출력 형태를 확인한다.

```python
sample_input = torch.randn(
    2,
    3,
    IMAGE_SIZE,
    IMAGE_SIZE,
    device=DEVICE,
)

with torch.no_grad():
    sample_outputs = model(sample_input)

print("Head 개수:", len(sample_outputs))

for index, output in enumerate(sample_outputs, start=1):
    print(f"Head {index}:", output.shape)
```

출력 결과는 다음과 같다.

```text
Head 개수: 4
Head 1: torch.Size([2, 10])
Head 2: torch.Size([2, 10])
Head 3: torch.Size([2, 10])
Head 4: torch.Size([2, 10])
```

이미지가 두 장이므로 각 Head는 `(2, 10)` 형태의 logits를 반환한다.

---

## 9. 손실 함수와 Optimizer

```python
EPOCHS = 10
LR = 3e-5
WEIGHT_DECAY = 0.05
LABEL_SMOOTHING = 0.1

criterion = nn.CrossEntropyLoss(
    label_smoothing=LABEL_SMOOTHING,
)

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LR,
    weight_decay=WEIGHT_DECAY,
)

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=EPOCHS,
    eta_min=LR * 0.05,
)
```

### Label Smoothing

일반적인 정답은 실제 클래스에 확률 1, 나머지 클래스에 0을 부여한다. Label Smoothing은 정답 분포를 조금 부드럽게 만들어 모델이 특정 클래스에 지나치게 확신하는 현상을 줄인다.

```text
일반 정답
[0, 0, 1, 0, ...]

Label Smoothing 적용
[작은 값, 작은 값, 큰 값, 작은 값, ...]
```

### AdamW

AdamW는 Adam의 적응적 학습률 조절과 Weight Decay를 분리하여 적용하는 Optimizer다. Transformer 계열 모델을 미세 조정할 때 자주 사용한다.

### CosineAnnealingLR

학습률을 코사인 곡선 형태로 점차 감소시킨다.

```text
초기 학습률
0.00003
    ↓
Epoch가 진행되면서 부드럽게 감소
    ↓
최소 학습률
0.00003 × 0.05 = 0.0000015
```

초반에는 비교적 큰 폭으로 학습하고, 후반에는 작은 학습률로 파라미터를 세밀하게 조정한다.

---

## 10. AMP와 Mixed Precision

AMP(Automatic Mixed Precision)는 연산에 따라 FP32와 낮은 정밀도의 자료형을 함께 사용하여 학습 속도와 메모리 사용량을 개선하는 기술이다.

| 자료형 | 특징 |
|---|---|
| FP32 | 정밀도가 높지만 메모리 사용량과 계산 비용이 큼 |
| FP16 | 정밀도가 낮지만 메모리 사용량이 작고 GPU 연산이 빠름 |
| BF16 | FP16보다 표현 가능한 값의 범위가 넓어 학습에 활용됨 |

FP64는 FP16보다 정밀도가 더 높은 자료형이므로 낮은 정밀도 자료형으로 설명하면 안 된다.

현재 학습 코드에서 Autocast를 CUDA일 때만 활성화한다면 GradScaler도 같은 조건으로 맞추는 편이 명확하다.

```python
use_amp = DEVICE.type == "cuda"

scaler = torch.amp.GradScaler(
    "cuda",
    enabled=use_amp,
)
```

```python
with torch.amp.autocast(
    device_type=DEVICE.type,
    dtype=torch.float16,
    enabled=use_amp,
):
    outputs = model(images)
```

MPS의 AMP 지원 범위와 동작은 PyTorch 버전에 따라 달라질 수 있으므로 CUDA용 설정을 그대로 MPS에 적용하면 안 된다.

---

## 11. 네 개 Head의 Loss 계산

각 자리에서 Cross Entropy Loss를 구한 뒤 네 Loss의 평균을 최종 손실로 사용한다.

```python
outputs = model(images)

losses = [
    criterion(outputs[position], targets[:, position])
    for position in range(4)
]

loss = torch.stack(losses).mean()
```

```text
Head 1 Loss ┐
Head 2 Loss ├─ 평균 → 최종 Loss
Head 3 Loss ┤
Head 4 Loss ┘
```

모든 자리의 Loss가 역전파에 함께 사용되므로 ViT Backbone은 네 자리 숫자를 인식하는 데 공통으로 필요한 특징을 학습한다.

---

## 12. 모델 평가 함수

평가할 때는 가중치를 변경하지 않으므로 `@torch.no_grad()`를 사용한다.

```python
@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()

    total_loss = 0.0
    total_samples = 0
    correct_per_head = torch.zeros(4, dtype=torch.long)
    exact_correct = 0

    for images, targets in loader:
        images = images.to(device)
        targets = targets.to(device)

        outputs = model(images)

        losses = [
            criterion(outputs[position], targets[:, position])
            for position in range(4)
        ]
        loss = torch.stack(losses).mean()

        predictions = torch.stack(
            [output.argmax(dim=1) for output in outputs],
            dim=1,
        )

        batch_size = images.size(0)
        total_loss += loss.item() * batch_size
        total_samples += batch_size

        correct_matrix = predictions.eq(targets)
        correct_per_head += correct_matrix.sum(dim=0).cpu()
        exact_correct += correct_matrix.all(dim=1).sum().item()

    digit_accuracy = (
        correct_per_head.float() / total_samples
    ).tolist()
    exact_accuracy = exact_correct / total_samples

    return {
        "loss": total_loss / total_samples,
        "digit_acc": digit_accuracy,
        "exact_acc": exact_accuracy,
    }
```

### 자리별 정확도

```text
D1: 첫 번째 자리 정확도
D2: 두 번째 자리 정확도
D3: 세 번째 자리 정확도
D4: 네 번째 자리 정확도
```

### Exact Match Accuracy

네 자리를 모두 맞힌 경우에만 정답으로 계산한다.

```text
정답: 1568
예측: 1568 → 정답

정답: 1568
예측: 1563 → 오답
```

자리별 정확도가 높아도 한 자리만 틀리면 전체 번호판은 잘못 인식한 것이다. 실제 번호판 인식 성능을 판단할 때 Exact Match Accuracy가 중요하다.

---

## 13. 모델 학습 과정

한 Epoch의 학습 과정은 다음과 같다.

```text
1. model.train()
2. 이미지와 정답을 Device로 이동
3. optimizer의 기존 Gradient 초기화
4. Forward 연산
5. 네 Head의 Loss 평균 계산
6. Backward 연산
7. Gradient Clipping
8. Optimizer로 파라미터 갱신
```

Gradient Clipping은 Gradient가 지나치게 커지는 현상을 막는다.

```python
torch.nn.utils.clip_grad_norm_(
    model.parameters(),
    max_norm=1.0,
)
```

각 Epoch가 끝난 뒤에는 다음 과정을 수행한다.

```text
Train Loss 계산
      ↓
Validation 평가
      ↓
Scheduler로 학습률 변경
      ↓
History 저장
      ↓
최고 Exact Accuracy이면 Checkpoint 저장
```

---

## 14. Checkpoint 저장

최고 성능 모델을 저장할 때 가중치뿐 아니라 학습을 다시 이어가는 데 필요한 정보도 함께 저장한다.

```python
torch.save({
    "epoch": epoch,
    "model_name": MODEL_NAME,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "scheduler_state_dict": scheduler.state_dict(),
    "best_exact_acc": best_exact_acc,
    "image_size": IMAGE_SIZE,
    "num_classes": 10,
    "num_heads_out": 4,
}, best_path)
```

| 저장 항목 | 목적 |
|---|---|
| `epoch` | 어느 Epoch에서 저장했는지 확인 |
| `model_state_dict` | 학습된 모델 가중치 |
| `optimizer_state_dict` | Optimizer 상태 복원 |
| `scheduler_state_dict` | 학습률 Scheduler 상태 복원 |
| `best_exact_acc` | 저장 당시 최고 성능 |
| 모델 설정값 | 같은 구조로 모델 재생성 |

현재 노트북 출력에는 DataLoader와 모델 출력 형태까지 확인되어 있지만 Epoch별 Loss와 정확도 결과는 남아 있지 않다. 따라서 실제 학습 성능 수치는 학습을 완료한 뒤 출력 결과로 확인해야 한다.

---

## 15. 멀티모달이란?

모달리티(Modality)는 정보가 표현되는 형태를 뜻한다.

| 모달리티 | 모델이 처리하는 정보 |
|---|---|
| 이미지 | 픽셀, 색상, 사물, 위치, 장면 |
| 텍스트 | 단어, 문장, 문맥, 의미 |
| 오디오 | 음성, 소리, 음악 |
| 비디오 | 시간에 따라 변화하는 이미지와 오디오 |

멀티모달 학습(Multimodal Learning)은 서로 다른 두 개 이상의 모달리티를 함께 학습하는 방식이다.

사람은 주변 상황을 이해할 때 하나의 정보만 사용하지 않는다.

```text
눈으로 장면을 확인한다.
말소리를 듣는다.
글을 읽는다.
이전 상황과 함께 의미를 판단한다.
```

멀티모달 모델도 이미지와 텍스트처럼 서로 다른 데이터가 제공하는 정보를 결합하여 더 풍부한 의미를 학습한다.

### 멀티모달 활용 예시

```text
이미지 + 텍스트 → 이미지 설명 생성
이미지 + 질문 → 시각 질의응답
영상 + 음성 → 감정이나 상황 인식
텍스트 → 관련 이미지 검색
이미지 → 관련 설명 검색
```

---

## 16. 멀티모달 모델의 핵심 용어

### 인코더

원본 데이터를 모델이 계산할 수 있는 숫자 특징으로 바꾸는 부분이다.

```text
이미지 인코더
사진 → 이미지 특징 벡터

텍스트 인코더
문장 → 텍스트 특징 벡터
```

### 임베딩

데이터의 의미를 숫자 배열인 벡터로 표현한 것이다. 의미가 비슷한 데이터는 임베딩 공간에서 가까운 위치에 놓이도록 학습할 수 있다.

```text
고양이 이미지 벡터
       ↕ 가까움
"a photo of a cat" 문장 벡터
```

### 프로젝션

이미지 인코더와 텍스트 인코더는 서로 다른 형태와 차원의 특징을 만들 수 있다. 프로젝션은 두 특징을 같은 차원의 공통 공간으로 변환한다.

```text
이미지 특징 ── 이미지 Projection ──┐
                                  ├─ 공통 임베딩 공간
텍스트 특징 ── 텍스트 Projection ──┘
```

### 유사도

두 벡터가 의미적으로 얼마나 가까운지 나타내는 값이다. CLIP은 이미지 임베딩과 텍스트 임베딩의 유사도를 비교한다.

---

## 17. CLIP

CLIP은 이미지와 텍스트를 같은 의미 공간에 정렬하는 대표적인 사전 학습 Vision-Language 모델이다.

CLIP은 두 개의 인코더를 사용하는 Dual Encoder 구조를 가진다.

```text
이미지
  ↓
이미지 인코더
  ↓
이미지 임베딩 ─────┐
                   ├─ 유사도 비교
텍스트 임베딩 ─────┘
  ↑
텍스트 인코더
  ↑
문장
```

이미지와 텍스트를 각각 독립적으로 벡터화할 수 있으므로 많은 이미지와 문장의 임베딩을 미리 만들어 빠르게 검색할 수 있다.

[CLIP 논문](https://arxiv.org/pdf/2103.00020)

---

## 18. 대비 학습

CLIP은 대비 학습(Contrastive Learning)을 사용한다.

한 배치에 이미지 4장과 각각의 설명 문장 4개가 있다면 모든 이미지와 문장의 유사도를 계산한다.

```text
             문장 1   문장 2   문장 3   문장 4
이미지 1      높음      낮음      낮음      낮음
이미지 2      낮음      높음      낮음      낮음
이미지 3      낮음      낮음      높음      낮음
이미지 4      낮음      낮음      낮음      높음
```

올바른 이미지와 문장 쌍은 대각선에 위치한다.

```text
고양이 사진 ↔ "a photo of a cat"    가까워지도록 학습
고양이 사진 ↔ "a photo of a banana" 멀어지도록 학습
고양이 사진 ↔ "a photo of a TV"     멀어지도록 학습
```

학습 목표는 다음과 같다.

```text
정답 이미지·텍스트 쌍의 유사도는 높인다.
관련 없는 이미지·텍스트 쌍의 유사도는 낮춘다.
```

많은 이미지와 텍스트 쌍으로 이 과정을 반복하면 모델은 단순한 클래스 번호가 아니라 시각적 특징과 언어 의미 사이의 관계를 학습한다.

---

## 19. Zero-Shot 이미지 분류

Zero-Shot은 새로운 작업을 위해 별도의 정답 예제를 제공하고 재학습하지 않은 상태에서 예측하는 방식을 뜻한다.

CLIP의 Zero-Shot 이미지 분류 과정은 다음과 같다.

```text
1. 후보 클래스 이름을 자연어 문장으로 만든다.
2. 각 후보 문장의 텍스트 임베딩을 만든다.
3. 입력 이미지의 이미지 임베딩을 만든다.
4. 이미지와 각 문장의 유사도를 비교한다.
5. 가장 유사한 문장을 예측 클래스로 선택한다.
```

예를 들어 후보 클래스가 고양이, 강아지, 자동차라면 다음 Prompt를 만든다.

```python
prompts = [
    "a photo of a cat",
    "a photo of a dog",
    "a photo of a car",
]
```

```text
입력 이미지 임베딩
       │
       ├─ "a photo of a cat" 유사도: 0.87
       ├─ "a photo of a dog" 유사도: 0.21
       └─ "a photo of a car" 유사도: 0.05

최종 예측: cat
```

기존 분류 모델은 클래스 수에 맞춘 새로운 Linear Layer와 학습 데이터가 필요하다. CLIP은 클래스 이름을 자연어 Prompt로 만들어 비교하므로 별도의 분류기 재학습 없이 후보 클래스를 바꿀 수 있다.

---

## 20. 이미지와 텍스트 검색

CLIP은 이미지와 텍스트를 같은 임베딩 공간에 배치하므로 양방향 검색에 활용할 수 있다.

### Text-to-Image Retrieval

텍스트를 입력하여 관련 이미지를 찾는다.

```text
"해변에서 뛰는 강아지"
          ↓
텍스트 임베딩
          ↓
저장된 이미지 임베딩들과 유사도 비교
          ↓
가장 관련 있는 이미지 반환
```

### Image-to-Text Retrieval

이미지를 입력하여 가장 잘 맞는 설명을 찾는다.

```text
입력 이미지
    ↓
이미지 임베딩
    ↓
후보 문장 임베딩들과 유사도 비교
    ↓
가장 관련 있는 문장 반환
```

CLIP은 기존 이미지와 텍스트의 관계를 이해하고 검색하는 데 강점이 있지만 새로운 문장을 직접 생성하는 모델은 아니다.

---

## 21. 멀티모달 모델 구조 비교

| 구조 | 대표 모델 | 핵심 기능 |
|---|---|---|
| Dual Encoder | CLIP | 이미지와 텍스트를 각각 임베딩하여 유사도 비교 |
| Encoder-Decoder | BLIP | 이미지 특징을 참고하여 문장을 토큰 단위로 생성 |
| Grounded Detection | Grounding DINO | 텍스트 조건과 관련된 이미지 영역을 Bounding Box로 탐지 |
| Vision-Language Model | 멀티모달 LLM | 이미지 기반 질의응답, 추론, 대화 |

### 표현 정렬과 생성의 차이

CLIP은 이미지와 텍스트 표현을 공통 공간에 정렬한다.

```text
이미지 → 벡터
텍스트 → 벡터
두 벡터의 유사도 비교
```

BLIP과 같은 Encoder-Decoder 모델은 이미지 특징을 참고하여 새로운 문장을 생성한다.

```text
이미지 → 이미지 특징 → 단어를 하나씩 생성 → 설명 문장
```

Grounding DINO는 텍스트와 관련된 객체가 이미지의 어느 위치에 있는지 찾는다.

```text
이미지 + "red car"
        ↓
빨간 자동차 영역의 Bounding Box
```

멀티모달 LLM은 이미지 특징을 언어 모델과 연결하여 질문에 답하거나 추론하는 기능을 제공한다. 구체적인 지원 기능은 모델마다 다르다.

---

## 22. ViT와 CLIP의 연결

ViT와 CLIP은 서로 경쟁하는 같은 종류의 모델이 아니다. ViT는 이미지를 특징 벡터로 변환하는 비전 인코더이고, CLIP은 이미지 특징과 텍스트 특징의 의미를 정렬하는 학습 구조다.

```text
ViT
이미지 → 패치 토큰 → Transformer → 이미지 특징

CLIP
이미지 특징 + 텍스트 특징 → 공통 공간에서 정렬
```

CLIP의 이미지 인코더로 ViT를 사용할 수 있다.

```text
이미지 ── ViT ── 이미지 임베딩 ──┐
                                 ├─ 유사도 비교
텍스트 ─ 텍스트 인코더 ─ 임베딩 ─┘
```

번호판 분류 실습에서는 ViT 특징 뒤에 고정된 숫자 분류 Head를 연결했다. CLIP에서는 ViT가 만든 이미지 특징을 텍스트 특징과 비교한다는 차이가 있다.

| 구분 | 번호판 ViT 분류 | CLIP |
|---|---|---|
| 입력 | 이미지 | 이미지와 텍스트 |
| 이미지 처리 | ViT Backbone | 이미지 인코더로 ViT 사용 가능 |
| 출력 | 네 자리 숫자 logits | 이미지·텍스트 임베딩과 유사도 |
| 학습 목표 | 숫자 정답과 Cross Entropy Loss | 올바른 이미지·텍스트 쌍의 유사도 증가 |
| 새로운 클래스 | 분류 Head 재구성과 학습 필요 | Prompt를 바꾸어 Zero-Shot 비교 가능 |

---

## 23. 핵심 정리

1. 번호판 이미지의 비율을 유지하려면 `LongestMaxSize`와 `PadIfNeeded`를 함께 사용할 수 있다.
2. `A.Normalize()`와 `ToTensorV2()`를 거치면 이미지가 ViT 입력용 Tensor로 변환된다.
3. JSON의 네 자리 문자열은 `(4,)` 형태의 정수 Tensor로 변환한다.
4. `vit_small_patch16_224`는 224 × 224 이미지를 16 × 16 패치로 처리하는 사전 학습 ViT다.
5. `num_classes=0`을 사용하면 기존 분류기를 제거하고 Backbone 특징을 얻을 수 있다.
6. 네 개의 Head는 각 자리에서 숫자 0부터 9까지를 분류한다.
7. 네 Head의 Cross Entropy Loss를 평균하여 모델을 학습한다.
8. 자리별 정확도와 네 자리 완전 일치 정확도를 함께 확인해야 한다.
9. 멀티모달 학습은 이미지, 텍스트, 오디오처럼 서로 다른 형태의 정보를 함께 다룬다.
10. CLIP은 이미지와 텍스트를 독립적으로 임베딩한 뒤 같은 의미 공간에서 정렬한다.
11. 대비 학습은 올바른 이미지·문장 쌍을 가깝게 하고 관련 없는 쌍을 멀어지게 한다.
12. CLIP은 별도의 분류기 학습 없이 자연어 Prompt를 이용한 Zero-Shot 분류가 가능하다.
13. CLIP은 검색과 표현 정렬에 강하지만 문장을 직접 생성하는 모델은 아니다.
14. ViT는 이미지 인코더이고 CLIP은 이미지와 텍스트 표현을 연결하는 학습 구조다.
