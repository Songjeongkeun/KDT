# JavaScript BOM, DOM, 화살표 함수, 콜백 함수, 이벤트 정리

JavaScript는 단순히 값을 계산하는 언어가 아니라 브라우저와 웹 페이지를 직접 제어할 수 있는 언어다.

브라우저 자체를 다룰 때는 **BOM**, HTML 문서를 다룰 때는 **DOM**, 사용자 행동에 반응할 때는 **이벤트**를 사용한다.

이번 글에서는 다음 흐름으로 정리한다.

```text
BOM으로 브라우저 정보와 URL 제어
        ↓
DOM으로 HTML 요소 선택과 수정
        ↓
화살표 함수와 콜백 함수로 동작 전달
        ↓
이벤트로 사용자 동작에 반응
```

---

## 1. BOM(Browser Object Model)

JavaScript가 브라우저 자체를 제어하고 브라우저 정보를 얻기 위해 사용하는 객체 모델이다.

대표적인 BOM 객체는 다음과 같다.

| 객체 | 역할 |
| --- | --- |
| `window` | 브라우저 창을 대표하는 최상위 객체 |
| `location` | 현재 페이지의 URL 정보를 확인하거나 이동 |
| `history` | 브라우저 방문 기록 제어 |
| `navigator` | 브라우저와 사용자 환경 정보 확인 |

---

## 2. API(**Application Programming Interface**)

서로 다른 프로그램이나 시스템이 데이터를 주고받고 기능을 사용할 수 있도록 연결해주는 중간 통로다.

예를 들어 브라우저가 제공하는 위치 정보 기능을 JavaScript에서 사용할 수 있는 것도 API를 통해 가능하다.

```text
JavaScript 코드
      ↓
브라우저 API
      ↓
브라우저 기능 사용
```

---

## 3. `window` 객체

`window`는 브라우저 창을 대표하는 최상위 객체다.

전역 범위에서 정의된 변수나 함수, 타이머, 팝업, 브라우저 정보 등 많은 기능이 `window` 객체에 포함된다.

```javascript
function showWindowInfo() {
    console.log("브라우저 이름:", window.navigator.appName)
    console.log("브라우저 엔진:", window.navigator.product)
    console.log("사용자 에이전트:", window.navigator.userAgent)
    console.log("현재 페이지 URL:", window.location.href)
    console.log("창 너비:", window.innerWidth)
    console.log("창 높이:", window.innerHeight)
}

showWindowInfo()
```

### 출력 결과

```text
브라우저 이름: Netscape
브라우저 엔진: Gecko
사용자 에이전트: Mozilla/5.0 ...
현재 페이지 URL: file:///...
창 너비: 1440
창 높이: 900
```

브라우저 정보는 사용 환경에 따라 다르게 출력된다.

`window`는 최상위 객체이므로 일부 경우에는 생략할 수 있다.

```javascript
console.log(window.location.href)
console.log(location.href)
```

---

## 4. 타이머 함수

`setTimeout()`은 일정 시간이 지난 뒤 함수를 한 번 실행한다.

```javascript
setTimeout(function () {
    alert("3초가 지났습니다.")
}, 3000)
```

`3000`은 3000ms, 즉 3초를 의미한다.

화살표 함수로도 작성할 수 있다.

```javascript
setTimeout(() => {
    alert("3초가 지났습니다.")
}, 3000)
```

---

## 5. `location` 객체

`location`은 현재 웹 페이지의 URL 정보를 다루는 객체다.

```javascript
function showLocationInfo() {
    console.log("전체 URL:", location.href)
    console.log("프로토콜:", location.protocol)
    console.log("호스트:", location.host)
    console.log("호스트명:", location.hostname)
    console.log("포트번호:", location.port)
    console.log("경로:", location.pathname)
    console.log("쿼리 문자열:", location.search)
}
```

URL이 다음과 같다고 가정한다.

```text
https://example.com:8080/search?q=javascript
```

출력은 다음과 비슷하다.

```text
전체 URL: https://example.com:8080/search?q=javascript
프로토콜: https:
호스트: example.com:8080
호스트명: example.com
포트번호: 8080
경로: /search
쿼리 문자열: ?q=javascript
```

### 페이지 새로고침

```javascript
function reloadPage() {
    location.reload()
}
```

### 다른 페이지로 이동

```javascript
function goToNaver() {
    location.href = "https://www.naver.com"
}
```

### 쿼리 문자열

쿼리 문자열은 URL에서 `?` 뒤에 붙어 데이터를 전달하는 방식이다.

```text
https://example.com/search?keyword=javascript&page=1
```

```text
keyword=javascript
page=1
```

---

## 6. `history` 객체

`history` 객체는 브라우저의 방문 기록을 제어한다.

```javascript
function goBack() {
    history.back()
}

function goForward() {
    history.forward()
}

function showHistoryLength() {
    alert("방문 기록 수: " + history.length)
}
```

| 메서드 또는 속성 | 설명 |
| --- | --- |
| `history.back()` | 이전 페이지로 이동 |
| `history.forward()` | 다음 페이지로 이동 |
| `history.length` | 현재 탭의 방문 기록 개수 |

---

## 7. `navigator` 객체

`navigator` 객체는 브라우저와 사용자 환경 정보를 제공한다.

```javascript
function showNavigatorInfo() {
    console.log("브라우저 정보:", navigator.userAgent)
    console.log("운영체제:", navigator.platform)
    console.log("언어 설정:", navigator.language)
    console.log("쿠키 사용 가능 여부:", navigator.cookieEnabled)
}
```

### 위치 정보 가져오기

`navigator.geolocation`은 사용자의 위치 정보를 가져오기 위한 API다.

위치 정보는 개인정보에 해당하므로 사용자의 명시적인 동의가 있어야 작동한다.

```html
<p id="locationInfo">위치 정보가 여기에 표시됩니다.</p>
<button onclick="getLocation()">위치 가져오기</button>
```

```javascript
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError)
    } else {
        document.getElementById("locationInfo").innerText =
            "이 브라우저는 위치 정보를 지원하지 않습니다."
    }
}

function showPosition(position) {
    const latitude = position.coords.latitude
    const longitude = position.coords.longitude

    document.getElementById("locationInfo").innerText =
        `위도: ${latitude}, 경도: ${longitude}`
}

function showError(error) {
    switch (error.code) {
        case error.PERMISSION_DENIED:
            alert("사용자가 위치 정보 제공을 거부했습니다.")
            break
        case error.POSITION_UNAVAILABLE:
            alert("위치 정보를 사용할 수 없습니다.")
            break
        case error.TIMEOUT:
            alert("위치 정보를 가져오는 데 시간이 초과되었습니다.")
            break
        default:
            alert("알 수 없는 오류가 발생했습니다.")
    }
}
```

---

## 8. DOM

DOM은 **Document Object Model**의 약자다.

브라우저가 HTML 문서를 읽고 각 태그를 객체로 만든 구조다. JavaScript는 DOM을 통해 HTML 요소를 선택하고, 내용이나 스타일을 변경하고, 요소를 추가하거나 삭제할 수 있다.

```text
HTML 문서
   ↓ 브라우저가 읽음
DOM 트리 생성
   ↓
JavaScript가 DOM 객체를 조작
   ↓
화면 변경
```

### DOM 작동 원리

1. 브라우저가 HTML 파일을 읽는다.
2. HTML 태그를 하나씩 분석한다.
3. 각 태그를 노드 객체로 만든다.
4. JavaScript는 DOM 객체를 통해 화면을 제어한다.

---

## 9. `document` 객체

`document` 객체는 웹 페이지 전체를 표현하는 최상위 DOM 객체다.

브라우저가 HTML 파일을 로드하면 자동으로 `document` 객체가 생성된다.

`document`를 사용하면 다음 작업을 할 수 있다.

- 요소 선택
- 요소 생성
- 내용 수정
- 스타일 변경
- 속성 변경
- 요소 추가 또는 삭제

---

## 10. DOM 요소 선택

### HTML

```html
<p id="greeting">안녕하세요.</p>
<p class="item">아이템 1</p>
<p class="item">아이템 2</p>
<p class="desc">1번째 문장</p>
<p class="desc">2번째 문장</p>
```

### 10.1 `getElementById()`

`id`로 요소 하나를 선택한다.

```javascript
const greeting = document.getElementById("greeting")
console.log(greeting.innerText)
```

```text
안녕하세요.
```

### 10.2 `getElementsByClassName()`

`class` 이름으로 여러 요소를 선택한다.

```javascript
const items = document.getElementsByClassName("item")

for (let i = 0; i < items.length; i++) {
    console.log(items[i].innerText)
}
```

```text
아이템 1
아이템 2
```

### 10.3 `querySelector()`

CSS 선택자와 일치하는 첫 번째 요소를 선택한다.

```javascript
const desc = document.querySelector(".desc")
console.log(desc.innerText)
```

```text
1번째 문장
```

### 10.4 `querySelectorAll()`

CSS 선택자와 일치하는 모든 요소를 선택한다.

```javascript
const descList = document.querySelectorAll(".desc")

for (let i = 0; i < descList.length; i++) {
    console.log(descList[i].innerText)
}
```

```text
1번째 문장
2번째 문장
```

---

## 11. DOM 내용과 스타일 변경

### 11.1 텍스트 변경

```javascript
function changeText() {
    document.getElementById("greeting").innerText = "반가워요."
}
```

`innerText`는 글자만 넣을 때 사용한다.

### 11.2 스타일 변경

```javascript
function highlightItems() {
    const items = document.getElementsByClassName("item")

    for (let i = 0; i < items.length; i++) {
        items[i].style.color = "deeppink"
    }
}
```

### 11.3 HTML 변경

```javascript
function updateFirst() {
    const item = document.querySelector(".desc")
    item.innerHTML = "<b>바뀐 문장</b>"
}
```

`innerHTML`은 글자와 HTML 태그를 함께 넣을 수 있다.

```javascript
function updateDesc() {
    const items = document.querySelectorAll(".desc")

    for (let i = 0; i < items.length; i++) {
        items[i].innerHTML = "<h3>바뀐 문장</h3>"
    }
}
```

> 사용자 입력값을 그대로 `innerHTML`에 넣으면 보안 문제가 생길 수 있다. 단순 텍스트를 넣을 때는 `innerText`나 `textContent`를 사용하는 것이 안전하다.

---

## 12. DOM 요소 추가와 삭제

### HTML

```html
<ul id="list">
    <li>기존 항목</li>
</ul>
```

### 12.1 요소 생성 후 추가

```javascript
function addItem() {
    const newItem = document.createElement("li")
    newItem.innerText = "새 항목"

    document.getElementById("list").appendChild(newItem)
}
```

### 12.2 요소 삭제

```javascript
function removeItem() {
    const ul = document.getElementById("list")
    const li = document.querySelector("li")

    ul.removeChild(li)
}
```

### 12.3 맨 앞에 요소 추가

```javascript
function insertItem() {
    const ul = document.getElementById("list")
    const newItem = document.createElement("li")
    newItem.innerText = "사과"

    const firstItem = ul.firstElementChild
    ul.insertBefore(newItem, firstItem)
}
```

### 12.4 요소 자체 삭제

```javascript
function removeText() {
    document.getElementById("notice").remove()
}
```

---

## 13. DOM 속성 변경과 노드 복제

### 이미지 변경

```html
<img id="image" src="./images/spring1.png" alt="봄1">
```

```javascript
function changeImage() {
    document
        .getElementById("image")
        .setAttribute("src", "./images/spring2.png")
}
```

`setAttribute()`는 HTML 속성 값을 변경한다.

### 새 문단 추가

```html
<div id="box"></div>
```

```javascript
function appendP() {
    const div = document.getElementById("box")
    const p = document.createElement("p")

    p.innerText = "새 문단 추가!"
    div.appendChild(p)
}
```

### 노드 복제

```javascript
function copyChild() {
    const original = document.getElementById("list")
    const clone = original.cloneNode(true)

    document.body.appendChild(clone)
}
```

`cloneNode(true)`는 자식 요소까지 함께 복제한다.

```text
cloneNode(true)  → 깊은 복사
cloneNode(false) → 해당 노드만 복사
```

---

## 14. 화살표 함수

화살표 함수는 `function` 키워드 대신 `=>`를 사용하는 함수 표현 방식이다.

```javascript
const func1 = () => {
    console.log("실행")
}

const func2 = (a, b) => {
    return a + b
}

const func3 = x => {
    return x * x
}

const func4 = (a, b) => a + b

const func5 = (a, b) => ({ a, b })
```

함수 본문이 한 줄이고 값을 바로 반환한다면 `{}`와 `return`을 생략할 수 있다.

```javascript
const add = (a, b) => a + b

console.log(add(3, 5))
```

```text
8
```

---

## 15. JavaScript의 `this`

JavaScript에서 `this`는 함수가 어디에 선언되었는지가 아니라 **어떻게 호출되었는지**에 따라 달라진다.

### 일반 함수 호출

```javascript
function show() {
    console.log(this)
}

show()
```

브라우저의 느슨한 모드에서 일반 함수로 호출하면 `this`는 보통 `window`를 가리킨다.

### 객체의 메서드 호출

```javascript
const obj = {
    name: "김사과",
    show() {
        console.log(this.name)
    }
}

obj.show()
```

### 출력 결과

```text
김사과
```

메서드 호출에서는 점 앞의 객체가 `this`가 된다.

---

## 16. 콜백 함수에서 `this`가 바뀌는 문제

`setTimeout()` 안에서 일반 함수를 사용하면 `this`가 원래 객체를 가리키지 않을 수 있다.

```javascript
const obj2 = {
    name: "김사과",
    show() {
        setTimeout(function () {
            console.log(this.name)
        }, 1000)
    }
}

obj2.show()
```

이 경우 콜백 함수 내부의 `this`는 `obj2`가 아니다. 따라서 원하는 값이 출력되지 않을 수 있다.

---

## 17. 화살표 함수와 `this`

화살표 함수는 자신만의 `this`를 만들지 않고, 바깥 스코프의 `this`를 그대로 사용한다.

```javascript
const obj3 = {
    name: "김사과",
    show() {
        setTimeout(() => {
            console.log(this.name)
        }, 1000)
    }
}

obj3.show()
```

### 출력 결과

```text
김사과
```

이처럼 객체 메서드 안에서 비동기 콜백을 작성할 때 화살표 함수가 유용할 수 있다.

---

## 18. 동기와 비동기

### 동기

동기(Synchronous)는 작업이 순서대로 하나씩 실행되는 방식이다.

앞 작업이 끝나야 다음 작업을 실행한다.

```text
작업 1 완료 → 작업 2 실행 → 작업 3 실행
```

### 비동기

비동기(Asynchronous)는 시간이 오래 걸리는 작업을 기다리는 동안 다음 코드를 먼저 실행할 수 있는 방식이다.

```text
작업 1 시작
작업 2 실행
작업 1이 나중에 완료되면 콜백 실행
```

비동기가 필요한 대표적인 작업은 다음과 같다.

- 서버에서 데이터 가져오기
- 파일 읽기
- 이미지 로딩
- 타이머
- 사용자 이벤트 처리

---

## 19. 콜백 함수

콜백 함수는 다른 함수의 인자로 전달되어 나중에 실행되는 함수다.

```javascript
function greet(name, callback) {
    console.log("안녕, " + name + "!")
    callback()
}

function sayBye() {
    console.log("빠이~")
}

greet("김사과", sayBye)
```

### 출력 결과

```text
안녕, 김사과!
빠이~
```

### 화살표 함수를 콜백으로 사용

```javascript
function doSomething(callback) {
    console.log("작업 시작!")
    callback()
}

doSomething(() => {
    console.log("작업 완료")
})
```

### 출력 결과

```text
작업 시작!
작업 완료
```

---

## 20. 배열 메서드와 콜백

배열 메서드에서도 콜백 함수를 자주 사용한다.

```javascript
const numbers = [1, 2, 3, 4]
const doubled = numbers.map(n => n * 2)

console.log(doubled)
```

### 출력 결과

```text
[2, 4, 6, 8]
```

`map()`은 배열의 각 요소를 콜백 함수로 가공해 새 배열을 반환한다.

---

## 21. 함수를 전달하는 계산기 예제

함수를 값처럼 전달하면 계산 방식만 바꿔 재사용할 수 있다.

```javascript
const calcAdd = (a, b) => a + b
const calcMultiply = (a, b) => a * b

function calculator(num1, num2, action) {
    if (num1 < 0 || num2 < 0) return

    const result = action(num1, num2)
    return result
}

console.log(calculator(10, 3, calcMultiply))
console.log(calculator(10, 3, calcAdd))
```

### 출력 결과

```text
30
13
```

`calculator()`는 덧셈인지 곱셈인지 직접 알 필요가 없다. 세 번째 인자로 전달된 함수 `action`을 실행할 뿐이다.

---

## 22. 이벤트

이벤트(Event)는 사용자가 웹 페이지와 상호작용할 때 발생하는 특정 동작이나 상황이다.

예시는 다음과 같다.

- 버튼 클릭
- 키보드 입력
- 마우스 이동
- 폼 제출
- 브라우저 창 크기 변경
- 스크롤

이벤트를 처리하려면 특정 요소에 이벤트 리스너를 등록한다.

```text
대상 요소 + 이벤트 종류 + 실행할 함수
```

---

## 23. 인라인 이벤트 방식

HTML 속성에 직접 이벤트 함수를 작성할 수 있다.

```html
<button type="button" onclick="sayHello()">인사하기</button>
```

```javascript
function sayHello() {
    alert("안녕하세요!")
}
```

간단한 예제에서는 사용할 수 있지만, HTML과 JavaScript가 섞이기 때문에 코드가 많아지면 관리하기 어렵다.

---

## 24. `addEventListener()`

`addEventListener()`는 JavaScript에서 이벤트를 등록하는 대표적인 방법이다.

```html
<button type="button" id="eventBtn">이벤트 리스너 사용</button>
```

```javascript
const eventBtn = document.getElementById("eventBtn")

eventBtn.addEventListener("click", function () {
    alert("addEventListener로 연결된 이벤트!")
})
```

같은 요소에 여러 이벤트를 등록할 수 있다.

```javascript
eventBtn.addEventListener("mouseenter", function () {
    eventBtn.style.backgroundColor = "deeppink"
})

eventBtn.addEventListener("mouseleave", function () {
    eventBtn.style.backgroundColor = "deepskyblue"
})
```

---

## 25. 이벤트 종류

### 마우스 이벤트

| 이벤트 | 설명 |
| --- | --- |
| `click` | 클릭했을 때 |
| `dblclick` | 더블 클릭했을 때 |
| `mousedown` | 마우스 버튼을 눌렀을 때 |
| `mouseup` | 마우스 버튼을 뗐을 때 |
| `mouseenter` | 마우스를 요소 위에 올렸을 때 |
| `mouseleave` | 요소에서 마우스가 벗어났을 때 |
| `mousemove` | 마우스를 움직일 때 |

### 키보드 이벤트

| 이벤트 | 설명 |
| --- | --- |
| `keydown` | 키를 누르는 순간 |
| `keyup` | 키를 눌렀다 뗐을 때 |
| `keypress` | 문자 키 입력 시 발생했지만 현재는 사용을 권장하지 않음 |

### 폼 이벤트

| 이벤트 | 설명 |
| --- | --- |
| `submit` | 폼이 제출될 때 |
| `input` | 입력값이 변경될 때 |
| `change` | 입력이 끝나고 값이 변경되었을 때 |
| `focus` | 입력창에 포커스가 생겼을 때 |
| `blur` | 입력창에서 포커스가 사라졌을 때 |

### 문서와 브라우저 이벤트

| 이벤트 | 설명 |
| --- | --- |
| `load` | 페이지가 모두 로드되었을 때 |
| `resize` | 브라우저 크기가 변경될 때 |
| `scroll` | 페이지를 스크롤할 때 |

### 터치와 드래그 이벤트

| 이벤트 | 설명 |
| --- | --- |
| `touchstart` | 화면을 터치했을 때 |
| `touchmove` | 터치한 채 움직일 때 |
| `touchend` | 터치를 뗐을 때 |
| `dragstart` | 드래그를 시작할 때 |
| `drag` | 드래그 중일 때 |
| `dragend` | 드래그가 끝났을 때 |

---

## 26. 이벤트 객체

이벤트가 발생하면 브라우저는 이벤트 정보를 담은 객체를 자동으로 이벤트 핸들러에 전달한다.

이 객체를 보통 `event` 또는 `e`라고 부른다.

```html
<div id="clickArea">여기를 클릭하세요</div>
```

```javascript
document.getElementById("clickArea").addEventListener("click", function (event) {
    alert(
        `클릭한 위치의 좌표: X=${event.clientX}, Y=${event.clientY}\n` +
        `이벤트 타입: ${event.type}\n` +
        `이벤트 대상: ${event.target.id}`
    )
})
```

이벤트 객체에서 자주 사용하는 정보는 다음과 같다.

| 속성 | 설명 |
| --- | --- |
| `event.type` | 발생한 이벤트 종류 |
| `event.target` | 이벤트가 발생한 요소 |
| `event.clientX` | 브라우저 화면 기준 마우스 X 좌표 |
| `event.clientY` | 브라우저 화면 기준 마우스 Y 좌표 |
| `event.key` | 입력된 키 |
| `event.code` | 키보드의 물리적 키 코드 |

---

## 27. 키보드 이벤트

```html
<input type="text" id="inputBox" placeholder="키보드를 눌러보세요.">
```

```javascript
document.getElementById("inputBox").addEventListener("keydown", function (event) {
    console.log("입력된 키:", event.key)
    console.log("코드:", event.code)
    console.log("이벤트가 발생한 요소:", event.target)
})
```

입력창에서 키를 누르면 어떤 키를 눌렀는지 콘솔에서 확인할 수 있다.

### Enter 기본 동작 막기

폼 안에서 Enter를 누르면 기본적으로 폼 제출이 발생할 수 있다.

기본 동작을 막고 싶다면 `event.preventDefault()`를 사용한다.

```javascript
document.getElementById("inputBox").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault()
        alert("엔터키는 막았어요")
    }
})
```

---

## 28. 폼 안의 버튼 주의점

`form` 안에 있는 `<button>`은 기본 타입이 `submit`이다.

따라서 단순히 클릭 이벤트만 처리하고 싶다면 `type="button"`을 명시하는 것이 좋다.

```html
<form action="./result">
    <button type="button" onclick="sayHello()">인사하기</button>
    <button type="button" id="eventBtn">이벤트 리스너 사용</button>
</form>
```

폼 제출 자체를 제어하고 싶다면 `submit` 이벤트에서 기본 동작을 막는다.

```javascript
const form = document.querySelector("form")

form.addEventListener("submit", function (event) {
    event.preventDefault()
    console.log("폼 제출을 막고 JavaScript로 처리합니다.")
})
```

---

## 29. 전체 연결 예제

BOM, DOM, 콜백 함수와 이벤트를 한 번에 연결하면 다음과 같은 흐름이 된다.

```html
<p id="info">버튼을 눌러 브라우저 정보를 확인하세요.</p>
<button type="button" id="infoBtn">브라우저 정보 보기</button>
```

```javascript
const info = document.getElementById("info")
const infoBtn = document.getElementById("infoBtn")

infoBtn.addEventListener("click", () => {
    const width = window.innerWidth
    const height = window.innerHeight
    const language = navigator.language

    info.innerText = `창 크기: ${width} x ${height}, 언어: ${language}`
})
```

### 동작 흐름

```text
사용자가 버튼 클릭
        ↓
click 이벤트 발생
        ↓
화살표 함수 콜백 실행
        ↓
window, navigator에서 브라우저 정보 확인
        ↓
DOM 요소의 innerText 변경
```

---

## 30. 핵심 정리

### BOM

- BOM은 브라우저 자체를 다루는 객체 모델이다.
- `window`는 브라우저의 최상위 객체다.
- `location`은 URL 정보를 확인하거나 페이지를 이동할 때 사용한다.
- `history`는 뒤로 가기와 앞으로 가기 같은 방문 기록을 제어한다.
- `navigator`는 브라우저와 사용자 환경 정보를 제공한다.

### DOM

- DOM은 HTML 문서를 객체로 표현한 구조다.
- `document` 객체를 통해 HTML 요소를 선택하고 조작한다.
- `innerText`는 텍스트를 변경한다.
- `innerHTML`은 HTML 태그를 포함해 변경할 수 있다.
- `createElement()`, `appendChild()`, `removeChild()`로 요소를 추가하거나 삭제한다.

### 화살표 함수와 콜백

- 화살표 함수는 `=>`를 사용해 함수를 간결하게 작성한다.
- 화살표 함수는 자신만의 `this`를 만들지 않는다.
- 콜백 함수는 다른 함수에 전달되어 나중에 실행된다.
- 비동기 작업이나 이벤트 처리에서 콜백이 자주 사용된다.

### 이벤트

- 이벤트는 사용자의 동작이나 브라우저 상태 변화다.
- `addEventListener()`로 이벤트를 등록한다.
- 이벤트 객체에는 이벤트 타입, 대상 요소, 마우스 좌표, 키 입력 정보 등이 들어 있다.
- 폼 안의 버튼은 기본적으로 제출 동작을 할 수 있으므로 `type="button"` 또는 `preventDefault()`를 적절히 사용한다.
