# [73일차] PLM과 KLUE-BERT 멀티라벨 분류

PLM(Pre-trained Language Model)은 대규모 텍스트로 언어의 일반적인 패턴을 먼저 학습한 모델이다. 학습이 끝난 PLM을 가져와 원하는 문제에 맞게 추가 학습하면 처음부터 모델을 만드는 것보다 적은 데이터와 시간으로 높은 성능을 얻을 수 있다.

이번에는 한국어 사전 학습 모델인 **KLUE-BERT**를 K-MHaS 데이터셋에 Fine-tuning해 하나의 문장에서 여러 혐오 표현 범주를 찾는 **멀티라벨 분류** 과정을 정리한다.

---

## 1. PLM

PLM은 대규모 텍스트 데이터에서 단어의 의미, 문장 구조, 문맥 관계를 미리 학습한 언어 모델이다.

```text
대규모 텍스트 데이터
        ↓
Pre-training
        ↓
언어의 일반적인 패턴을 학습한 PLM
        ↓
Fine-tuning
        ↓
문장 분류, 질의응답, 번역, 요약 등
```

대표적인 PLM에는 BERT, GPT, T5 등이 있다.

### Pre-training

Pre-training은 대규모 데이터에서 언어의 일반적인 패턴을 먼저 학습하는 단계다.

- 문장에서 단어가 사용되는 방식
- 문장 안에서 Token이 맺는 관계
- 앞뒤 문맥에 따라 달라지는 의미
- 문법과 표현 방식

### Fine-tuning

Fine-tuning은 사전 학습된 모델을 특정 문제에 맞게 추가 학습하는 단계다.

```text
사전 학습 BERT
    +
분류 Head
    +
K-MHaS 학습 데이터
    ↓
한국어 멀티라벨 혐오 표현 분류 모델
```

---

## 2. Transformer 모델 계열

Transformer 기반 PLM은 사용하는 구조에 따라 크게 세 종류로 나눌 수 있다.

| 구조 | 대표 모델 | 주요 방식 | 대표 작업 |
| --- | --- | --- | --- |
| Encoder-only | BERT | 문장 전체의 양방향 문맥을 이해한다. | 분류, 유사도, 개체명 인식, 질의응답 |
| Decoder-only | GPT | 이전 Token을 바탕으로 다음 Token을 생성한다. | 텍스트 생성, 대화, 코드 생성 |
| Encoder-Decoder | T5 | 입력을 이해한 뒤 새로운 출력 시퀀스를 생성한다. | 번역, 요약, Text-to-Text 작업 |

### BERT 계열

```text
입력 문장
   ↓
Transformer Encoder
   ↓
문맥이 반영된 표현
   ↓
분류 또는 질의응답 Head
```

BERT는 문장의 앞과 뒤를 함께 참고해 문맥을 이해한다.

### GPT 계열

```text
이전 Token들
   ↓
Transformer Decoder
   ↓
다음 Token 예측
   ↓
예측한 Token을 다시 입력해 생성 반복
```

이전 Token을 이용해 다음 Token을 순차적으로 생성하는 방식을 자기회귀(Autoregressive) 생성이라고 한다.

### T5 계열

T5는 Encoder와 Decoder를 모두 사용하며 여러 NLP 문제를 Text-to-Text 형식으로 통일한다.

```text
입력: translate English to Korean: I love coffee
출력: 나는 커피를 좋아한다
```

---

## 3. BERT와 MLM

BERT의 대표적인 사전 학습 목표는 MLM(Masked Language Modeling)이다.

문장의 일부 Token을 `[MASK]`로 가리고 주변 문맥을 이용해 원래 Token을 맞히도록 학습한다.

```text
대한민국의 수도는 [MASK]이다.
                ↓
        Transformer Encoder
                ↓
               서울
```

이 과정을 매우 많은 문장에서 반복하면 같은 단어라도 문맥에 따라 다른 표현을 만들 수 있다.

```text
배를 먹었다.       → 과일
배가 바다에 있다.  → 선박
배가 아프다.       → 신체
```

BERT는 단순한 단어 사전을 만드는 것이 아니라 **문장 안의 관계를 반영한 문맥적 표현**을 학습한다.

---

## 4. K-MHaS 데이터셋

K-MHaS는 한국어 온라인 뉴스 댓글의 혐오 표현을 분류하기 위한 멀티라벨 데이터셋이다.

![K-MHaS](./images/73일차/K-MHaS.png)

데이터는 공식적으로 Train, Validation, Test로 나뉘어 있다.

| 구간 | 데이터 수 |
| --- | ---: |
| Train | 78,977 |
| Validation | 8,776 |
| Test | 21,939 |
| 전체 | 109,692 |

각 행은 문장과 하나 이상의 라벨로 구성된다.

```text
document                              label
정치적 편견과 연령 비하를 함께 포함한 문장      2,4
혐오 표현에 해당하지 않는 일반 문장             8
```

### 라벨 구성

| 번호 | 라벨 |
| ---: | --- |
| 0 | 출신차별 |
| 1 | 외모차별 |
| 2 | 정치성향차별 |
| 3 | 혐오욕설 |
| 4 | 연령차별 |
| 5 | 성차별 |
| 6 | 인종차별 |
| 7 | 종교차별 |
| 8 | 해당사항없음 |

한 문장이 정치성향차별과 연령차별에 동시에 해당하면 라벨은 `2,4`처럼 여러 개가 기록된다.

---

## 5. 데이터 불러오기

노트북은 K-MHaS GitHub 저장소를 로컬 `data` 폴더에 복제한다.

```python
import subprocess
from pathlib import Path

PROJECT_DIR = Path.cwd()
DATA_DIR = PROJECT_DIR / "data"
REPO_DIR = DATA_DIR / "K-MHaS"

if not REPO_DIR.exists():
    subprocess.run(
        [
            "git",
            "clone",
            "https://github.com/adlnlp/K-MHaS",
            str(REPO_DIR),
        ],
        check=True,
    )
else:
    print("이미 저장소가 존재한다:", REPO_DIR)
```

`subprocess.run()`은 Python에서 외부 명령어를 실행한다. `check=True`를 지정하면 `git clone`이 실패했을 때 예외가 발생한다.

Hugging Face `datasets`의 `load_dataset()`으로 TSV 파일을 읽는다.

```python
from datasets import load_dataset

DATA_DIR = REPO_DIR / "data"

train = load_dataset(
    "csv",
    data_files=str(DATA_DIR / "kmhas_train.txt"),
    delimiter="\t",
    split="train",
)

validation = load_dataset(
    "csv",
    data_files=str(DATA_DIR / "kmhas_valid.txt"),
    delimiter="\t",
    split="train",
)

test = load_dataset(
    "csv",
    data_files=str(DATA_DIR / "kmhas_test.txt"),
    delimiter="\t",
    split="train",
)
```

여기서 각 호출의 `split="train"`은 K-MHaS의 세 구간을 다시 Train으로 합친다는 뜻이 아니다. 전달한 파일 하나를 `datasets.Dataset` 객체로 바로 반환하기 위한 옵션이다.

실행 결과:

```text
Train:      78,977 rows
Validation:  8,776 rows
Test:       21,939 rows
```

---

## 6. Multi-class와 Multi-label

Multi-class와 Multi-label은 출력과 Loss 구성이 다르다.

### Multi-class Classification

하나의 입력에 하나의 클래스만 정답이 된다.

```text
이미지 → 고양이, 강아지, 토끼 중 하나
```

클래스끼리 서로 경쟁하므로 일반적으로 Softmax를 사용한다.

```text
[고양이 0.1, 강아지 0.8, 토끼 0.1]
합계 = 1
```

### Multi-label Classification

하나의 입력이 여러 범주에 동시에 해당할 수 있다.

```text
문장
→ 정치성향차별=1
→ 혐오욕설=1
→ 성차별=0
→ 연령차별=1
```

각 라벨이 독립적인 이진 분류 문제이므로 각 출력에 Sigmoid를 적용한다.

```text
[0.12, 0.81, 0.77, 0.09, ...]
```

각 확률은 독립적이므로 합계가 `1`일 필요가 없다. 학습에는 보통 `BCEWithLogitsLoss` 계열 목적함수를 사용한다.

> `single_label_classification`은 이진 분류만 뜻하지 않는다. 하나의 정답만 선택하는 이진 또는 다중 클래스 분류를 모두 포함할 수 있다.

---

## 7. Multi-hot Vector 만들기

원본 라벨 문자열 `"2,4"`를 정수 리스트로 변환한다.

```python
def parse_label(value):
    return [
        int(x)
        for x in str(value).split(",")
    ]

train_y = [
    parse_label(x)
    for x in train["label"]
]
validation_y = [
    parse_label(x)
    for x in validation["label"]
]
test_y = [
    parse_label(x)
    for x in test["label"]
]
```

`MultiLabelBinarizer`로 여러 라벨을 Multi-hot Vector로 바꾼다.

```python
from sklearn.preprocessing import MultiLabelBinarizer

encoder = MultiLabelBinarizer()
encoder.fit(train_y)

num_labels = len(encoder.classes_)

train_labels = torch.tensor(
    encoder.transform(train_y),
    dtype=torch.float32,
)
validation_labels = torch.tensor(
    encoder.transform(validation_y),
    dtype=torch.float32,
)
test_labels = torch.tensor(
    encoder.transform(test_y),
    dtype=torch.float32,
)
```

실행 결과:

```text
클래스: [0 1 2 3 4 5 6 7 8]
클래스 수: 9
원래 라벨: [2, 4]
Multi-hot: [0, 0, 1, 0, 1, 0, 0, 0, 0]
```

Train, Validation, Test마다 `fit()`하면 클래스 위치의 의미가 달라질 수 있다. 하나의 Encoder를 Train에 `fit()`하고 모든 구간에 같은 `transform()`을 적용해야 한다.

---

## 8. BERT의 Special Token

BERT Tokenizer는 일반 Token 외에 특별한 역할을 가진 Token을 사용한다.

| Token | 역할 |
| --- | --- |
| `[CLS]` | 문장 전체를 대표하며 주로 분류에 사용한다. |
| `[SEP]` | 문장 또는 문장 쌍의 경계를 표시한다. |
| `[PAD]` | 길이가 다른 문장을 같은 길이로 맞춘다. |
| `[MASK]` | MLM 사전 학습에서 가린 Token을 나타낸다. |
| `[UNK]` | Vocabulary에 없는 Token을 나타낸다. |

KLUE-BERT의 Tokenizer를 불러온다.

```python
from transformers import AutoTokenizer

MODEL_NAME = "klue/bert-base"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("CLS:", tokenizer.cls_token, tokenizer.cls_token_id)
print("SEP:", tokenizer.sep_token, tokenizer.sep_token_id)
print("PAD:", tokenizer.pad_token, tokenizer.pad_token_id)
print("MASK:", tokenizer.mask_token, tokenizer.mask_token_id)
```

```text
CLS:  [CLS] 2
SEP:  [SEP] 3
PAD:  [PAD] 0
MASK: [MASK] 4
```

`AutoTokenizer`를 사용하면 모델 이름에 맞는 Tokenizer 클래스를 자동으로 선택한다. 이 예제에서는 `BertTokenizer`가 로드된다.

---

## 9. Tokenization 결과

Tokenizer의 전체 처리 흐름은 다음과 같다.

```text
문장
 ↓
Subword Tokenization
 ↓
Token ID 변환
 ↓
[CLS], [SEP] 추가
 ↓
Truncation과 Padding
 ↓
input_ids와 attention_mask 생성
```

### `input_ids`

각 Token을 Vocabulary의 정수 번호로 변환한 값이다.

```text
[CLS] 나는 학교에 간다 [SEP]
  2   ...   ...   ...    3
```

### `attention_mask`

실제 Token과 Padding을 구분한다.

```text
Token: [CLS] 나는 [SEP] [PAD] [PAD]
Mask:     1    1     1     0     0
```

`0`인 Padding 위치를 Attention의 참고 대상에서 제외한다.

### 샘플 확인

```python
sample = tokenizer(
    sample_text,
    add_special_tokens=True,
    truncation=True,
    max_length=64,
    return_tensors="pt",
    padding="max_length",
)

print(sample["input_ids"])
print(
    tokenizer.convert_ids_to_tokens(
        sample["input_ids"][0]
    )
)
print(sample["attention_mask"])
```

실행 결과에서는 한국어 단어가 다음처럼 Subword로 나뉜다.

```text
[CLS], 자, ##한, ##당, ##틀, ##딱, ##들, ... [SEP], [PAD], ...
```

`##`은 앞의 Subword와 이어지는 조각임을 나타낸다.

---

## 10. 전체 데이터 Encoding

```python
MAX_LEN = 128

def encode_texts(
    texts,
    labels,
    tokenizer,
    max_len=MAX_LEN,
):
    encoded = tokenizer(
        [
            "" if x is None else str(x)
            for x in texts
        ],
        add_special_tokens=True,
        truncation=True,
        max_length=max_len,
        return_tensors="pt",
        padding="max_length",
    )

    return (
        encoded["input_ids"],
        encoded["attention_mask"],
        labels.to(torch.float32),
    )
```

> 원본 코드에서는 함수 인자 `max_len` 대신 전역 변수 `MAX_LEN`을 사용한다. 재사용성을 위해 `max_length=max_len`으로 작성하는 편이 안전하다.

Train 데이터의 Encoding 결과는 다음과 같다.

```text
input_ids:      torch.Size([78977, 128])
attention_mask: torch.Size([78977, 128])
labels:         torch.Size([78977, 9])
```

각 Sample은 길이 128의 Token ID와 Mask, 길이 9의 Multi-hot Label을 가진다.

---

## 11. DataLoader 구성

```python
from torch.utils.data import (
    TensorDataset,
    DataLoader,
    RandomSampler,
    SequentialSampler,
)

BATCH_SIZE = 32

train_data = TensorDataset(
    train_inputs,
    train_mask,
    train_labels,
)
validation_data = TensorDataset(
    validation_inputs,
    validation_mask,
    validation_labels,
)
test_data = TensorDataset(
    test_inputs,
    test_mask,
    test_labels,
)

train_dataloader = DataLoader(
    train_data,
    sampler=RandomSampler(train_data),
    batch_size=BATCH_SIZE,
)

validation_dataloader = DataLoader(
    validation_data,
    sampler=SequentialSampler(validation_data),
    batch_size=BATCH_SIZE,
)

test_dataloader = DataLoader(
    test_data,
    sampler=SequentialSampler(test_data),
    batch_size=BATCH_SIZE,
)
```

- Train은 매 Epoch 데이터 순서를 섞는다.
- Validation과 Test는 Parameter를 업데이트하지 않으므로 일반적으로 순차적으로 읽는다.

한 Batch의 Shape은 다음과 같다.

```text
input_ids:      [32, 128]
attention_mask: [32, 128]
labels:         [32, 9]
```

---

## 12. KLUE-BERT 분류 모델

사전 학습된 KLUE-BERT Encoder 위에 9개 Logit을 출력하는 분류 Head를 붙인다.

```text
문장
 ↓
Tokenizer
 ↓
input_ids + attention_mask
 ↓
Pre-trained KLUE-BERT
 ↓
문장 Representation
 ↓
Linear Classification Head
 ↓
9개 Logit
 ↓ Sigmoid
각 라벨의 독립적인 확률
```

```python
from transformers import (
    AutoModelForSequenceClassification,
)

model = (
    AutoModelForSequenceClassification
    .from_pretrained(
        MODEL_NAME,
        num_labels=num_labels,
        problem_type="multi_label_classification",
    )
)

model.to(DEVICE)
```

`problem_type="multi_label_classification"`을 지정하면 Label이 전달되었을 때 Transformers가 멀티라벨 분류에 맞는 Loss를 사용한다.

### 모델 구조

KLUE-BERT Base의 주요 구성은 다음과 같다.

| 항목 | 값 |
| --- | ---: |
| Vocabulary 크기 | 32,000 |
| Hidden Size | 768 |
| Encoder Layer | 12 |
| FFN 중간 차원 | 3,072 |
| 최대 Position Embedding | 512 |
| 분류 출력 | 9 |

### Load Report 해석

모델을 불러올 때 다음과 같은 메시지가 나타난다.

```text
UNEXPECTED: 기존 사전 학습용 Head Parameter
MISSING: classifier.weight, classifier.bias
```

이는 기본 BERT Checkpoint를 다른 작업인 문장 분류 모델로 불러오기 때문에 발생한다.

- MLM 등 사전 학습용 Head는 현재 분류 작업에 사용하지 않아 `UNEXPECTED`가 된다.
- 9개 라벨용 Classification Head는 Checkpoint에 없으므로 새로 초기화되어 `MISSING`이 된다.

모델 종류를 의도적으로 바꾼 상황에서는 정상적인 메시지다. 새 Classification Head는 반드시 Fine-tuning해야 한다.

---

## 13. Full Fine-tuning과 PEFT

현재 코드는 BERT와 Classification Head의 모든 Parameter를 업데이트하는 **Full Fine-tuning** 방식이다.

```text
Pre-trained BERT Parameter  ┐
                            ├─ 모두 업데이트
Classification Head         ┘
```

데이터가 적거나 GPU 메모리가 제한적이면 다음 방법을 고려할 수 있다.

- BERT 일부 Layer를 Freeze한다.
- Classification Head만 먼저 학습한다.
- LoRA 같은 PEFT(Parameter-Efficient Fine-Tuning)를 사용한다.

> 올바른 약어는 `PRRT`가 아니라 **PEFT**다.

---

## 14. Optimizer와 Learning Rate Scheduler

BERT Fine-tuning에는 사전 학습 가중치를 크게 훼손하지 않도록 비교적 작은 Learning Rate를 사용한다.

```python
from torch.optim import AdamW
from transformers import (
    get_linear_schedule_with_warmup,
)

EPOCHS = 5
LEARNING_RATE = 2e-5

optimizer = AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=0.01,
)

total_steps = (
    len(train_dataloader) * EPOCHS
)

warmup_steps = int(total_steps * 0.1)

scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=warmup_steps,
    num_training_steps=total_steps,
)
```

노트북에서는 전체 학습 Step이 `12,345`로 계산되었다.

```text
초기 10% Step
Learning Rate를 0에서 2e-5까지 증가
                ↓
나머지 Step
Learning Rate를 선형으로 감소
```

Warmup은 초기의 큰 Gradient가 사전 학습 가중치를 급격하게 바꾸는 현상을 완화한다.

---

## 15. Fine-tuning Loop

```python
for epoch in range(EPOCHS):
    model.train()
    total_loss = 0.0

    for batch in train_dataloader:
        input_ids, attention_mask, labels = [
            x.to(DEVICE)
            for x in batch
        ]

        optimizer.zero_grad(set_to_none=True)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels,
        )

        loss = outputs.loss
        total_loss += loss.item()

        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(),
            max_norm=1.0,
        )

        optimizer.step()
        scheduler.step()
```

핵심 흐름은 다음과 같다.

```text
Forward
 ↓
Multi-label Loss 계산
 ↓
Backward
 ↓
Gradient Clipping
 ↓
Optimizer Step
 ↓
Scheduler Step
```

`clip_grad_norm_()`은 Gradient Norm이 지나치게 커질 때 값을 제한해 학습을 안정화한다.

---

## 16. 멀티라벨 평가 지표

모델의 Logit에 Sigmoid를 적용하고 Threshold 이상인 라벨을 `1`로 예측한다.

```python
def multi_label_metrics(
    logits,
    labels,
    threshold=0.5,
):
    probs = torch.sigmoid(
        torch.as_tensor(logits)
    ).cpu().numpy()

    y_true = np.asarray(labels)
    y_pred = (
        probs >= threshold
    ).astype(int)

    return {
        "subset_accuracy": accuracy_score(
            y_true,
            y_pred,
        ),
        "f1_micro": f1_score(
            y_true,
            y_pred,
            average="micro",
            zero_division=0,
        ),
        "f1_macro": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "f1_weighted": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),
        "hamming_loss": hamming_loss(
            y_true,
            y_pred,
        ),
        "roc_auc_micro": roc_auc_score(
            y_true,
            probs,
            average="micro",
        ),
    }
```

### 지표 의미

| 지표 | 의미 | 방향 |
| --- | --- | --- |
| Subset Accuracy | 한 Sample의 모든 라벨을 정확히 맞힌 비율이다. | 높을수록 좋다. |
| Micro F1 | 모든 라벨의 TP, FP, FN을 합쳐 계산한다. | 높을수록 좋다. |
| Macro F1 | 라벨별 F1을 동일한 비중으로 평균낸다. | 높을수록 좋다. |
| Weighted F1 | 라벨별 데이터 수를 반영해 F1을 평균낸다. | 높을수록 좋다. |
| Hamming Loss | 전체 라벨 판단 중 잘못 예측한 비율이다. | 낮을수록 좋다. |
| ROC-AUC Micro | 전체 라벨의 확률 순위 품질을 계산한다. | 높을수록 좋다. |

Subset Accuracy는 일부 라벨만 틀려도 Sample 전체를 오답으로 처리하므로 매우 엄격하다.

```text
정답: [1, 0, 1, 0]
예측: [1, 0, 1, 0] → 정답

정답: [1, 0, 1, 0]
예측: [1, 0, 0, 0] → 전체 오답
```

클래스 불균형이 있다면 Micro F1만 보지 말고 Macro F1과 라벨별 F1도 함께 확인해야 한다.

---

## 17. 평가 함수

```python
def evaluate(model, dataloader, device):
    model.eval()

    all_logits = []
    all_labels = []

    for batch in dataloader:
        input_ids, attention_mask, labels = [
            x.to(device)
            for x in batch
        ]

        with torch.inference_mode():
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
            )

        all_logits.append(outputs.logits.cpu())
        all_labels.append(labels.cpu())

    logits = torch.cat(all_logits).numpy()
    labels = torch.cat(all_labels).numpy()

    return multi_label_metrics(
        logits,
        labels,
    )
```

- `model.eval()`은 Dropout 등을 평가 모드로 전환한다.
- `torch.inference_mode()`는 Gradient 계산과 관련 상태 저장을 끈다.
- 전체 Batch의 Logit과 Label을 모은 뒤 지표를 한 번에 계산한다.

---

## 18. 모델 저장과 불러오기

### `state_dict()` 저장

```python
MODEL_DIR = Path.cwd() / "model"
MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

MODEL_PATH = (
    MODEL_DIR / "KLUE_BERT_multilabel.pt"
)

torch.save(
    model.state_dict(),
    MODEL_PATH,
)
```

노트북에서 생성된 파일의 크기는 약 `422MB`다.

### 모델 구조를 다시 만든 뒤 가중치 불러오기

```python
loaded_model = (
    AutoModelForSequenceClassification
    .from_pretrained(
        MODEL_NAME,
        num_labels=num_labels,
        problem_type="multi_label_classification",
    )
)

state_dict = torch.load(
    MODEL_PATH,
    map_location="cpu",
)

loaded_model.load_state_dict(state_dict)
loaded_model.to(DEVICE)
loaded_model.eval()
```

`state_dict()`에는 Parameter 값만 저장된다. 불러올 때는 저장 당시와 같은 모델 구조를 먼저 만들어야 한다.

Hugging Face 방식으로 모델과 설정을 함께 보관하려면 다음 방법도 사용할 수 있다.

```python
model.save_pretrained(MODEL_DIR)
tokenizer.save_pretrained(MODEL_DIR)
```

---

## 19. 현재 노트북 결과 해석

저장된 노트북을 확인하면 Fine-tuning Loop가 있는 Cell 38의 `execution_count`가 비어 있고 출력도 없다. 반면 모델 저장과 Test 평가는 이후에 실행되었다.

따라서 현재 저장된 결과는 **Fine-tuning을 완료한 모델의 성능으로 볼 수 없다.** 새로 초기화된 Classification Head가 학습되지 않은 상태로 저장되었을 가능성이 매우 높다.

Test 결과는 다음과 같다.

| 지표 | 결과 |
| --- | ---: |
| Subset Accuracy | 0.0000 |
| Micro F1 | 0.2037 |
| Macro F1 | 0.1324 |
| Weighted F1 | 0.3121 |
| Hamming Loss | 0.4827 |
| ROC-AUC Micro | 0.4966 |

ROC-AUC `0.4966`은 무작위 추정인 `0.5`와 비슷하다. Subset Accuracy도 `0`이며 Hamming Loss는 약 `48.3%`다.

이 결과는 모델 구조가 잘못되었다는 의미가 아니라, **학습하지 않은 분류 Head로 평가한 결과에 가깝다.**

### 확인 순서

1. Fine-tuning Cell을 실제로 실행한다.
2. Epoch별 Train Loss와 Validation 지표가 출력되는지 확인한다.
3. 가장 좋은 Validation 성능의 가중치를 저장한다.
4. 저장한 가중치를 새 모델에 불러온다.
5. 마지막에 한 번만 Test 데이터로 평가한다.

Test 데이터를 반복해서 보며 Hyperparameter를 조정하면 Test 정보가 학습 과정에 간접적으로 섞일 수 있다.

---

## 20. Hugging Face Pipeline

`pipeline()`은 다음 추론 과정을 하나의 고수준 API로 묶는다.

```text
문장
 ↓
Tokenizer
 ↓
Tensor
 ↓
Model
 ↓
Logits
 ↓
Sigmoid
 ↓
Label과 Score
```

대표적인 Task 이름은 다음과 같다.

| 작업 | Pipeline Task |
| --- | --- |
| 텍스트 분류 | `text-classification` |
| 감성 분석 | `sentiment-analysis` |
| 질의응답 | `question-answering` |
| 빈칸 채우기 | `fill-mask` |
| 텍스트 생성 | `text-generation` |
| 요약 | `summarization` |
| 번역 | `translation` |

### 멀티라벨 Pipeline 만들기

```python
from transformers import pipeline

pipe = pipeline(
    task="text-classification",
    model=loaded_model,
    tokenizer=tokenizer,
    device=DEVICE,
    truncation=True,
    max_length=MAX_LEN,
    function_to_apply="sigmoid",
)
```

모든 라벨의 Score를 받으려면 호출할 때 `top_k=None`을 전달한다.

```python
results = pipe(
    "오늘 날씨가 정말 좋다.",
    top_k=None,
)
```

> 원본 코드의 `tok_k=None`은 오타다. 올바른 인자 이름은 **`top_k=None`**이다. 오타 상태에서는 기본적으로 가장 높은 라벨 하나만 반환될 수 있다.

---

## 21. 라벨 이름과 Threshold 적용

```python
label_dict = {
    "LABEL_0": "출신차별",
    "LABEL_1": "외모차별",
    "LABEL_2": "정치성향차별",
    "LABEL_3": "혐오욕설",
    "LABEL_4": "연령차별",
    "LABEL_5": "성차별",
    "LABEL_6": "인종차별",
    "LABEL_7": "종교차별",
    "LABEL_8": "해당사항없음",
}

def prediction(text, threshold=0.5):
    results = pipe(text, top_k=None)

    selected = []

    for item in results:
        if item["score"] >= threshold:
            selected.append({
                "label": label_dict.get(
                    item["label"],
                    item["label"],
                ),
                "score": round(
                    float(item["score"]),
                    4,
                ),
            })

    return selected
```

Threshold `0.5`는 출발점일 뿐 항상 최선은 아니다.

- Threshold가 낮으면 더 많은 라벨을 선택해 Recall이 높아질 수 있다.
- Threshold가 높으면 선택을 엄격하게 해 Precision이 높아질 수 있다.
- 클래스별 데이터 비율이 다르면 라벨마다 다른 Threshold가 유리할 수 있다.

Test 데이터가 아니라 Validation 데이터에서 F1 등을 기준으로 Threshold를 선택해야 한다.

---

## 22. 현재 추론 결과의 문제

노트북의 현재 결과는 다음과 같다.

```text
"오늘 날씨가 정말 좋다."
→ 정치성향차별 0.5868

"어린 사람들은 다 예의가 없다고 생각해"
→ 인종차별 0.6535

"너희 나라로 가라"
→ 인종차별 0.6204
```

첫 번째 문장은 일반적인 문장인데 차별 표현으로 분류되었고, 두 번째 문장의 예측 라벨도 문맥과 맞지 않는다.

이는 앞서 확인한 무작위 수준의 평가 결과와 일치한다. Pipeline 코드가 실행되었다는 사실만으로 모델이 올바르게 학습되었다고 판단하면 안 된다.

```text
코드 실행 성공 ≠ 모델 학습 성공 ≠ 실제 활용 가능
```

---

## 23. 실습을 개선하는 방법

### Best Model 저장

매 Epoch Validation Micro F1 또는 Macro F1을 확인하고 가장 좋은 모델을 저장한다.

```python
best_f1 = -1.0

if valid_metrics["f1_macro"] > best_f1:
    best_f1 = valid_metrics["f1_macro"]
    torch.save(
        model.state_dict(),
        MODEL_PATH,
    )
```

### Threshold 조정

`0.5` 하나만 사용하지 말고 Validation 데이터에서 여러 값을 비교한다.

```text
0.2, 0.3, 0.4, 0.5, 0.6, 0.7
```

### 라벨별 성능 확인

전체 평균뿐 아니라 라벨마다 Precision, Recall, F1을 확인한다. 데이터가 적은 라벨에서 성능이 크게 낮을 수 있다.

### Class Imbalance 확인

K-MHaS의 라벨 빈도가 서로 다를 수 있으므로 각 라벨의 데이터 수를 먼저 확인한다. 필요하면 Loss 가중치나 Sampling 방법을 검토한다.

---

## 24. 실제 활용 시 주의점

혐오 표현 분류는 문맥과 사회적 배경에 민감하다. 모델 점수 하나만으로 게시물을 자동 삭제하거나 사용자를 제재하면 정상 문장을 잘못 차단할 수 있다.

다음 항목을 함께 고려해야 한다.

- False Positive와 False Negative 비용
- 인용, 풍자, 반어 표현
- 특정 집단에 대한 편향
- 신조어와 우회 표현의 변화
- 사람의 최종 검토 절차
- 예측 근거와 이의 제기 방법

실제 서비스에서는 모델을 최종 판단자가 아니라 검토 대상을 선별하는 보조 도구로 사용하는 편이 안전하다.

---

## 25. 전체 흐름

```text
K-MHaS TSV 파일
       ↓
문장과 라벨 불러오기
       ↓
라벨 문자열을 정수 리스트로 변환
       ↓
MultiLabelBinarizer
       ↓
9차원 Multi-hot Vector
       ↓
KLUE-BERT Tokenizer
       ↓
input_ids + attention_mask
       ↓
TensorDataset + DataLoader
       ↓
KLUE-BERT + Classification Head
       ↓
Full Fine-tuning
       ↓
Validation 지표와 Best Model 선택
       ↓
Test 평가
       ↓
Pipeline 추론 + Threshold 적용
```

---

## 26. 핵심 정리

1. PLM은 대규모 텍스트로 미리 학습한 뒤 특정 작업에 Fine-tuning해 사용한다.
2. BERT는 Transformer Encoder를 사용하며 MLM으로 양방향 문맥을 학습한다.
3. K-MHaS는 하나의 문장에 여러 혐오 표현 라벨을 지정할 수 있는 한국어 멀티라벨 데이터셋이다.
4. Multi-label Classification은 Softmax가 아니라 각 라벨에 독립적인 Sigmoid를 적용한다.
5. 라벨은 9차원 Multi-hot Vector로 변환하며 모든 데이터 구간에 같은 Encoder를 사용한다.
6. KLUE-BERT Tokenizer는 Special Token, Padding, Truncation과 Attention Mask를 처리한다.
7. 사전 학습 Checkpoint에 없던 Classification Head는 새로 초기화되므로 반드시 Fine-tuning해야 한다.
8. Warmup과 작은 Learning Rate는 사전 학습 가중치가 초기에 급격하게 변하는 것을 완화한다.
9. 멀티라벨 평가는 Subset Accuracy, Micro·Macro F1, Hamming Loss와 ROC-AUC를 함께 확인해야 한다.
10. 현재 노트북의 Fine-tuning Cell은 실행되지 않아 Test 결과를 학습된 모델의 성능으로 볼 수 없다.
11. Pipeline의 올바른 인자는 `tok_k`가 아니라 `top_k`다.
12. 분류 Threshold는 고정된 정답이 아니며 Validation 데이터에서 조정해야 한다.

