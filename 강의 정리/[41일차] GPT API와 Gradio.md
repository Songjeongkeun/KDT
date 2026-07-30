# [41일차] GPT API와 Gradio 정리

## 1. 생성형 AI API란?

생성형 AI API는 Python이나 JavaScript 같은 프로그램에서 AI 모델에 요청을 보내고 결과를 받아 사용할 수 있게 해주는 인터페이스다.

ChatGPT 웹 화면에서는 사용자가 직접 메시지를 입력한다. API를 사용하면 프로그램이 대신 요청을 보내고 응답을 받아 웹 서비스, 챗봇, 요약 도구 등에 활용할 수 있다.

```text
사용자
  │ 질문 입력
  ▼
Python 프로그램 또는 웹 서비스
  │ API 요청
  ▼
OpenAI API
  │ 모델이 응답 생성
  ▼
Python 프로그램 또는 웹 서비스
  │ 결과 출력
  ▼
사용자
```

API를 활용하면 다음과 같은 기능을 만들 수 있다.

- 질문에 답하는 챗봇
- 문서 요약 서비스
- 번역 서비스
- 리뷰 감정 분류
- 코드 설명 및 생성
- 데이터에서 필요한 정보 추출
- Gradio 기반 AI 웹 애플리케이션

---

## 2. 프롬프트 엔지니어링

프롬프트 엔지니어링은 AI 모델이 사용자의 의도를 정확하게 이해하고 원하는 결과를 생성하도록 입력 문장을 설계하는 작업이다.

같은 질문이라도 역할, 목적, 대상, 출력 형식을 얼마나 분명하게 제시하는지에 따라 응답 품질이 달라질 수 있다.

### 2.1 단순한 프롬프트

```text
FastAPI를 설명해줘.
```

질문의 범위가 넓기 때문에 답변의 난이도와 길이가 일정하지 않을 수 있다.

### 2.2 구체적인 프롬프트

```text
Python 기본 문법만 알고 있는 학습자에게 FastAPI를 설명해줘.
정의, 사용하는 이유, 간단한 실행 흐름 순서로 설명하고
전문 용어는 처음 등장할 때 뜻을 함께 적어줘.
```

두 번째 프롬프트에는 다음 정보가 들어 있다.

| 구성 요소 | 내용 |
|---|---|
| 대상 | Python 기본 문법만 알고 있는 학습자 |
| 주제 | FastAPI |
| 범위 | 정의, 사용 이유, 실행 흐름 |
| 제약 조건 | 전문 용어의 뜻을 함께 설명 |
| 출력 순서 | 설명할 순서를 지정 |

### 2.3 좋은 프롬프트의 기본 구조

프롬프트에는 다음 요소를 필요에 따라 포함할 수 있다.

```text
역할(Role)
누구의 관점과 말투로 답할지 지정한다.

작업(Task)
무엇을 해야 하는지 명확하게 작성한다.

맥락(Context)
왜 필요한지, 대상은 누구인지 설명한다.

제약 조건(Constraints)
길이, 말투, 포함하거나 제외할 내용을 정한다.

출력 형식(Output Format)
표, JSON, Markdown, 목록 등 결과 형식을 지정한다.

예시(Examples)
원하는 입력과 출력의 형태를 보여준다.
```

예시는 다음과 같다.

```text
역할: Python 입문자를 가르치는 선생님이다.
작업: FastAPI의 경로 매개변수를 설명한다.
대상: 함수와 딕셔너리까지 학습한 사람이다.
제약: 어려운 용어는 쉽게 풀어 쓰고 500자 이내로 작성한다.
형식: 개념, 코드, 실행 결과 순서로 작성한다.
```

프롬프트는 무조건 길게 작성하는 것이 좋은 것은 아니다. 필요한 정보를 빠뜨리지 않으면서 모순 없이 명확하게 작성하는 것이 중요하다.

---

## 3. 메시지 역할

AI 모델에 여러 메시지를 전달할 때 각 메시지에 역할을 지정할 수 있다.

| 역할 | 의미 |
|---|---|
| `system` | 모델의 전체적인 행동, 관점, 말투를 설정한다. |
| `developer` | 애플리케이션 개발자가 정한 규칙과 업무 지침을 전달한다. |
| `user` | 실제 사용자의 질문이나 요청을 전달한다. |
| `assistant` | 모델이 이전에 생성한 응답을 나타낸다. |

노트북 예제는 `system`과 `user` 역할을 사용한다.

```python
messages = [
    {
        "role": "system",
        "content": "당신은 초등학교 선생님입니다.",
    },
    {
        "role": "user",
        "content": "FastAPI가 뭐예요?",
    },
]
```

이 프롬프트는 모델에게 다음과 같이 전달된다.

```text
모델의 역할
초등학교 선생님

사용자의 질문
FastAPI가 무엇인지 설명

예상되는 응답
어린 학습자가 이해할 수 있는 쉬운 표현
```

현재 Responses API에서는 높은 수준의 지침을 `instructions` 매개변수나 `developer` 역할로 전달할 수도 있다.

```python
response = client.responses.create(
    model="사용할_모델_ID",
    instructions="초등학생도 이해할 수 있는 쉬운 말로 설명하세요.",
    input="FastAPI가 무엇인지 설명해 주세요.",
)
```

메시지 배열을 사용한다면 다음과 같이 작성할 수 있다.

```python
messages = [
    {
        "role": "developer",
        "content": "초등학생도 이해할 수 있는 쉬운 말로 설명하세요.",
    },
    {
        "role": "user",
        "content": "FastAPI가 무엇인지 설명해 주세요.",
    },
]
```

`assistant` 역할은 대화 기록을 직접 구성할 때 사용할 수 있다.

```python
messages = [
    {"role": "user", "content": "제 이름은 송정근입니다."},
    {"role": "assistant", "content": "안녕하세요, 송정근님."},
    {"role": "user", "content": "제 이름이 무엇이었나요?"},
]
```

단, 여러 번의 API 요청 사이에서 모델이 이전 대화를 자동으로 기억한다고 가정하면 안 된다. 이전 메시지를 다시 전달하거나 Responses API의 대화 상태 관리 기능을 사용해야 한다.

---

## 4. 토큰

토큰은 AI 모델이 텍스트를 처리하는 작은 단위다. 토큰 하나가 항상 단어 하나와 일치하는 것은 아니다.

토큰은 다음과 같은 형태가 될 수 있다.

- 하나의 짧은 단어
- 긴 단어의 일부
- 숫자
- 공백
- 문장 부호
- 한글 음절 또는 단어의 일부

```text
사용자가 입력한 문장
        ↓
여러 개의 토큰으로 분리
        ↓
모델이 토큰 단위로 내용을 처리
        ↓
다음에 올 토큰을 생성
        ↓
완성된 응답 반환
```

토큰은 다음 항목에 영향을 준다.

- API 사용 비용
- 모델이 한 번에 처리할 수 있는 문맥의 크기
- 생성 가능한 답변의 최대 길이
- 요청과 응답 처리 시간

---

## 5. API 비용의 기본 구조

API 비용은 일반적으로 처리한 토큰 수와 사용한 모델에 따라 달라진다.

| 항목 | 의미 |
|---|---|
| Input | API에 새롭게 전달한 입력 토큰 |
| Cached input | 이전 입력의 동일한 앞부분이 캐시되어 재사용된 토큰 |
| Cache writes | 새로운 입력을 캐시에 저장하는 과정에서 계산되는 항목 |
| Output | 모델이 생성한 출력 토큰 |

### 5.1 Input

사용자가 보낸 질문, 역할 지침, 대화 기록 등이 입력 토큰에 포함된다.

```python
response = client.responses.create(
    model="사용할_모델_ID",
    input="안녕하세요?",
)
```

`안녕하세요?`가 입력에 해당한다.

### 5.2 Output

모델이 생성한 답변이 출력에 해당한다.

```text
안녕하세요. 무엇을 도와드릴까요?
```

### 5.3 Cached input

여러 요청에서 긴 입력의 앞부분이 반복되면 지원되는 모델과 조건에서 프롬프트 캐시가 적용될 수 있다.

```text
공통 지침
"당신은 Python 선생님입니다.
답변은 개념, 코드, 결과 순서로 작성하세요."

질문 1
"리스트를 설명해 주세요."

질문 2
"딕셔너리를 설명해 주세요."
```

공통 지침처럼 동일하게 반복되는 앞부분은 캐시의 대상이 될 수 있다. 다만 같은 문장을 보냈다고 해서 모든 요청에서 항상 캐시가 적용된다고 단정할 수는 없다. 적용 조건과 가격은 모델 및 API 정책에 따라 달라질 수 있다.

### 5.4 모델 선택

모델마다 품질, 처리 속도, 비용, 지원 기능이 다르다.

| 선택 기준 | 적합한 작업 |
|---|---|
| 높은 추론 성능 | 복잡한 코드 분석, 어려운 문제 해결 |
| 성능과 비용의 균형 | 일반적인 API 서비스, 코드 설명 |
| 빠른 응답과 낮은 비용 | 분류, 간단한 요약, 대량 처리 |

모델 이름과 가격은 바뀔 수 있으므로 블로그에 고정된 가격표를 복사하기보다 공식 모델 목록과 가격 페이지를 함께 확인하는 것이 안전하다.

---

## 6. 개발 환경 준비

필요한 패키지는 다음과 같이 설치한다.

```bash
python -m pip install openai python-dotenv gradio
```

각 패키지의 역할은 다음과 같다.

| 패키지 | 역할 |
|---|---|
| `openai` | Python에서 OpenAI API를 호출한다. |
| `python-dotenv` | `.env` 파일의 값을 환경변수로 불러온다. |
| `gradio` | Python 함수에 웹 사용자 인터페이스를 연결한다. |

현재 노트북 실행 환경에서는 다음 버전이 확인되었다.

```text
openai 2.48.0
gradio 6.20.0
```

라이브러리 버전에 따라 일부 매개변수나 동작이 달라질 수 있으므로 코드가 실행되지 않으면 설치된 버전과 공식 문서를 함께 확인한다.

---

## 7. API 키 관리

API 키는 OpenAI API 요청을 보낸 사용자를 인증하는 비밀값이다. 비밀번호처럼 다뤄야 하며 코드에 직접 작성하거나 GitHub에 올리면 안 된다.

### 7.1 `.env` 파일

프로젝트 폴더에 `.env` 파일을 만들고 다음처럼 작성한다.

```dotenv
OPENAI_API_KEY=발급받은_API_키
```

실제 키를 따옴표 없이 작성할 수 있다. 블로그, 화면 캡처, 저장소에는 실제 값을 공개하지 않는다.

### 7.2 `.gitignore`

`.env` 파일이 Git에 올라가지 않도록 `.gitignore`에 등록한다.

```gitignore
.env
```

가상환경과 Python 캐시도 함께 제외할 수 있다.

```gitignore
.env
.venv/
venv/
__pycache__/
```

### 7.3 환경변수 불러오기

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ["OPENAI_API_KEY"]
```

코드 실행 순서는 다음과 같다.

```text
.env 파일
  ↓ load_dotenv()
운영체제 환경변수로 등록
  ↓ os.environ["OPENAI_API_KEY"]
Python 코드에서 API 키 사용
```

`os.environ[...]`은 해당 환경변수가 없으면 `KeyError`를 발생시킨다.

```python
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY가 설정되지 않았다.")
```

`os.getenv()`는 값이 없을 때 `None`을 반환하므로 오류 메시지를 직접 작성할 수 있다.

---

## 8. OpenAI 클라이언트 생성

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
```

OpenAI Python SDK는 기본적으로 `OPENAI_API_KEY` 환경변수를 읽는다. 따라서 키를 명시적으로 전달하지 않아도 된다.

다음처럼 직접 전달할 수도 있다.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)
```

두 방식 모두 가능하지만, 환경변수의 기본 이름을 그대로 사용한다면 `OpenAI()`가 더 간결하다.

---

## 9. Responses API

Responses API는 모델에 입력을 전달하고 생성된 응답을 받는 API다.

가장 간단한 요청은 다음과 같다.

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="사용할_모델_ID",
    input="안녕하세요?",
)

print(response.output_text)
```

주요 매개변수는 다음과 같다.

| 매개변수 | 역할 |
|---|---|
| `model` | 요청을 처리할 모델을 선택한다. |
| `input` | 모델에 전달할 문자열 또는 메시지 목록이다. |
| `instructions` | 모델의 행동, 말투, 목표에 대한 상위 지침이다. |
| `max_output_tokens` | 응답 생성에 사용할 최대 출력 토큰 수다. |
| `temperature` | 지원하는 모델에서 응답의 무작위성을 조절한다. |

### 9.1 문자열 입력

사용자 메시지 하나만 전달한다면 문자열을 바로 사용할 수 있다.

```python
response = client.responses.create(
    model="사용할_모델_ID",
    input="FastAPI가 무엇인지 설명해 주세요.",
)
```

문자열 입력은 일반적인 사용자 입력으로 처리된다.

### 9.2 메시지 목록 입력

역할을 나눠 전달하려면 메시지 목록을 사용한다.

```python
messages = [
    {
        "role": "system",
        "content": "당신은 초등학교 선생님입니다.",
    },
    {
        "role": "user",
        "content": "FastAPI가 뭐예요?",
    },
]

response = client.responses.create(
    model="gpt-5-nano",
    input=messages,
)
```

---

## 10. 응답 객체

`client.responses.create()`는 단순 문자열이 아니라 여러 정보를 담은 응답 객체를 반환한다.

주요 속성은 다음과 같다.

| 속성 | 의미 |
|---|---|
| `id` | 응답을 식별하는 고유 ID |
| `model` | 실제 응답을 생성한 모델 |
| `status` | 응답 처리 상태 |
| `output` | 메시지, 추론 정보, 도구 호출 등이 담긴 결과 목록 |
| `output_text` | 텍스트 출력만 합쳐서 제공하는 편의 속성 |
| `usage` | 입력·출력 토큰 사용량 |
| `incomplete_details` | 응답이 중간에 종료된 원인 |

전체 객체를 출력하면 내부 정보가 매우 많이 표시된다.

```python
print(response)
```

일반적인 텍스트 응답만 필요하다면 다음처럼 작성하는 것이 가장 간단하다.

```python
print(response.output_text)
```

---

## 11. 텍스트 응답 안전하게 가져오기

노트북에서는 다음처럼 고정된 인덱스로 텍스트에 접근한다.

```python
response.output[1].content[0].text
```

하지만 `response.output`에는 텍스트 메시지 외에도 추론 정보나 도구 호출 결과가 포함될 수 있다. 따라서 텍스트가 항상 `output[1]`에 있다고 가정하면 안전하지 않다.

OpenAI SDK가 제공하는 다음 속성을 우선 사용하는 것이 간단하다.

```python
text = response.output_text
print(text)
```

직접 출력 항목을 검사하려면 다음과 같이 작성할 수 있다.

```python
def get_response_text(response):
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    return content.text

    return None
```

```python
text = get_response_text(response)
print(text)
```

이 함수의 처리 과정은 다음과 같다.

```text
response.output 순회
        ↓
type이 message인지 확인
        ↓
message의 content 순회
        ↓
type이 output_text인지 확인
        ↓
text 반환
```

단순 텍스트 요청에서는 `response.output_text`를 사용하고, 출력 항목을 세부적으로 구분해야 할 때 직접 순회하는 방식이 적합하다.

---

## 12. `max_output_tokens`

`max_output_tokens`는 모델이 응답 생성에 사용할 수 있는 최대 출력 토큰 수를 제한한다.

```python
response = client.responses.create(
    model="gpt-5-nano",
    input="안녕하세요.",
    max_output_tokens=30,
)
```

출력 토큰을 제한하는 이유는 다음과 같다.

- 답변이 지나치게 길어지는 것을 막는다.
- 요청당 최대 비용을 어느 정도 제어한다.
- 짧은 분류나 추출 작업에서 불필요한 출력을 줄인다.
- 응답 시간을 줄이는 데 도움이 될 수 있다.

출력 한도를 너무 작게 설정하면 답변이 끝나기 전에 중단될 수 있다. 추론 모델에서는 내부 추론에도 출력 토큰 예산이 사용될 수 있으므로 화면에 보이는 답변이 거의 생성되지 않을 수도 있다.

```python
print(response.status)
print(response.incomplete_details)
```

예상 결과는 다음과 같다.

```text
incomplete
IncompleteDetails(reason='max_output_tokens')
```

이 경우 다음 방법을 고려할 수 있다.

- `max_output_tokens` 값을 높인다.
- 프롬프트에서 짧은 형식을 요구한다.
- 작업을 여러 단계로 나눈다.
- 사용 목적에 맞는 모델을 선택한다.

---

## 13. 응답 상태

`response.status`를 확인하면 응답이 정상적으로 완료되었는지 알 수 있다.

| 상태 | 의미 |
|---|---|
| `completed` | 응답 생성이 정상적으로 완료되었다. |
| `incomplete` | 응답을 끝까지 만들지 못하고 중간에 종료되었다. |
| `failed` | 오류로 인해 응답 생성에 실패했다. |
| `queued` | 처리 대기열에서 기다리는 중이다. |
| `in_progress` | 현재 응답을 생성하고 있다. |
| `cancelled` | 요청이 취소되었다. |

일반적인 동기 요청에서는 요청 함수가 결과를 반환한 시점에 `completed`, `incomplete`, `failed` 상태를 주로 확인하게 된다. 백그라운드 작업에서는 `queued`나 `in_progress` 상태도 볼 수 있다.

```python
if response.status == "completed":
    print(response.output_text)
elif response.status == "incomplete":
    print("응답이 중간에 종료되었다.")
    print(response.incomplete_details)
else:
    print("응답 생성에 실패했거나 완료되지 않았다.")
```

---

## 14. `incomplete_details`

응답이 `incomplete` 상태라면 `incomplete_details`에서 중단 원인을 확인할 수 있다.

```python
print(response.incomplete_details)
```

출력 예시는 다음과 같다.

```text
IncompleteDetails(reason='max_output_tokens')
```

이 결과는 출력 토큰 제한 때문에 응답 생성이 끝나기 전에 중단되었다는 뜻이다.

상태만 확인하는 것보다 중단 이유까지 함께 확인해야 문제를 정확하게 해결할 수 있다.

---

## 15. `temperature`

`temperature`는 지원하는 모델에서 다음 토큰을 선택할 때의 무작위성을 조절하는 값이다.

```python
response = client.responses.create(
    model="gpt-4.1-nano",
    input="안녕하세요.",
    temperature=0,
)
```

일반적인 경향은 다음과 같다.

| 값 | 경향 | 활용 예시 |
|---|---|---|
| 낮은 값 | 답변이 비교적 일관되고 보수적이다. | 분류, 정보 추출, 정해진 형식 |
| 높은 값 | 답변이 다양하고 창의적으로 달라질 수 있다. | 아이디어 생성, 창작 |

`temperature=0`이라고 해서 실행할 때마다 글자 하나까지 완전히 같은 결과가 반드시 보장되는 것은 아니다. 또한 일부 추론 모델은 `temperature`를 지원하지 않거나 다른 설정 방식을 사용할 수 있으므로 선택한 모델의 매개변수 지원 여부를 확인해야 한다.

---

## 16. 토큰 사용량 확인

응답 객체의 `usage` 속성에서 사용한 토큰 정보를 확인할 수 있다.

```python
print(response.usage)
```

세부 속성은 SDK와 모델에 따라 달라질 수 있지만 다음과 같은 정보를 포함한다.

```text
input_tokens
입력에 사용된 토큰 수

output_tokens
출력 생성에 사용된 토큰 수

total_tokens
입력과 출력의 전체 토큰 수

cached_tokens
캐시가 적용된 입력 토큰 수

reasoning_tokens
추론 과정에 사용된 토큰 수
```

사용량을 확인하면 예상보다 긴 프롬프트나 불필요하게 긴 응답을 찾아 비용과 처리 시간을 개선할 수 있다.

---

## 17. 기본 API 호출 코드 정리

노트북의 내용을 기준으로 안전하게 정리한 기본 코드는 다음과 같다.

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "당신은 초등학교 선생님입니다.",
    },
    {
        "role": "user",
        "content": "FastAPI가 뭐예요?",
    },
]

response = client.responses.create(
    model="gpt-5-nano",
    input=messages,
)

if response.status == "completed":
    print(response.output_text)
else:
    print("응답 상태:", response.status)
    print("세부 정보:", response.incomplete_details)
```

실행 흐름은 다음과 같다.

```text
.env에서 API 키 로드
        ↓
OpenAI 클라이언트 생성
        ↓
역할별 메시지 작성
        ↓
Responses API 요청
        ↓
응답 상태 확인
        ↓
output_text 출력
```

---

## 18. Gradio란?

Gradio는 Python 함수에 웹 사용자 인터페이스를 연결할 수 있는 라이브러리다.

HTML, CSS, JavaScript를 직접 작성하지 않아도 입력창, 버튼, 체크박스, 드롭다운 같은 화면을 만들 수 있다.

```text
웹 화면의 입력 컴포넌트
        ↓
Gradio 이벤트
        ↓
Python 함수 실행
        ↓
함수의 반환값
        ↓
웹 화면의 출력 컴포넌트
```

Gradio는 다음 상황에서 유용하다.

- 머신러닝 모델을 빠르게 테스트할 때
- GPT API의 입력과 출력을 웹 화면으로 확인할 때
- 데이터 처리 함수를 시각적으로 실행할 때
- 프로젝트의 간단한 프로토타입을 만들 때
- 다른 사람에게 모델의 동작을 시연할 때

---

## 19. Gradio 설치와 실행

```bash
python -m pip install gradio
```

Python 코드에서는 다음과 같이 불러온다.

```python
import gradio as gr
```

Gradio 앱은 일반적으로 `launch()`로 실행한다.

```python
demo.launch()
```

실행 결과 예시는 다음과 같다.

```text
Running on local URL: http://127.0.0.1:7860
```

브라우저에서 해당 주소에 접속하면 Gradio 화면을 볼 수 있다. 이미 포트가 사용 중이면 `7861`, `7862`처럼 다른 포트가 선택될 수 있다.

---

## 20. `Blocks`와 `Interface`

Gradio에서는 `Blocks`와 `Interface`를 주로 사용한다.

| 구분 | `Blocks` | `Interface` |
|---|---|---|
| 목적 | 자유로운 화면 구성 | 함수 하나를 빠르게 웹 화면으로 변환 |
| 레이아웃 | 세밀하게 구성 가능 | 기본 레이아웃 자동 생성 |
| 이벤트 | 직접 연결 | 기본 제출 동작 자동 연결 |
| 적합한 경우 | 여러 컴포넌트와 복잡한 흐름 | 간단한 모델 또는 함수 테스트 |

### 20.1 `Blocks`

```python
with gr.Blocks() as demo:
    gr.Markdown("# 안녕하세요 Gradio!")

demo.launch()
```

`with gr.Blocks() as demo:` 블록 안에 작성한 컴포넌트가 하나의 웹 화면을 구성한다.

### 20.2 `Interface`

```python
def add(num1, num2):
    return num1 + num2


interface = gr.Interface(
    fn=add,
    inputs=["number", "number"],
    outputs="number",
    title="계산기",
    description="숫자 두 개를 입력하세요.",
    flagging_mode="never",
)

interface.launch()
```

`Interface`는 함수, 입력 컴포넌트, 출력 컴포넌트를 지정하면 제출 버튼이 있는 기본 화면을 자동으로 만든다.

---

## 21. Markdown 컴포넌트

`gr.Markdown()`은 화면에 제목, 설명, 목록 등을 표시한다.

```python
import gradio as gr


with gr.Blocks() as demo:
    gr.Markdown("# 안녕하세요 Gradio!")
    gr.Markdown("### 작은 제목을 입력합니다")
    gr.Markdown(
        "- 첫 번째 아이템\n"
        "- 두 번째 아이템\n"
        "- 세 번째 아이템"
    )

demo.launch()
```

Markdown 문자열 안에서 `\n`은 줄바꿈을 의미한다.

---

## 22. Textbox와 `submit` 이벤트

텍스트 입력값을 Python 함수로 전달하고 반환값을 출력창에 표시할 수 있다.

```python
def handle_input(text):
    return text


with gr.Blocks() as demo:
    text_input = gr.Textbox(
        label="문자 입력",
        lines=1,
    )

    output_text = gr.Textbox(
        label="출력",
    )

    text_input.submit(
        fn=handle_input,
        inputs=text_input,
        outputs=output_text,
    )

demo.launch()
```

실행 흐름은 다음과 같다.

```text
사용자가 Textbox에 문자 입력
        ↓
Enter를 눌러 submit 이벤트 발생
        ↓
handle_input(입력값) 실행
        ↓
함수의 반환값
        ↓
output_text에 표시
```

이벤트 연결의 공통 구조는 다음과 같다.

```python
컴포넌트.이벤트(
    fn=실행할_함수,
    inputs=입력_컴포넌트,
    outputs=출력_컴포넌트,
)
```

---

## 23. Checkbox와 `change` 이벤트

Checkbox는 선택 상태를 `True` 또는 `False`로 전달한다.

```python
def handle_checkbox(selected):
    if selected:
        return "동의했습니다."

    return "동의하지 않았습니다."


with gr.Blocks() as demo:
    checkbox = gr.Checkbox(
        label="개인정보 사용에 동의하겠습니까?",
    )

    output_checkbox = gr.Textbox(
        label="출력",
    )

    checkbox.change(
        fn=handle_checkbox,
        inputs=checkbox,
        outputs=output_checkbox,
    )

demo.launch()
```

실행 결과는 다음과 같다.

```text
체크됨
selected == True
→ "동의했습니다."

체크 해제
selected == False
→ "동의하지 않았습니다."
```

`change` 이벤트는 컴포넌트의 값이 바뀔 때 실행된다.

---

## 24. Dropdown과 `change` 이벤트

Dropdown은 여러 선택지 중 하나를 고르게 한다.

```python
def handle_fruit(fruit):
    return f"선택한 과일: {fruit}"


with gr.Blocks() as demo:
    fruit_dropdown = gr.Dropdown(
        label="과일",
        choices=["사과", "오렌지", "바나나", "메론"],
    )

    output_fruit = gr.Textbox(
        label="구입한 과일",
    )

    fruit_dropdown.change(
        fn=handle_fruit,
        inputs=fruit_dropdown,
        outputs=output_fruit,
    )

demo.launch()
```

`오렌지`를 선택하면 다음 결과가 표시된다.

```text
선택한 과일: 오렌지
```

처리 과정은 다음과 같다.

```text
Dropdown에서 "오렌지" 선택
        ↓
handle_fruit("오렌지")
        ↓
"선택한 과일: 오렌지" 반환
        ↓
Textbox에 출력
```

---

## 25. 숫자 계산기

`gr.Interface`를 사용하면 두 숫자를 더하는 함수를 빠르게 웹 화면으로 만들 수 있다.

```python
def add(num1, num2):
    return num1 + num2


interface = gr.Interface(
    fn=add,
    inputs=["number", "number"],
    outputs="number",
    title="계산기",
    description="숫자 두 개를 입력하세요.",
    flagging_mode="never",
)

interface.launch()
```

각 설정의 의미는 다음과 같다.

| 설정 | 의미 |
|---|---|
| `fn=add` | 입력값을 전달할 Python 함수 |
| `inputs` | 함수에 전달할 입력 컴포넌트 |
| `outputs` | 함수의 반환값을 표시할 컴포넌트 |
| `title` | 화면 상단 제목 |
| `description` | 화면 설명 |
| `flagging_mode="never"` | 결과 신고 기능을 표시하지 않음 |

입력과 함수 매개변수는 순서대로 연결된다.

```text
첫 번째 number → num1
두 번째 number → num2
add(num1, num2)의 반환값 → output number
```

---

## 26. Radio 컴포넌트

Radio는 여러 선택지 중 하나만 선택할 때 사용한다.

```python
def favorite_language(language):
    messages = {
        "Python": "데이터 과학, 웹 개발, AI에 적합한 언어",
        "JavaScript": "프론트엔드와 백엔드에서 사용할 수 있는 언어",
        "Java": "대규모 시스템 개발에 널리 사용되는 언어",
        "C++": "고성능 애플리케이션과 게임 개발에 사용되는 언어",
    }

    return messages.get(
        language,
        "선택된 언어에 대한 정보가 없음",
    )


interface = gr.Interface(
    fn=favorite_language,
    inputs=gr.Radio(
        ["Python", "JavaScript", "Java", "C++"],
        label="좋아하는 언어",
    ),
    outputs="text",
    title="좋아하는 언어",
    description="라디오 버튼에서 언어를 선택하세요.",
)

interface.launch()
```

`Python`을 선택하면 다음 값이 함수에 전달된다.

```python
favorite_language("Python")
```

출력 결과는 다음과 같다.

```text
데이터 과학, 웹 개발, AI에 적합한 언어
```

---

## 27. `submit`과 `change` 비교

| 이벤트 | 실행 시점 | 예시 |
|---|---|---|
| `submit` | 입력을 제출할 때 | Textbox에서 Enter 입력 |
| `change` | 컴포넌트의 값이 바뀔 때 | Checkbox, Dropdown 값 변경 |
| `click` | 버튼을 클릭할 때 | 실행 버튼 |

버튼을 사용하면 다음과 같이 연결할 수 있다.

```python
def greet(name):
    return f"{name}님, 안녕하세요."


with gr.Blocks() as demo:
    name_input = gr.Textbox(label="이름")
    submit_button = gr.Button("인사하기")
    result = gr.Textbox(label="결과")

    submit_button.click(
        fn=greet,
        inputs=name_input,
        outputs=result,
    )

demo.launch()
```

---

## 28. API 예외 처리 추가

네트워크 문제, 인증 실패, 요청 제한 등이 발생할 수 있으므로 실제 애플리케이션에서는 예외 처리를 추가하는 것이 좋다.

```python
from openai import (
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
)


def ask_gpt(question):
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=question,
            max_output_tokens=500,
        )

        if response.status == "completed":
            return response.output_text

        return f"응답 상태: {response.status}"

    except AuthenticationError:
        return "API 키를 확인해 주세요."

    except RateLimitError:
        return "요청이 너무 많습니다. 잠시 후 다시 시도해 주세요."

    except APIConnectionError:
        return "OpenAI 서버에 연결할 수 없습니다."

    except Exception as error:
        print(error)
        return "요청 처리 중 오류가 발생했습니다."
```

사용자 화면에는 이해하기 쉬운 메시지를 보여주고, 개발자가 확인할 구체적인 오류는 서버의 로그에 기록하는 방식이 좋다.

---

## 29. Gradio 실행 옵션

### 29.1 브라우저 자동 열기

```python
demo.launch(inbrowser=True)
```

앱 실행 시 기본 브라우저를 자동으로 연다.

### 29.2 포트 지정

```python
demo.launch(server_port=7860)
```

특정 포트를 지정한다. 해당 포트가 이미 사용 중이면 실행에 실패할 수 있다.

### 29.3 외부 접속 허용

```python
demo.launch(server_name="0.0.0.0")
```

같은 네트워크의 다른 기기에서 접근할 수 있게 한다. 방화벽과 네트워크 설정을 함께 확인해야 한다.

### 29.4 공유 링크

```python
demo.launch(share=True)
```

외부에서 접속할 수 있는 임시 공유 링크를 만들 수 있다. 개인 데이터나 API 키가 노출될 수 있는 화면은 공개하지 않도록 주의한다.

---

## 30. API 키 보안

API 키는 다음 원칙에 따라 관리한다.

- Python 코드에 API 키를 직접 작성하지 않는다.
- HTML이나 브라우저 JavaScript에 API 키를 넣지 않는다.
- `.env`를 `.gitignore`에 등록한다.
- 노트북 출력이나 화면 캡처에 키가 보이지 않는지 확인한다.
- 실수로 GitHub에 올렸다면 파일만 삭제하지 말고 해당 키를 폐기하고 새로 발급한다.
- 공개된 Gradio 앱에서는 요청 횟수 제한과 인증을 고려한다.
- 오류 메시지에 API 키나 민감한 환경변수를 출력하지 않는다.

다음과 같은 코드는 사용하지 않는다.

```python
client = OpenAI(
    api_key="실제_API_키",
)
```

다음처럼 환경변수를 사용한다.

```python
client = OpenAI()
```

---

## 31. 핵심 정리

- 프롬프트 엔지니어링은 AI가 원하는 결과를 생성하도록 역할, 작업, 맥락, 제약, 출력 형식을 설계하는 작업이다.
- API 요청과 응답은 토큰 단위로 처리되며 모델과 토큰 사용량에 따라 비용이 달라진다.
- API 키는 `.env`에 저장하고 GitHub나 브라우저 코드에 노출하지 않는다.
- OpenAI Python SDK는 `OPENAI_API_KEY` 환경변수를 자동으로 읽을 수 있다.
- Responses API는 `client.responses.create()`로 호출하며 입력은 `input`에 전달한다.
- 단순 텍스트 결과는 `response.output_text`로 가져오는 것이 편리하다.
- `response.status`와 `response.incomplete_details`를 확인하면 응답 완료 여부와 중단 이유를 알 수 있다.
- `max_output_tokens`가 너무 작으면 응답이 `incomplete` 상태로 끝날 수 있다.
- `temperature`는 지원하는 모델에서 응답의 무작위성을 조절하지만 완전히 동일한 출력을 보장하지는 않는다.
- Gradio는 Python 함수를 웹 입력·출력 컴포넌트와 연결한다.
- `Blocks`는 자유로운 화면과 이벤트 구성이 필요할 때 사용한다.
- `Interface`는 하나의 함수를 빠르게 웹 화면으로 만들 때 사용한다.
- `submit`, `change`, `click` 이벤트를 통해 사용자의 행동과 Python 함수를 연결한다.

이번 내용의 핵심은 OpenAI API와 Gradio를 각각 외우는 것이 아니다. **사용자의 입력이 Gradio 컴포넌트에서 Python 함수로 전달되고, 함수가 OpenAI API를 호출한 뒤 반환한 결과가 다시 웹 화면에 표시되는 전체 흐름을 이해하는 것**이다.
