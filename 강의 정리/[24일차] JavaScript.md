# JavaScript TODO 앱과 브라우저 저장소 정리

이번 내용은 JavaScript로 간단한 TODO 앱을 만들고, 브라우저 저장소를 이용해 데이터를 유지하는 방법을 정리한 것이다.

브라우저에서 사용할 수 있는 대표적인 저장 방식은 다음과 같다.

- `localStorage`
- `sessionStorage`
- Cookie

각 저장소는 데이터를 저장한다는 점은 비슷하지만, 유지 기간과 사용 목적이 다르다.

---

## 1. 전체 흐름

```text
TODO 앱 만들기
    ↓
배열에 할 일 저장
    ↓
DOM으로 화면 다시 그리기
    ↓
localStorage로 데이터 유지
    ↓
sessionStorage와 Cookie 차이 이해
    ↓
테마 변경처럼 사용자 설정 저장
```

---

## 2. TODO 앱 HTML 구조

TODO 앱은 입력창, 추가 버튼, 개수 표시 영역, 목록 영역으로 구성된다.

```html
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TODO앱</title>
    <link rel="stylesheet" href="./css/style.css">
</head>

<body>
    <div class="app">
        <h1>TODO 앱</h1>

        <div class="row">
            <input type="text" id="todoInput" placeholder="할 일을 입력하세요">
            <button id="addBtn" type="button">추가</button>
        </div>

        <div class="meta">
            <div>남은 항목 : <strong id="remainingCount">0</strong></div>
            <div>전체 : <strong id="totalCount">0</strong></div>
        </div>

        <ul id="todoList"></ul>
    </div>

    <script src="./js/todo.js"></script>
</body>

</html>
```

### 주요 요소

| 요소 | 역할 |
| --- | --- |
| `todoInput` | 할 일을 입력하는 입력창 |
| `addBtn` | 할 일을 추가하는 버튼 |
| `remainingCount` | 완료하지 않은 항목 수 표시 |
| `totalCount` | 전체 항목 수 표시 |
| `todoList` | 할 일 목록이 들어갈 영역 |

---

## 3. TODO 앱 기본 상태

TODO 앱은 할 일 데이터를 배열로 관리한다.

```javascript
const todos = []
```

하나의 할 일은 다음과 같은 객체 형태로 저장한다.

```javascript
{
    text: "아침식사",
    done: false
}
```

| 속성 | 의미 |
| --- | --- |
| `text` | 할 일 내용 |
| `done` | 완료 여부 |

예를 들어 할 일이 여러 개 있으면 다음과 같은 배열이 된다.

```javascript
const todos = [
    { text: "아침식사", done: false },
    { text: "운동하기", done: true },
    { text: "JavaScript 공부", done: false }
]
```

---

## 4. DOM 요소 선택

TODO 앱에서 자주 사용할 요소를 미리 선택한다.

```javascript
const todoInput = document.getElementById("todoInput")
const addBtn = document.getElementById("addBtn")
const todoList = document.getElementById("todoList")
const remainingCount = document.getElementById("remainingCount")
const totalCount = document.getElementById("totalCount")
```

이렇게 변수에 저장해두면 같은 요소를 여러 번 사용할 때 코드가 더 깔끔해진다.

---

## 5. 화면 다시 그리기: `render()`

`render()` 함수는 현재 `todos` 배열을 기준으로 화면을 다시 그리는 함수다.

```javascript
function render() {
    todoList.innerHTML = ""

    todos.forEach((todo, index) => {
        const li = document.createElement("li")

        if (todo.done) {
            li.classList.add("done")
        }

        const left = document.createElement("div")
        left.className = "left"

        const checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox.checked = todo.done

        checkbox.addEventListener("change", () => {
            todo.done = checkbox.checked
            render()
        })

        const text = document.createElement("span")
        text.className = "todo-text"
        text.textContent = todo.text

        const delBtn = document.createElement("button")
        delBtn.type = "button"
        delBtn.className = "delete-btn"
        delBtn.textContent = "삭제"

        delBtn.addEventListener("click", () => {
            todos.splice(index, 1)
            render()
        })

        left.appendChild(checkbox)
        left.appendChild(text)
        left.appendChild(delBtn)

        li.appendChild(left)
        todoList.appendChild(li)
    })

    updateCounts()
}
```

### 동작 흐름

```text
기존 목록 비우기
    ↓
todos 배열 반복
    ↓
li, 체크박스, 텍스트, 삭제 버튼 생성
    ↓
각 버튼에 이벤트 연결
    ↓
ul에 li 추가
    ↓
개수 업데이트
```

> 원본 코드에는 `render()` 함수 마지막에 `render()`를 다시 호출하는 부분이 있다. 이 코드는 무한 재귀 호출을 만들 수 있으므로 제거해야 한다.

---

## 6. 개수 업데이트

```javascript
function updateCounts() {
    remainingCount.textContent = String(todos.filter(todo => !todo.done).length)
    totalCount.textContent = String(todos.length)
}
```

`filter()`는 조건을 만족하는 요소만 모아 새 배열을 만든다.

```javascript
todos.filter(todo => !todo.done)
```

위 코드는 완료되지 않은 할 일만 모은다.

---

## 7. 할 일 추가

```javascript
function addTodo() {
    const text = todoInput.value.trim()

    if (!text) return

    todos.push({ text, done: false })
    todoInput.value = ""
    todoInput.focus()

    render()
}
```

### 코드 설명

| 코드 | 의미 |
| --- | --- |
| `trim()` | 앞뒤 공백 제거 |
| `if (!text) return` | 빈 문자열이면 추가하지 않음 |
| `todos.push()` | 배열 끝에 새 할 일 추가 |
| `todoInput.value = ""` | 입력창 비우기 |
| `todoInput.focus()` | 입력창에 다시 커서 이동 |
| `render()` | 화면 다시 그리기 |

---

## 8. 버튼과 Enter 이벤트 연결

```javascript
addBtn.addEventListener("click", addTodo)

todoInput.addEventListener("keydown", (e) => {
    if (e.isComposing) return
    if (e.key === "Enter") addTodo()
})
```

버튼을 클릭하거나 입력창에서 Enter를 누르면 할 일이 추가된다.

`e.isComposing`은 한글 입력 조합 중 Enter가 중복 처리되는 문제를 줄이기 위해 사용할 수 있다.

---

## 9. TODO 앱 전체 JavaScript

```javascript
const todoInput = document.getElementById("todoInput")
const addBtn = document.getElementById("addBtn")
const todoList = document.getElementById("todoList")
const remainingCount = document.getElementById("remainingCount")
const totalCount = document.getElementById("totalCount")

const todos = []

function render() {
    todoList.innerHTML = ""

    todos.forEach((todo, index) => {
        const li = document.createElement("li")

        if (todo.done) {
            li.classList.add("done")
        }

        const left = document.createElement("div")
        left.className = "left"

        const checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox.checked = todo.done

        checkbox.addEventListener("change", () => {
            todo.done = checkbox.checked
            render()
        })

        const text = document.createElement("span")
        text.className = "todo-text"
        text.textContent = todo.text

        const delBtn = document.createElement("button")
        delBtn.type = "button"
        delBtn.className = "delete-btn"
        delBtn.textContent = "삭제"

        delBtn.addEventListener("click", () => {
            todos.splice(index, 1)
            render()
        })

        left.appendChild(checkbox)
        left.appendChild(text)
        left.appendChild(delBtn)

        li.appendChild(left)
        todoList.appendChild(li)
    })

    updateCounts()
}

function updateCounts() {
    remainingCount.textContent = String(todos.filter(todo => !todo.done).length)
    totalCount.textContent = String(todos.length)
}

function addTodo() {
    const text = todoInput.value.trim()

    if (!text) return

    todos.push({ text, done: false })
    todoInput.value = ""
    todoInput.focus()

    render()
}

addBtn.addEventListener("click", addTodo)

todoInput.addEventListener("keydown", (e) => {
    if (e.isComposing) return
    if (e.key === "Enter") addTodo()
})

render()
```

이 버전은 메모리에만 데이터를 저장한다. 따라서 페이지를 새로고침하면 `todos` 배열이 다시 빈 배열이 되어 기존 할 일이 사라진다.

데이터를 새로고침 후에도 유지하려면 `localStorage`를 사용할 수 있다.

---

## 10. 브라우저 저장소 비교

| 구분 | localStorage | sessionStorage | Cookie |
| --- | --- | --- | --- |
| 저장 위치 | 브라우저 | 브라우저 | 브라우저 |
| 유지 기간 | 직접 삭제 전까지 유지 | 탭 또는 창을 닫으면 삭제 | 만료 시간까지 유지 |
| 저장 용량 | 약 5MB | 약 5MB | 약 4KB |
| 서버 전송 | 자동 전송 안 됨 | 자동 전송 안 됨 | 같은 사이트 요청마다 자동 전송 |
| 데이터 형식 | 문자열 | 문자열 | 문자열 |
| 탭 간 공유 | 같은 도메인에서 공유 | 같은 탭에서만 유지 | 같은 도메인 조건에 따라 공유 |
| 사용 예 | 테마, TODO 목록 | 일시적 방문 횟수 | 팝업 숨김, 로그인 상태 보조 |

민감한 정보인 비밀번호, 인증 토큰, 주민등록번호 등은 브라우저 저장소에 저장하지 않는 것이 원칙이다.

---

## 11. localStorage

`localStorage`는 브라우저가 제공하는 웹 스토리지 기능 중 하나다.

키와 값 형태로 데이터를 저장하며, 브라우저를 닫았다가 다시 열어도 데이터가 유지된다.

### 특징

- 브라우저에 데이터를 영구적으로 저장한다.
- 같은 도메인에서 접근할 수 있다.
- 약 5MB 내외의 저장 공간을 제공한다.
- 문자열만 저장할 수 있다.
- 직접 삭제하기 전까지 데이터가 유지된다.

### 기본 문법

```javascript
localStorage.setItem("키", "값")

const value = localStorage.getItem("키")

localStorage.removeItem("키")

localStorage.clear()
```

| 메서드 | 설명 |
| --- | --- |
| `setItem(key, value)` | 데이터 저장 |
| `getItem(key)` | 데이터 불러오기 |
| `removeItem(key)` | 특정 데이터 삭제 |
| `clear()` | 전체 데이터 삭제 |

---

## 12. 객체를 localStorage에 저장하기

`localStorage`에는 문자열만 저장할 수 있다.

객체를 저장하려면 `JSON.stringify()`로 문자열로 바꾸어야 한다.

```javascript
function saveUser() {
    const user = {
        name: "김사과",
        age: 20,
        job: "개발자"
    }

    localStorage.setItem("user", JSON.stringify(user))
}
```

> 원본 예제의 `locatStorage`는 오타다. 올바른 이름은 `localStorage`다.

저장한 문자열을 다시 객체로 사용하려면 `JSON.parse()`를 사용한다.

```javascript
function loadUser() {
    const data = localStorage.getItem("user")

    if (data) {
        const user = JSON.parse(data)

        document.getElementById("info").innerText =
            `이름: ${user.name}, 나이: ${user.age}, 직업: ${user.job}`
    }
}
```

### JSON 변환 흐름

```text
객체
  ↓ JSON.stringify()
문자열
  ↓ localStorage 저장
브라우저 저장소
  ↓ JSON.parse()
객체
```

---

## 13. localStorage로 테마 변경하기

테마 변경 기능은 `localStorage`를 활용하기 좋은 예제다.

사용자가 어두운 테마를 선택했다면 새로고침 후에도 같은 테마가 유지되어야 하기 때문이다.

### HTML

```html
<button onclick="toggleTheme()">테마변경</button>
<p>현재 테마: <span id="themeText"></span></p>
```

### JavaScript

```javascript
const body = document.body

function applyTheme(theme) {
    body.style.backgroundColor = theme === "dark" ? "#222" : "#fff"
    body.style.color = theme === "dark" ? "#fff" : "#222"
    document.getElementById("themeText").innerText = theme
}

function toggleTheme() {
    const current = localStorage.getItem("theme") || "white"
    const next = current === "white" ? "dark" : "white"

    localStorage.setItem("theme", next)
    applyTheme(next)
}

applyTheme(localStorage.getItem("theme") || "white")
```

### 동작 흐름

```text
페이지 로드
    ↓
localStorage에서 theme 값 확인
    ↓
저장된 값이 있으면 해당 테마 적용
    ↓
버튼 클릭
    ↓
white ↔ dark 변경
    ↓
변경된 테마를 localStorage에 저장
```

---

## 14. TODO 앱에 localStorage 적용하기

TODO 앱도 `localStorage`를 사용하면 새로고침 후에도 목록을 유지할 수 있다.

### 저장된 TODO 불러오기

```javascript
const savedTodos = localStorage.getItem("todos")
const todos = savedTodos ? JSON.parse(savedTodos) : []
```

### TODO 저장하기

```javascript
function saveTodos() {
    localStorage.setItem("todos", JSON.stringify(todos))
}
```

### `render()`와 이벤트에서 저장하기

```javascript
function render() {
    todoList.innerHTML = ""

    todos.forEach((todo, index) => {
        const li = document.createElement("li")

        if (todo.done) li.classList.add("done")

        const checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox.checked = todo.done

        checkbox.addEventListener("change", () => {
            todo.done = checkbox.checked
            saveTodos()
            render()
        })

        const text = document.createElement("span")
        text.textContent = todo.text

        const delBtn = document.createElement("button")
        delBtn.type = "button"
        delBtn.textContent = "삭제"

        delBtn.addEventListener("click", () => {
            todos.splice(index, 1)
            saveTodos()
            render()
        })

        li.appendChild(checkbox)
        li.appendChild(text)
        li.appendChild(delBtn)
        todoList.appendChild(li)
    })

    updateCounts()
}

function addTodo() {
    const text = todoInput.value.trim()

    if (!text) return

    todos.push({ text, done: false })
    saveTodos()

    todoInput.value = ""
    todoInput.focus()

    render()
}
```

### 저장 시점

```text
할 일 추가       → saveTodos()
완료 체크 변경   → saveTodos()
할 일 삭제       → saveTodos()
```

---

## 15. sessionStorage

`sessionStorage`는 탭 또는 창 단위로 데이터를 임시 저장하는 저장소다.

페이지를 새로고침해도 데이터는 유지되지만, 브라우저 탭이나 창을 닫으면 데이터가 삭제된다.

### 특징

- 탭 단위로 데이터가 유지된다.
- 같은 사이트라도 다른 탭과 데이터가 공유되지 않는다.
- 새로고침해도 값이 유지된다.
- 탭을 닫으면 자동으로 삭제된다.
- 문자열만 저장할 수 있다.
- 약 5MB 정도 저장할 수 있다.

### 기본 문법

```javascript
sessionStorage.setItem("key", "value")

const value = sessionStorage.getItem("key")

sessionStorage.removeItem("key")

sessionStorage.clear()
```

> 원본 메모의 `sessionStorage.remove("key")`는 올바른 메서드명이 아니다. 특정 항목 삭제는 `removeItem("key")`를 사용한다.

---

## 16. sessionStorage 방문 횟수 예제

```html
<h2>이 탭에서 방문한 횟수: <span id="counter">0</span>회</h2>
```

```javascript
let count = sessionStorage.getItem("visitCount")

count = count ? Number(count) + 1 : 1

sessionStorage.setItem("visitCount", count)
document.getElementById("counter").innerText = count
```

### 동작 흐름

```text
visitCount 값 가져오기
    ↓
값이 있으면 숫자로 바꾼 뒤 1 증가
    ↓
값이 없으면 1로 시작
    ↓
sessionStorage에 다시 저장
    ↓
화면에 방문 횟수 출력
```

페이지를 새로고침하면 숫자가 증가한다. 하지만 탭을 닫았다가 다시 열면 값이 초기화된다.

---

## 17. 쿠키

쿠키(Cookie)는 브라우저가 작은 텍스트 데이터를 저장해두었다가 같은 웹사이트에 요청을 보낼 때 서버에 함께 전송하는 저장 방식이다.

### 특징

- 저장 용량이 약 4KB로 작다.
- 만료 시간을 설정할 수 있다.
- 같은 사이트 요청마다 서버로 자동 전송될 수 있다.
- 보안과 성능 측면에서 주의가 필요하다.

### 쿠키 저장

```javascript
document.cookie = "userid=apple"
```

### 만료 시간 설정

```javascript
const date = new Date()
date.setDate(date.getDate() + 7)

document.cookie = "userid=apple; expires=" + date.toUTCString()
```

### 쿠키 읽기

```javascript
console.log(document.cookie)
```

### 쿠키 삭제

쿠키는 `expires` 값을 과거 날짜로 설정하면 삭제된다.

```javascript
document.cookie = "userid=apple; expires=Thu, 01 Jan 1970 00:00:00 UTC"
```

---

## 18. 쿠키로 팝업 하루 숨기기

공지 팝업을 닫을 때 `오늘 하루 보지 않기`를 체크하면 쿠키를 저장하고, 다음 방문 때 팝업을 숨긴다.

### HTML

```html
<div id="popup" style="padding: 20px; background-color: #f0f0f0; border:1px solid #ccc; width:300px">
    <p><strong>[공지]</strong> 신규 강의가 업데이트 되었습니다.</p>

    <label>
        <input type="checkbox" id="hideToday">
        오늘 하루 보지 않기
    </label>

    <hr>

    <button onclick="closePopup()">닫기</button>
</div>
```

### 쿠키 저장 함수

```javascript
function setCookie(name, value, days) {
    const d = new Date()
    d.setTime(d.getTime() + days * 24 * 60 * 60 * 1000)

    const expires = "expires=" + d.toUTCString()

    document.cookie = `${name}=${value}; ${expires}; path=/`
}
```

> 원본 예제의 `const expires = "expires" + d.toUTCString()`는 `expires=`가 빠져 있어 쿠키 만료 시간이 의도대로 설정되지 않을 수 있다.

### 팝업 닫기

```javascript
function closePopup() {
    const checkbox = document.getElementById("hideToday")

    if (checkbox.checked) {
        setCookie("hidePopup", "true", 1)
    }

    document.getElementById("popup").style.display = "none"
}
```

### 쿠키 읽기

```javascript
function getCookie(name) {
    const decodedCookie = decodeURIComponent(document.cookie)
    const cookies = decodedCookie.split("; ")

    for (let cookie of cookies) {
        const [key, value] = cookie.split("=")

        if (key === name) return value
    }

    return null
}
```

### 페이지 로드 시 팝업 숨김

```javascript
window.onload = function () {
    if (getCookie("hidePopup") === "true") {
        document.getElementById("popup").style.display = "none"
    }
}
```

### 동작 흐름

```text
사용자가 오늘 하루 보지 않기 체크
        ↓
닫기 버튼 클릭
        ↓
hidePopup=true 쿠키 저장
        ↓
팝업 숨김
        ↓
다음 방문 시 쿠키 확인
        ↓
hidePopup=true라면 팝업 숨김
```

---

## 19. localStorage, sessionStorage, Cookie 선택 기준

### localStorage가 어울리는 경우

- 사용자가 선택한 테마 저장
- TODO 목록 저장
- 마지막으로 선택한 탭이나 필터 저장
- 서버로 자동 전송할 필요 없는 사용자 설정 저장

### sessionStorage가 어울리는 경우

- 현재 탭에서만 유지할 임시 데이터
- 새로고침해도 유지되어야 하지만 탭을 닫으면 사라져도 되는 값
- 탭별로 독립되어야 하는 값

### Cookie가 어울리는 경우

- 만료 시간이 필요한 작은 데이터
- 서버와 함께 확인해야 하는 값
- 팝업 하루 숨김 같은 간단한 상태 저장

단, 쿠키는 요청마다 서버로 전송될 수 있으므로 큰 데이터 저장에는 적합하지 않다.

---

## 20. 보안 주의사항

브라우저 저장소는 사용자가 개발자 도구로 확인하거나 수정할 수 있다.

따라서 다음과 같은 민감한 정보는 저장하지 않는 것이 좋다.

- 비밀번호
- 주민등록번호
- 신용카드 번호
- 민감한 개인정보
- 중요한 인증 토큰

클라이언트 저장소는 편의 기능을 위한 공간으로 이해해야 한다.

---

## 21. 핵심 정리

### TODO 앱

- 할 일은 객체 형태로 배열에 저장한다.
- `render()`는 배열 상태를 기준으로 화면을 다시 그린다.
- 체크박스 변경과 삭제 버튼 클릭 시 배열을 수정하고 다시 렌더링한다.
- 메모리 배열만 사용하면 새로고침 시 데이터가 사라진다.

### localStorage

- 브라우저를 닫아도 데이터가 유지된다.
- 문자열만 저장할 수 있다.
- 객체와 배열은 `JSON.stringify()`로 저장하고 `JSON.parse()`로 다시 꺼낸다.
- 테마 설정이나 TODO 목록 저장에 적합하다.

### sessionStorage

- 현재 탭에서만 유지된다.
- 새로고침해도 유지된다.
- 탭을 닫으면 삭제된다.
- 방문 횟수처럼 임시 데이터를 저장하기 좋다.

### Cookie

- 작은 텍스트 데이터를 저장한다.
- 만료 시간을 설정할 수 있다.
- 같은 사이트 요청에 서버로 전송될 수 있다.
- 팝업 하루 숨김 같은 기능에 사용할 수 있다.

### 저장소 선택

```text
오래 유지할 사용자 설정      → localStorage
탭 안에서만 필요한 임시 값   → sessionStorage
만료 시간이 필요한 작은 값   → Cookie
```
