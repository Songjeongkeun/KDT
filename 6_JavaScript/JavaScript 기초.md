# JavaScript 기초: 실행 방법, 콘솔 출력, 변수와 자료형

JavaScript는 HTML과 CSS로 만든 웹 페이지에 동적인 기능을 추가하는 프로그래밍 언어다.

버튼 클릭 처리, 입력값 검사, 화면 내용 변경, 애니메이션 제어, 서버와의 데이터 통신 등에 사용한다. 현재는 웹 브라우저뿐만 아니라 Node.js를 이용한 서버 개발, 모바일·데스크톱 애플리케이션 개발 등에도 활용한다.

---

## 1. JavaScript란?

웹 페이지를 구성하는 대표적인 세 가지 기술은 다음과 같다.

| 기술 | 역할 |
| --- | --- |
| HTML | 웹 페이지의 구조를 만든다 |
| CSS | 색상, 크기, 배치 등 화면을 꾸민다 |
| JavaScript | 사용자와 상호작용하고 동작을 처리한다 |

예를 들어 사용자가 버튼을 클릭했을 때 내용을 변경하거나 입력값이 올바른지 검사하려면 JavaScript가 필요하다.

```text
HTML       → 웹 페이지의 뼈대
CSS        → 웹 페이지의 디자인
JavaScript → 웹 페이지의 동작
```

---

## 2. JavaScript의 역사

### 2.1 JavaScript의 탄생

JavaScript는 1995년 Netscape에서 근무하던 브렌던 아이크(Brendan Eich)가 웹 페이지에 동적인 기능을 추가하기 위해 개발했다.

초기 이름은 다음과 같이 변경되었다.

```text
Mocha → LiveScript → JavaScript
```

JavaScript와 Java는 이름이 비슷하지만 서로 다른 프로그래밍 언어다.

### 2.2 표준화

브라우저마다 JavaScript의 동작 방식이 달라지는 문제를 줄이기 위해 ECMA International에서 표준화 작업을 진행했다.

이 표준 명세를 **ECMAScript**라고 한다. JavaScript는 ECMAScript 표준을 구현하는 대표적인 프로그래밍 언어다.

### 2.3 모던 JavaScript

2009년 Node.js가 등장하면서 JavaScript를 웹 브라우저 밖에서도 실행할 수 있게 되었다.

2015년에는 ES6 또는 ECMAScript 2015가 발표되었다. ES6에는 현재 자주 사용하는 다음 기능들이 추가되었다.

- `let`
- `const`
- `class`
- 화살표 함수
- 템플릿 리터럴
- 구조 분해 할당

---

## 3. JavaScript 실행 과정

브라우저는 HTML 문서를 위에서 아래로 읽으며 웹 페이지의 구조를 해석한다. 이 과정을 **파싱(Parsing)**이라고 한다.

일반적인 `<script>` 태그를 만나면 다음 순서로 처리한다.

```text
HTML 파싱
   ↓
<script> 태그 발견
   ↓
JavaScript 다운로드 또는 코드 확인
   ↓
JavaScript 실행
   ↓
HTML 파싱 재개
```

외부 JavaScript 파일을 일반적인 `<script src="...">` 방식으로 불러오면 다운로드와 실행 과정에서 HTML 파싱이 잠시 멈출 수 있다.

따라서 기초 예제에서는 `<script>` 태그를 `</body>` 바로 앞에 작성하는 방법을 자주 사용한다.

```html
<body>
    <h1>JavaScript 예제</h1>

    <script src="./js/script.js"></script>
</body>
```

> `defer` 속성을 사용하면 HTML 파싱과 JavaScript 파일 다운로드를 함께 진행하고, HTML 파싱이 끝난 뒤 스크립트를 실행할 수 있다.

```html
<head>
    <script src="./js/script.js" defer></script>
</head>
```

---

## 4. 콘솔 출력

`console.log()`는 값을 브라우저 개발자 도구의 Console에 출력하는 함수다.

변수의 값이나 프로그램의 실행 흐름을 확인할 때 사용한다.

### 예제

```html
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>콘솔 출력</title>
</head>

<body>
    <h1>콘솔 출력</h1>

    <script>
        console.log("안녕하세요. 자바스크립트입니다.")
        console.log("현재 페이지가 정상적으로 로드되었습니다.")
    </script>
</body>

</html>
```

### 출력 결과

```text
안녕하세요. 자바스크립트입니다.
현재 페이지가 정상적으로 로드되었습니다.
```

### 브라우저 콘솔 확인 방법

1. HTML 파일을 브라우저에서 연다.
2. 개발자 도구를 실행한다.
3. `Console` 탭을 선택한다.

Chrome에서는 보통 `F12` 또는 다음 단축키를 사용한다.

```text
Windows: Ctrl + Shift + J
macOS:   Command + Option + J
```

---

## 5. JavaScript 작성 방법

JavaScript는 HTML 문서 안에 직접 작성하거나 별도의 `.js` 파일로 분리할 수 있다.

### 5.1 내부 JavaScript

HTML의 `<script>` 태그 안에 JavaScript 코드를 작성한다.

```html
<script>
    console.log("내부 JavaScript")
</script>
```

간단한 예제를 작성할 때 편리하지만 코드가 길어지면 HTML 문서가 복잡해질 수 있다.

### 5.2 외부 JavaScript

JavaScript 코드를 별도의 `.js` 파일로 작성하고 HTML에서 불러온다.

#### HTML

```html
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>외부 JavaScript</title>
</head>

<body>
    <h1>외부 JavaScript</h1>

    <script src="./js/script.js"></script>
</body>

</html>
```

#### `js/script.js`

```javascript
console.log("외부 자바스크립트 파일이 실행되었습니다.")
console.log("HTML과 JavaScript가 분리되어 있습니다.")
```

### 출력 결과

```text
외부 자바스크립트 파일이 실행되었습니다.
HTML과 JavaScript가 분리되어 있습니다.
```

### 외부 파일을 사용하는 이유

- HTML과 JavaScript의 역할을 분리할 수 있다.
- 코드의 가독성과 유지보수성이 좋아진다.
- 하나의 JavaScript 파일을 여러 HTML에서 재사용할 수 있다.
- 파일별로 기능을 나누어 관리할 수 있다.

`src`에 작성하는 경로는 HTML 파일을 기준으로 한다.

```text
프로젝트/
├── js/
│   └── script.js
└── index.html
```

위 구조에서는 다음과 같이 연결한다.

```html
<script src="./js/script.js"></script>
```

---

## 6. 변수

변수(Variable)는 프로그램에서 사용하는 값을 저장하기 위해 이름을 붙인 공간이다.

JavaScript에서는 주로 `let`과 `const`를 사용해 변수를 선언한다.

```javascript
let age
let name
```

### 6.1 변수 선언과 값 할당

변수를 만드는 것을 **선언**, 변수에 값을 저장하는 것을 **할당**이라고 한다.

```javascript
// 변수 선언
let age
let name

// 값 할당
age = 20
name = "김사과"
```

선언과 할당을 동시에 할 수도 있다.

```javascript
let age = 20
let name = "김사과"
```

처음 값을 저장하는 것은 **초기화**라고도 한다.

### 6.2 변수 이름 작성 규칙

JavaScript 변수 이름은 다음 규칙을 지켜야 한다.

- 문자, 숫자, `_`, `$`를 사용할 수 있다.
- 숫자로 시작할 수 없다.
- 공백을 사용할 수 없다.
- 예약어를 사용할 수 없다.
- 대문자와 소문자를 구분한다.

```javascript
let userName
let user_name
let $price
let score1
```

다음 변수 이름은 사용할 수 없다.

```javascript
// let 1score     // 숫자로 시작
// let user name  // 공백 포함
// let const      // 예약어 사용
```

JavaScript에서는 여러 단어로 된 변수 이름에 카멜 표기법(camelCase)을 주로 사용한다.

```javascript
let userName
let totalPrice
let isStudent
```

---

## 7. `let`, `const`, `var`

### 7.1 `let`

`let`으로 선언한 변수는 값을 다시 할당할 수 있다.

```javascript
let age = 20
console.log(age)

age = 25
console.log(age)
```

### 출력 결과

```text
20
25
```

같은 범위에서 동일한 이름으로 다시 선언할 수는 없다.

```javascript
let age = 20
// let age = 30  // SyntaxError
```

### 7.2 `const`

`const`는 선언할 때 반드시 값을 할당해야 하며, 이후 다른 값을 다시 할당할 수 없다.

```javascript
const PI = 3.14
console.log(PI)

// PI = 3.14159  // TypeError
```

변경할 필요가 없는 값은 `const`로 선언하는 것이 좋다.

> `const` 객체와 배열은 객체 자체를 다른 값으로 재할당할 수 없다는 의미다. 객체 내부의 속성이나 배열 요소까지 모두 변경할 수 없는 것은 아니다.

```javascript
const user = { name: "김사과" }
user.name = "반하나"

console.log(user.name)
```

```text
반하나
```

### 7.3 `var`

`var`는 이전 JavaScript 코드에서 많이 사용하던 변수 선언 키워드다.

```javascript
var score = 90
console.log("점수:", score)

var score = 100
console.log("점수:", score)
```

### 출력 결과

```text
점수: 90
점수: 100
```

`var`는 같은 범위에서 중복 선언을 허용하고 함수 스코프를 사용한다. 선언이 끌어올려지는 호이스팅 동작 때문에 코드의 흐름을 예측하기 어려워질 수 있다.

현대 JavaScript에서는 다음 기준으로 선언하는 것이 일반적이다.

```text
기본적으로 const를 사용한다.
값을 다시 할당해야 한다면 let을 사용한다.
var의 사용은 가급적 피한다.
```

### 7.4 선언하지 않은 변수

다음 코드는 변수 선언 키워드 없이 값을 할당한다.

```javascript
message = "안녕하세요"
console.log(message)
```

이 코드는 느슨한 모드에서 전역 객체의 속성을 만들 수 있지만, `var` 변수가 자동으로 선언되는 것은 아니다.

엄격 모드에서는 오류가 발생한다.

```javascript
"use strict"

message = "안녕하세요"  // ReferenceError
```

따라서 변수는 반드시 `const` 또는 `let`으로 선언해야 한다.

```javascript
const message = "안녕하세요"
```

### 7.5 비교 정리

| 구분 | `let` | `const` | `var` |
| --- | --- | --- | --- |
| 재할당 | 가능 | 불가능 | 가능 |
| 중복 선언 | 불가능 | 불가능 | 가능 |
| 스코프 | 블록 스코프 | 블록 스코프 | 함수 스코프 |
| 선언 전 접근 | 오류 발생 | 오류 발생 | `undefined` |
| 권장 여부 | 필요할 때 사용 | 우선 사용 | 가급적 사용하지 않음 |

---

## 8. 변수 예제

```javascript
let age = 20
let name = "김사과"
const PI = 3.14

console.log(age)
console.log(name)
console.log(PI)

age = 25
name = "반하나"

console.log(age)
console.log(name)

var score = 90
console.log("점수:", score)

var score = 100
console.log("점수:", score)

const message = "안녕하세요"
console.log(message)
```

### 출력 결과

```text
20
김사과
3.14
25
반하나
점수: 90
점수: 100
안녕하세요
```

---

## 9. 자료형

자료형(Data Type)은 변수에 저장된 값의 종류를 의미한다.

JavaScript의 자료형은 크게 **원시 타입(Primitive Type)**과 **참조 타입(Reference Type)**으로 나눌 수 있다.

### 원시 타입

- Number
- String
- Boolean
- Undefined
- Null
- BigInt
- Symbol

### 참조 타입

- Object
- Array
- Function

이번 내용에서는 원시 타입을 중심으로 살펴본다.

---

## 10. 원시 타입

원시 타입은 하나의 값을 표현하는 기본 자료형이다.

### 10.1 Number

`Number`는 정수, 실수, 양수와 음수를 모두 표현한다.

```javascript
let age = 20
let price = 3.14
let temperature = -5
```

```javascript
console.log(typeof age)
console.log(typeof price)
```

```text
number
number
```

JavaScript는 일반적인 정수와 실수를 별도의 자료형으로 구분하지 않고 `number`로 처리한다.

### 10.2 String

`String`은 문자열을 표현하는 자료형이다.

큰따옴표, 작은따옴표 또는 백틱을 사용할 수 있다.

```javascript
let name1 = "김사과"
let name2 = '반하나'
let name3 = `오렌지`
```

백틱을 사용하면 문자열 안에 변수나 표현식을 쉽게 넣을 수 있다.

```javascript
const name = "김사과"
const age = 20

console.log(`${name}님의 나이는 ${age}세입니다.`)
```

```text
김사과님의 나이는 20세입니다.
```

`String()`은 전달받은 값을 문자열 원시값으로 변환한다.

```javascript
const value = String(100)

console.log(value)
console.log(typeof value)
```

```text
100
string
```

`String("김사과")`가 객체를 생성하는 것은 아니다. 명시적인 문자열 객체는 `new String()`으로 만들 수 있지만 일반적으로 사용하지 않는다.

### 10.3 Boolean

`Boolean`은 참과 거짓을 표현한다.

```javascript
let isStudent = true
let isLogin = false
```

조건문이나 반복문의 실행 여부를 판단할 때 자주 사용한다.

```javascript
console.log(typeof isStudent)
```

```text
boolean
```

### 10.4 Undefined

변수를 선언했지만 값을 할당하지 않으면 `undefined`가 자동으로 저장된다.

```javascript
let result

console.log(result)
console.log(typeof result)
```

```text
undefined
undefined
```

`undefined`는 아직 값이 정해지지 않은 상태를 의미한다.

### 10.5 Null

`null`은 개발자가 의도적으로 값이 없음을 표현할 때 사용한다.

```javascript
let data = null

console.log(data)
console.log(typeof data)
```

```text
null
object
```

`typeof null`의 결과는 `"object"`다. 하지만 `null`은 실제 객체가 아니라 원시값이며, 이 결과는 JavaScript 초기 설계에서 비롯된 오래된 특성이다.

값이 `null`인지 확인할 때는 직접 비교한다.

```javascript
console.log(data === null)
```

```text
true
```

### 10.6 BigInt

`BigInt`는 `Number`가 안전하게 표현할 수 있는 범위를 넘어서는 큰 정수를 다룰 때 사용한다.

`Number`가 안전하게 표현할 수 있는 가장 큰 정수는 다음과 같다.

```javascript
console.log(Number.MAX_SAFE_INTEGER)
```

```text
9007199254740991
```

정수 뒤에 `n`을 붙이면 `BigInt`가 된다.

```javascript
const bigNumber = 1234567890123456789n

console.log(bigNumber)
console.log(typeof bigNumber)
```

```text
1234567890123456789n
bigint
```

`BigInt`와 `Number`를 그대로 섞어 계산할 수는 없다.

```javascript
const bigNumber = 10n
const number = 5

// console.log(bigNumber + number)  // TypeError
```

자료형을 맞춘 뒤 계산해야 한다.

```javascript
console.log(bigNumber + BigInt(number))
```

```text
15n
```

---

## 11. `typeof` 연산자

`typeof`는 값이나 변수의 자료형을 문자열로 반환하는 연산자다.

```javascript
console.log(typeof 20)
console.log(typeof "김사과")
console.log(typeof true)
console.log(typeof undefined)
console.log(typeof null)
console.log(typeof 10n)
```

### 출력 결과

```text
number
string
boolean
undefined
object
bigint
```

주요 결과를 정리하면 다음과 같다.

| 값 | `typeof` 결과 |
| --- | --- |
| `20` | `"number"` |
| `"김사과"` | `"string"` |
| `true` | `"boolean"` |
| `undefined` | `"undefined"` |
| `null` | `"object"` |
| `10n` | `"bigint"` |

---

## 12. 원시 타입 전체 예제

```html
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>자료형</title>
</head>

<body>
    <h1>원시 타입 예제</h1>

    <script>
        let age = 20
        let name = "김사과"
        let isStudent = true
        let result
        let data = null

        console.log("age:", age, typeof age)
        console.log("name:", name, typeof name)
        console.log("isStudent:", isStudent, typeof isStudent)
        console.log("result:", result, typeof result)
        console.log("data:", data, typeof data)
        console.log("MAX_SAFE_INTEGER:", Number.MAX_SAFE_INTEGER)
    </script>
</body>

</html>
```

### 출력 결과

```text
age: 20 number
name: 김사과 string
isStudent: true boolean
result: undefined undefined
data: null object
MAX_SAFE_INTEGER: 9007199254740991
```

---

## 13. 핵심 정리

### JavaScript 실행

- JavaScript는 `<script>` 태그 안에 작성할 수 있다.
- 외부 `.js` 파일로 분리하면 코드 관리와 재사용이 편리하다.
- `console.log()`를 사용해 실행 결과와 변수 값을 확인한다.

### 변수

- 변경하지 않을 값은 `const`로 선언한다.
- 다시 할당해야 하는 값은 `let`으로 선언한다.
- `var`는 중복 선언과 함수 스코프 등의 특징 때문에 가급적 사용하지 않는다.
- 선언 키워드 없이 변수를 사용하지 않는다.

### 자료형

- JavaScript는 값에 따라 변수의 자료형이 결정되는 동적 타입 언어다.
- `typeof` 연산자로 값의 자료형을 확인할 수 있다.
- `undefined`는 값이 할당되지 않은 상태다.
- `null`은 값이 없음을 의도적으로 표현한 값이다.
- 큰 정수는 `BigInt`로 표현한다.

```javascript
const language = "JavaScript"
let version = 2026

console.log(language, typeof language)
console.log(version, typeof version)
```

JavaScript의 기본 문법을 학습할 때는 단순히 코드를 실행하는 것에서 끝내지 않고, 각 값의 자료형과 변수의 변경 가능 여부를 함께 확인하는 것이 중요하다.
