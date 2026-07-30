# [40일차] FastAPI 기초 정리

## 1. FastAPI란?

FastAPI는 Python으로 웹 API를 만들기 위한 웹 프레임워크다. Python의 타입 힌트를 적극적으로 사용하며, 작성한 코드에서 요청 데이터의 형식을 검사하고 API 문서를 자동으로 생성한다.

FastAPI의 주요 특징은 다음과 같다.

- Python 문법과 타입 힌트를 사용해 API를 작성한다.
- 경로 매개변수, 쿼리 매개변수, 요청 본문을 자동으로 구분한다.
- 잘못된 요청 데이터가 들어오면 자동으로 유효성을 검사한다.
- 딕셔너리나 Pydantic 모델을 JSON 응답으로 변환한다.
- Swagger UI와 ReDoc 형식의 API 문서를 자동으로 제공한다.
- `async def`를 이용한 비동기 요청 처리를 지원한다.
- Uvicorn과 같은 ASGI 서버에서 실행한다.

FastAPI는 API 서버를 만드는 데 주로 사용하지만, Jinja2 템플릿과 정적 파일을 연결하면 HTML 페이지도 함께 제공할 수 있다.

---

## 2. 웹 서비스의 기본 구조

웹 서비스는 일반적으로 클라이언트와 서버가 요청과 응답을 주고받는 구조로 동작한다.

```text
클라이언트
브라우저, 모바일 앱, React 등
        │
        │ HTTP 요청
        ▼
FastAPI 서버
요청 분석 → 함수 실행 → 데이터 처리
        │
        │ HTTP 응답
        ▼
클라이언트
HTML 또는 JSON 결과 사용
```

예를 들어 브라우저가 `/api/data`로 `GET` 요청을 보내면 FastAPI는 해당 경로에 연결된 함수를 실행하고 JSON 데이터를 응답한다.

```python
@app.get("/api/data")
async def get_data():
    return {"message": "FastAPI에서 보내는 데이터입니다"}
```

응답은 다음과 같다.

```json
{
  "message": "FastAPI에서 보내는 데이터입니다"
}
```

---

## 3. 타입 힌트

타입 힌트는 변수, 매개변수, 반환값에 어떤 자료형을 사용할지 표시하는 문법이다.

```python
def add(a: int, b: int) -> int:
    return a + b
```

타입 힌트는 자료형을 설명하는 역할만 하는 경우도 있지만, FastAPI에서는 요청 데이터를 분석하고 검증하는 데 직접 사용한다.

```python
@app.get("/users/{id}")
def find_user(id: int):
    return {"id": id}
```

`id: int`라고 작성했기 때문에 FastAPI는 URL에 전달된 값을 정수로 변환한다.

```text
GET /users/10
```

```json
{
  "id": 10
}
```

정수로 바꿀 수 없는 값이 들어오면 함수가 실행되기 전에 FastAPI가 요청을 거절한다.

```text
GET /users/apple
```

```text
422 Unprocessable Entity
```

즉, 타입 힌트는 다음 역할을 한다.

- 코드에서 사용할 자료형을 명확하게 보여준다.
- 에디터의 자동 완성과 오류 검사를 돕는다.
- FastAPI가 요청 데이터를 자동으로 변환하게 한다.
- 잘못된 요청 데이터가 함수 내부까지 들어오는 것을 막는다.
- 자동 API 문서에 매개변수의 자료형을 표시한다.

---

## 4. ASGI와 Uvicorn

### 4.1 ASGI

ASGI는 **Asynchronous Server Gateway Interface**의 약자다. Python 웹 서버와 웹 애플리케이션이 통신하는 규칙이다.

FastAPI 애플리케이션만 작성해서는 외부의 HTTP 요청을 직접 받을 수 없다. Uvicorn과 같은 ASGI 서버가 네트워크 요청을 받은 뒤 FastAPI 애플리케이션에 전달한다.

```text
브라우저
  │
  │ HTTP 요청
  ▼
Uvicorn
  │ ASGI 규칙에 따라 전달
  ▼
FastAPI 애플리케이션
  │ 처리 결과 반환
  ▼
Uvicorn
  │ HTTP 응답
  ▼
브라우저
```

ASGI는 비동기 처리와 WebSocket처럼 연결을 오래 유지하는 통신을 지원한다. 다만 WSGI가 항상 느리고 ASGI가 항상 빠르다는 뜻은 아니다. 네트워크나 파일 입출력을 기다리는 요청이 많을 때 ASGI의 비동기 처리 방식이 특히 유용하다.

### 4.2 Uvicorn

Uvicorn은 FastAPI 애플리케이션을 실행하는 ASGI 서버다.

```bash
python -m pip install fastapi
python -m pip install "uvicorn[standard]"
```

HTML 템플릿을 사용하려면 Jinja2도 필요하다.

```bash
python -m pip install jinja2
```

한 번에 설치할 수도 있다.

```bash
python -m pip install fastapi "uvicorn[standard]" jinja2
```

`uvicorn[standard]`는 기본 Uvicorn에 자동 리로드, 성능, WebSocket 처리 등에 사용되는 선택 의존성을 함께 설치한다. CORS나 GZip 같은 FastAPI 미들웨어를 자동으로 설정하는 패키지는 아니므로 필요한 미들웨어는 애플리케이션에서 별도로 등록해야 한다.

---

## 5. 프로젝트 구조

예제는 다음 구조로 작성되어 있다.

```text
1_PYTHON
├── fastapi_main.py
├── static
│   └── script.js
└── templates
    └── index.html
```

각 파일의 역할은 다음과 같다.

| 파일 | 역할 |
|---|---|
| `fastapi_main.py` | FastAPI 객체와 API 경로를 정의한다. |
| `templates/index.html` | 브라우저에 보여줄 HTML 문서다. |
| `static/script.js` | `/api/data`에 요청을 보내고 결과를 화면에 출력한다. |

Uvicorn은 파일이 있는 디렉터리에서 실행하는 것이 좋다. `StaticFiles(directory="static")`와 `Jinja2Templates(directory="templates")`가 현재 작업 디렉터리를 기준으로 폴더를 찾기 때문이다.

---

## 6. FastAPI 애플리케이션 생성

```python
from fastapi import FastAPI

app = FastAPI()
```

`FastAPI()`는 웹 애플리케이션 객체를 만든다. 이후 `app`에 URL 경로와 처리 함수를 연결한다.

```python
@app.get("/api/data")
async def get_data():
    return {"message": "FastAPI에서 보내는 데이터입니다"}
```

여기서 각 부분의 의미는 다음과 같다.

| 코드 | 의미 |
|---|---|
| `@app.get(...)` | 해당 경로로 들어오는 `GET` 요청을 등록한다. |
| `"/api/data"` | 요청을 받을 URL 경로다. |
| `get_data()` | 요청이 들어왔을 때 실행할 경로 처리 함수다. |
| `return {...}` | 클라이언트에 반환할 응답 데이터다. |

`@app.get()`과 같은 문법을 **경로 연산 데코레이터**라고 한다.

---

## 7. 라우팅

라우팅은 클라이언트가 요청한 HTTP 메서드와 URL을 어떤 함수가 처리할지 연결하는 작업이다.

```python
@app.get("/")
def home():
    return {"message": "메인 페이지"}
```

```text
GET /
  ↓
home() 실행
  ↓
JSON 응답 반환
```

같은 URL이라도 HTTP 메서드가 다르면 서로 다른 동작으로 구분할 수 있다.

```python
@app.get("/users")
def get_users():
    return {"message": "사용자 조회"}


@app.post("/users")
def create_user():
    return {"message": "사용자 생성"}
```

---

## 8. HTTP 메서드와 CRUD

HTTP 메서드는 서버에 어떤 작업을 요청하는지 나타낸다.

| HTTP 메서드 | 주요 용도 | CRUD |
|---|---|---|
| `GET` | 데이터 조회 | Read |
| `POST` | 새 데이터 생성 | Create |
| `PUT` | 데이터 전체 수정 | Update |
| `PATCH` | 데이터 일부 수정 | Update |
| `DELETE` | 데이터 삭제 | Delete |

FastAPI에서는 메서드에 맞는 데코레이터를 사용한다.

```python
@app.get("/users")
def read_users():
    pass


@app.post("/users")
def create_user():
    pass


@app.put("/users/{id}")
def update_user(id: int):
    pass


@app.delete("/users/{id}")
def delete_user(id: int):
    pass
```

---

## 9. REST와 RESTful API

REST는 자원을 URL로 표현하고 HTTP 메서드를 사용해 자원에 대한 작업을 구분하는 웹 아키텍처 스타일이다.

사용자를 자원으로 본다면 URL은 동사보다 명사 중심으로 작성할 수 있다.

| 요청 | 의미 |
|---|---|
| `GET /users` | 모든 사용자를 조회한다. |
| `GET /users/1` | 1번 사용자를 조회한다. |
| `POST /users` | 새 사용자를 생성한다. |
| `PUT /users/1` | 1번 사용자를 수정한다. |
| `DELETE /users/1` | 1번 사용자를 삭제한다. |

REST 원칙을 고려해 설계한 API를 RESTful API라고 한다. 실무에서는 모든 REST 원칙을 완벽하게 적용했는지보다 URL과 HTTP 메서드가 일관되고 이해하기 쉬운지가 중요하다.

---

## 10. JSON

JSON은 **JavaScript Object Notation**의 약자로, 서로 다른 프로그램 사이에서 데이터를 교환할 때 많이 사용하는 텍스트 형식이다.

```json
{
  "userid": "apple",
  "name": "김사과",
  "skills": ["Python", "FastAPI"],
  "profile": {
    "level": 1,
    "active": true
  }
}
```

JSON과 Python 딕셔너리는 모양이 비슷하지만 완전히 같은 것은 아니다.

| Python | JSON |
|---|---|
| `dict` | object |
| `list` | array |
| `True` | `true` |
| `False` | `false` |
| `None` | `null` |

FastAPI 경로 처리 함수에서 Python 딕셔너리를 반환하면 FastAPI가 JSON 응답으로 변환한다.

```python
@app.get("/api/data")
def get_data():
    return {"message": "안녕하세요", "success": True}
```

```json
{
  "message": "안녕하세요",
  "success": true
}
```

---

## 11. HTML 템플릿 연결

### 11.1 필요한 객체 가져오기

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
```

| 객체 | 역할 |
|---|---|
| `Request` | 현재 HTTP 요청의 정보를 담는다. |
| `HTMLResponse` | 응답이 HTML 문서임을 명시한다. |
| `Jinja2Templates` | Jinja2 HTML 템플릿을 불러온다. |

### 11.2 템플릿 폴더 등록

```python
templates = Jinja2Templates(directory="templates")
```

FastAPI가 `templates` 폴더 안에서 HTML 파일을 찾도록 설정한다.

### 11.3 HTML 페이지 응답

```python
@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )
```

`GET /` 요청이 들어오면 `templates/index.html`을 읽어 HTML 응답으로 반환한다.

`TemplateResponse`는 FastAPI와 Starlette 버전에 따라 위치 인자의 순서가 달라 혼동하기 쉽다. `request=`와 `name=`처럼 키워드 인자를 사용하면 각 값의 의미가 분명해진다.

---

## 12. 정적 파일 연결

정적 파일은 서버가 내용을 변경하지 않고 그대로 제공하는 CSS, JavaScript, 이미지 파일 등을 의미한다.

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

각 부분의 의미는 다음과 같다.

| 코드 | 의미 |
|---|---|
| `"/static"` | 브라우저가 접근할 URL 경로다. |
| `directory="static"` | 실제 파일이 저장된 폴더다. |
| `name="static"` | FastAPI 내부에서 사용할 이름이다. |

예제 HTML은 다음과 같이 JavaScript 파일을 불러온다.

```html
<script defer src="/static/script.js"></script>
```

브라우저는 다음 주소로 파일을 요청한다.

```text
GET /static/script.js
```

`defer`는 HTML 분석을 막지 않고 JavaScript 파일을 내려받은 뒤, HTML 문서 분석이 끝나면 스크립트를 실행하게 한다.

---

## 13. 프론트엔드에서 API 호출하기

`static/script.js`에서는 `fetch()`로 FastAPI의 `/api/data`에 요청을 보낸다.

```javascript
document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/data")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("result").textContent = data.message
    })
    .catch((error) => {
      document.getElementById("result").textContent =
        "데이터 불러오기 실패"
      console.error(error)
    })
})
```

코드는 다음 순서로 실행된다.

1. HTML 문서의 DOM 구성이 끝날 때까지 기다린다.
2. `fetch("/api/data")`가 FastAPI 서버에 `GET` 요청을 보낸다.
3. 서버가 보낸 JSON 응답을 `response.json()`으로 JavaScript 객체로 변환한다.
4. `data.message`를 `id="result"`인 요소의 글자로 넣는다.
5. 요청이나 데이터 처리에 실패하면 오류 문구를 출력한다.

전체 동작 흐름은 다음과 같다.

```text
브라우저에서 / 접속
        ↓
FastAPI가 index.html 반환
        ↓
브라우저가 /static/script.js 요청
        ↓
script.js가 /api/data 요청
        ↓
FastAPI가 JSON 응답 반환
        ↓
data.message를 화면에 출력
```

처음 HTML에는 다음 문구가 들어 있다.

```html
<p id="result">데이터를 불러오는 중...</p>
```

API 요청에 성공하면 다음 문구로 변경된다.

```text
FastAPI에서 보내는 데이터입니다
```

---

## 14. 경로 매개변수

경로 매개변수는 URL 경로 안에 포함되는 값이다. 중괄호를 사용해 정의한다.

```python
users = {
    0: {"userid": "apple", "name": "김사과"},
    1: {"userid": "banana", "name": "반하나"},
    2: {"userid": "orange", "name": "오렌지"},
}


@app.get("/users/{id}")
def find_user(id: int):
    user = users.get(id)

    if user is None:
        return {"error": "해당 id 없음"}

    return user
```

요청 주소에서 `0`이 `id`에 전달된다.

```text
GET /users/0
```

```json
{
  "userid": "apple",
  "name": "김사과"
}
```

존재하지 않는 사용자를 요청하면 다음 값을 반환한다.

```text
GET /users/10
```

```json
{
  "error": "해당 id 없음"
}
```

딕셔너리의 `users[id]`를 사용하면 키가 없을 때 `KeyError`가 발생한다. `users.get(id)`를 사용하면 키가 없을 때 `None`을 반환하므로 직접 예외 상황을 처리할 수 있다.

---

## 15. 여러 개의 경로 매개변수

URL에 경로 매개변수를 여러 개 넣을 수도 있다.

```python
@app.get("/users/{id}/{key}")
def find_user_by_key(id: int, key: str):
    user = users.get(id)

    if user is None or key not in user:
        return {"error": "잘못된 id 또는 key"}

    return user[key]
```

사용자의 `userid`만 조회하는 요청은 다음과 같다.

```text
GET /users/0/userid
```

```json
"apple"
```

사용자의 이름만 조회할 수도 있다.

```text
GET /users/0/name
```

```json
"김사과"
```

`id`가 없거나 `key`가 사용자 딕셔너리에 없으면 오류 메시지를 반환한다.

---

## 16. 쿼리 매개변수

쿼리 매개변수는 URL의 `?` 뒤에 `이름=값` 형태로 전달하는 값이다.

```text
/id-by-name?name=김사과
            └─ 쿼리 매개변수
```

경로에 중괄호로 선언되지 않은 함수 매개변수는 기본적으로 쿼리 매개변수로 처리된다.

```python
@app.get("/id-by-name")
def find_user_by_name(name: str):
    for idx, user in users.items():
        if user["name"] == name:
            return user

    return {"error": "데이터를 찾지 못함"}
```

요청은 다음과 같다.

```text
GET /id-by-name?name=김사과
```

```json
{
  "userid": "apple",
  "name": "김사과"
}
```

경로 매개변수와 쿼리 매개변수는 다음 기준으로 구분할 수 있다.

| 구분 | 예시 | 주로 사용하는 경우 |
|---|---|---|
| 경로 매개변수 | `/users/1` | 특정 자원을 식별할 때 사용한다. |
| 쿼리 매개변수 | `/users?name=김사과` | 검색, 필터, 정렬 조건을 전달할 때 사용한다. |

---

## 17. 요청 본문과 Pydantic

### 17.1 요청 본문

`POST` 요청으로 새 데이터를 만들 때는 보통 JSON 데이터를 요청 본문에 담아 보낸다.

```json
{
  "userid": "melon",
  "name": "이메론"
}
```

### 17.2 Pydantic 모델

FastAPI에서는 `BaseModel`을 상속해 요청 데이터의 형식을 정의한다.

```python
from pydantic import BaseModel


class User(BaseModel):
    userid: str
    name: str
```

이 모델은 다음 조건을 표현한다.

- 요청 본문에 `userid`가 있어야 한다.
- 요청 본문에 `name`이 있어야 한다.
- 두 값은 문자열이어야 한다.

### 17.3 사용자 생성 API

```python
@app.post("/users/{id}")
def create_user(id: int, user: User):
    if id in users:
        return {"error": "이미 존재하는 키"}

    users[id] = user.model_dump()
    return {"success": "ok"}
```

`id`는 URL에서 가져오는 경로 매개변수이고, `user`는 JSON 요청 본문에서 만드는 Pydantic 모델 객체다.

```text
POST /users/3
```

```json
{
  "userid": "melon",
  "name": "이메론"
}
```

처리 과정은 다음과 같다.

```text
URL의 3
  ↓
id: int에 전달

JSON 요청 본문
  ↓
User 모델로 검증
  ↓
user.model_dump()
  ↓
Python 딕셔너리로 변환
  ↓
users[3]에 저장
```

성공 응답은 다음과 같다.

```json
{
  "success": "ok"
}
```

`model_dump()`는 Pydantic 모델 객체를 Python 딕셔너리로 변환한다.

```python
user = User(userid="melon", name="이메론")

print(user.model_dump())
```

```text
{'userid': 'melon', 'name': '이메론'}
```

필수 필드가 빠지거나 자료형이 맞지 않으면 FastAPI가 자동으로 `422` 응답을 보낸다.

---

## 18. 경로·쿼리·본문 구분

FastAPI는 함수의 매개변수가 선언된 위치와 자료형을 보고 데이터의 출처를 구분한다.

```python
@app.post("/users/{id}")
def create_user(id: int, active: bool, user: User):
    return {
        "id": id,
        "active": active,
        "user": user,
    }
```

각 값의 출처는 다음과 같다.

| 매개변수 | 데이터 출처 | 이유 |
|---|---|---|
| `id` | 경로 매개변수 | URL에 `{id}`가 선언되어 있다. |
| `active` | 쿼리 매개변수 | 기본 자료형이고 경로에 선언되지 않았다. |
| `user` | 요청 본문 | `BaseModel`을 상속한 모델 타입이다. |

요청 예시는 다음과 같다.

```text
POST /users/3?active=true
```

```json
{
  "userid": "melon",
  "name": "이메론"
}
```

---

## 19. `def`와 `async def`

FastAPI 경로 처리 함수는 `def`와 `async def`를 모두 사용할 수 있다.

```python
@app.get("/sync")
def sync_route():
    return {"message": "일반 함수"}


@app.get("/async")
async def async_route():
    return {"message": "비동기 함수"}
```

`async def`는 다른 비동기 작업을 `await`해야 할 때 유용하다.

```python
@app.get("/data")
async def get_data():
    result = await some_async_function()
    return result
```

단순히 `async`를 붙인다고 모든 코드가 자동으로 빨라지는 것은 아니다. 비동기 HTTP 요청이나 비동기 데이터베이스 드라이버처럼 기다리는 동안 다른 요청을 처리할 수 있는 작업과 함께 사용할 때 효과가 크다.

---

## 20. 응답 상태 코드와 예외 처리

현재 예제는 오류가 발생해도 딕셔너리를 반환한다.

```python
if user is None:
    return {"error": "해당 id 없음"}
```

이 방식은 응답 내용에는 오류가 있지만 HTTP 상태 코드는 기본적으로 `200 OK`가 된다. 실제 API에서는 상황에 맞는 상태 코드를 반환하면 클라이언트가 성공과 실패를 더 명확하게 구분할 수 있다.

```python
from fastapi import HTTPException


@app.get("/users/{id}")
def find_user(id: int):
    user = users.get(id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="해당 id의 사용자가 없다.",
        )

    return user
```

주요 상태 코드는 다음과 같다.

| 상태 코드 | 의미 | 사용 예시 |
|---|---|---|
| `200 OK` | 요청 처리 성공 | 데이터 조회 성공 |
| `201 Created` | 데이터 생성 성공 | 사용자 생성 성공 |
| `400 Bad Request` | 잘못된 요청 | 요청 형식이나 값이 잘못됨 |
| `404 Not Found` | 자원을 찾지 못함 | 해당 사용자가 없음 |
| `422 Unprocessable Entity` | 데이터 검증 실패 | 필수 필드 누락, 타입 불일치 |
| `500 Internal Server Error` | 서버 내부 오류 | 처리 중 예상하지 못한 오류 발생 |

사용자 생성 API에는 `201`을 지정할 수 있다.

```python
@app.post("/users/{id}", status_code=201)
def create_user(id: int, user: User):
    if id in users:
        raise HTTPException(
            status_code=400,
            detail="이미 존재하는 키다.",
        )

    users[id] = user.model_dump()
    return users[id]
```

---

## 21. 자동 API 문서

FastAPI는 작성한 경로, 매개변수, Pydantic 모델을 분석해 API 문서를 자동으로 만든다.

서버를 실행한 뒤 다음 주소에 접속한다.

| 주소 | 문서 |
|---|---|
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |
| `http://127.0.0.1:8000/openapi.json` | OpenAPI 원본 JSON |

Swagger UI에서는 다음 작업을 할 수 있다.

- 등록된 API 경로를 확인한다.
- 경로·쿼리 매개변수의 이름과 자료형을 확인한다.
- 요청 본문의 JSON 구조를 확인한다.
- `Try it out` 버튼으로 API를 직접 호출한다.
- 응답 상태 코드와 응답 본문을 확인한다.

---

## 22. 서버 실행

실제 Python 파일명이 `fastapi_main.py`이고 FastAPI 객체 이름이 `app`이므로 다음과 같이 실행한다.

```bash
cd "/Users/songjeong-geun/Desktop/KDT/1_PYTHON"
uvicorn fastapi_main:app --reload
```

명령의 의미는 다음과 같다.

```text
uvicorn fastapi_main:app --reload
        └──────┬──────┘
               │
        fastapi_main.py의 app 객체
```

| 부분 | 의미 |
|---|---|
| `uvicorn` | ASGI 서버를 실행한다. |
| `fastapi_main` | `.py`를 제외한 파일명이다. |
| `app` | `app = FastAPI()`로 만든 객체 이름이다. |
| `--reload` | 코드가 변경되면 개발 서버를 다시 시작한다. |

포트를 변경하려면 `--port`를 사용한다.

```bash
uvicorn fastapi_main:app --reload --port 9000
```

서버 실행 후 확인할 주요 주소는 다음과 같다.

| 주소 | 결과 |
|---|---|
| `http://127.0.0.1:8000/` | HTML 페이지 |
| `http://127.0.0.1:8000/api/data` | 메시지 JSON |
| `http://127.0.0.1:8000/users/0` | 0번 사용자 |
| `http://127.0.0.1:8000/users/0/userid` | 0번 사용자의 아이디 |
| `http://127.0.0.1:8000/id-by-name?name=김사과` | 이름으로 사용자 검색 |
| `http://127.0.0.1:8000/docs` | Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc |

---

## 23. 예제 API 정리

| 메서드 | 경로 | 입력 | 역할 |
|---|---|---|---|
| `GET` | `/` | 없음 | HTML 페이지를 반환한다. |
| `GET` | `/api/data` | 없음 | 메시지 JSON을 반환한다. |
| `GET` | `/users/{id}` | 경로의 `id` | 특정 사용자를 조회한다. |
| `GET` | `/users/{id}/{key}` | 경로의 `id`, `key` | 사용자의 특정 필드를 조회한다. |
| `GET` | `/id-by-name` | 쿼리의 `name` | 이름으로 사용자를 조회한다. |
| `POST` | `/users/{id}` | 경로의 `id`, JSON 본문 | 새 사용자를 생성한다. |

---

## 24. 현재 예제에서 주의할 부분

### 24.1 `TemplateResponse` 인자

`fastapi_main.py`에는 다음 코드가 들어 있다.

```python
return templates.TemplateResponse({"request": request}, "index.html")
```

위치 인자는 라이브러리 버전에 따라 해석 순서가 달라질 수 있다. 다음처럼 키워드 인자로 작성하는 편이 이해하기 쉽다.

```python
return templates.TemplateResponse(
    request=request,
    name="index.html",
)
```

### 24.2 `Annotated`는 현재 사용하지 않음

다음 import는 현재 실행 코드에서 사용되지 않는다.

```python
from typing import Annotated
```

삭제해도 현재 예제의 동작에는 영향을 주지 않는다. `Annotated`는 자료형에 추가 검증 조건이나 설명을 붙일 때 사용할 수 있다.

```python
from typing import Annotated
from fastapi import Query


@app.get("/search")
def search(
    keyword: Annotated[str, Query(min_length=1)],
):
    return {"keyword": keyword}
```

### 24.3 딕셔너리 데이터는 영구 저장되지 않음

```python
users = {
    0: {"userid": "apple", "name": "김사과"},
}
```

`users`는 실행 중인 Python 프로세스의 메모리에 존재한다. `POST` 요청으로 사용자를 추가하더라도 서버를 종료하거나 다시 시작하면 추가한 데이터가 사라진다.

영구적으로 데이터를 저장하려면 MySQL, PostgreSQL, MongoDB 같은 데이터베이스나 파일 저장 방식을 연결해야 한다.

### 24.4 서버 실행 위치

`static`과 `templates`는 상대 경로로 설정되어 있다.

```python
StaticFiles(directory="static")
Jinja2Templates(directory="templates")
```

따라서 다른 폴더에서 Uvicorn을 실행하면 디렉터리를 찾지 못할 수 있다. 예제 파일이 있는 `1_PYTHON` 폴더로 이동한 뒤 서버를 실행한다.

### 24.5 패키지 설치 환경

패키지는 서버를 실행할 Python 환경에 설치해야 한다.

```bash
which python
python -m pip show fastapi
python -m pip show uvicorn
python -m pip show jinja2
```

가상환경을 사용한다면 가상환경을 활성화한 후 설치와 실행을 진행한다.

---

## 25. 자주 발생하는 오류

### 25.1 `ModuleNotFoundError: No module named 'fastapi'`

현재 Python 환경에 FastAPI가 설치되지 않은 경우 발생한다.

```bash
python -m pip install fastapi
```

### 25.2 `uvicorn: command not found`

Uvicorn이 설치되지 않았거나 현재 가상환경이 활성화되지 않은 경우 발생한다.

```bash
python -m pip install "uvicorn[standard]"
python -m uvicorn fastapi_main:app --reload
```

`python -m uvicorn`으로 실행하면 현재 `python`이 사용하는 환경의 Uvicorn을 명확하게 실행할 수 있다.

### 25.3 `Error loading ASGI app`

파일명이나 FastAPI 객체 이름이 잘못된 경우가 많다.

```bash
uvicorn fastapi_main:app --reload
```

다음 두 이름이 실제 코드와 일치해야 한다.

```text
fastapi_main → fastapi_main.py
app          → app = FastAPI()
```

### 25.4 `Directory 'static' does not exist`

Uvicorn을 실행한 위치에 `static` 폴더가 없거나 폴더명이 다른 경우 발생한다. `fastapi_main.py`, `static`, `templates`가 있는 프로젝트 폴더에서 실행한다.

### 25.5 템플릿 관련 오류

Jinja2가 설치되지 않았거나 `index.html` 경로가 잘못된 경우 발생할 수 있다.

```bash
python -m pip install jinja2
```

```text
templates
└── index.html
```

### 25.6 `422 Unprocessable Entity`

경로 매개변수의 타입이 맞지 않거나 요청 본문의 필수 값이 누락된 경우 발생한다.

```text
GET /users/apple
```

`id: int`이므로 `apple`은 정수로 변환할 수 없다.

```json
{
  "userid": "melon"
}
```

`User` 모델에 필요한 `name`이 없으므로 사용자 생성 요청이 검증에 실패한다.

---

## 26. 핵심 정리

- FastAPI는 Python 타입 힌트를 기반으로 요청 데이터를 처리하고 검증하는 웹 프레임워크다.
- Uvicorn은 FastAPI 애플리케이션을 실행하고 HTTP 요청을 전달하는 ASGI 서버다.
- `@app.get()`과 `@app.post()`는 HTTP 메서드와 URL을 Python 함수에 연결한다.
- 경로의 `{id}`는 경로 매개변수로 전달된다.
- 경로에 포함되지 않은 기본 자료형 매개변수는 쿼리 매개변수로 처리된다.
- `BaseModel` 타입의 매개변수는 JSON 요청 본문으로 처리된다.
- Pydantic은 요청 데이터의 필수 필드와 자료형을 자동으로 검사한다.
- Python 딕셔너리를 반환하면 FastAPI가 JSON 응답으로 변환한다.
- `StaticFiles`는 JavaScript, CSS, 이미지 등의 정적 파일을 제공한다.
- `Jinja2Templates`는 HTML 템플릿을 응답하는 데 사용한다.
- `/docs`와 `/redoc`에서 자동 생성된 API 문서를 확인할 수 있다.
- 예제의 `users` 딕셔너리는 메모리 데이터이므로 서버를 재시작하면 변경 내용이 사라진다.

이번 예제의 핵심은 단순히 URL마다 함수를 만드는 것이 아니다. **클라이언트가 어떤 형식으로 요청하고, FastAPI가 경로·쿼리·본문을 어떻게 구분하며, 처리 결과를 어떤 형식으로 응답하는지 전체 흐름을 이해하는 것**이다.
