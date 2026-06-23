# JavaScript 정규식과 회원가입 폼 검증 정리

정규식은 문자열이 특정한 규칙을 만족하는지 검사할 때 사용하는 표현식이다.

회원가입 페이지에서는 아이디, 비밀번호, 이름, 휴대폰 번호, 이메일처럼 입력 형식이 정해진 값을 검증할 때 정규식을 자주 사용한다.

이번 글에서는 다음 흐름으로 정리한다.

```text
정규식 기본 문법
        ↓
정규식 메서드
        ↓
이메일·휴대폰 번호 검사
        ↓
회원가입 폼 구조
        ↓
JavaScript 입력 검증
        ↓
주민등록번호 검증 로직
        ↓
주소 검색 API 연결
```

---

## 1. 정규식이란?

정규식(Regular Expression)은 문자열에서 특정 패턴을 찾거나 검사하거나 치환하기 위해 사용하는 표현식이다.

예를 들어 다음과 같은 작업을 할 수 있다.

- 문자열이 숫자로만 이루어져 있는지 확인한다.
- 이메일 형식이 맞는지 확인한다.
- 휴대폰 번호 형식이 맞는지 확인한다.
- 문자열에서 특정 문자를 찾아 제거한다.
- 문자열에서 원하는 패턴만 추출한다.

---

## 2. 정규식 작성 방법

JavaScript에서 정규식을 만드는 방법은 두 가지다.

### 2.1 정규식 리터럴

```javascript
const reg = /^[0-9]+$/
```

슬래시 `/ /` 안에 패턴을 작성한다.

### 2.2 `RegExp` 생성자

```javascript
const reg = new RegExp("^[0-9]+$")
```

문자열로 패턴을 전달해 정규식을 만든다.

일반적으로 직접 작성하는 정규식은 리터럴 방식을 많이 사용한다.

---

## 3. 정규식 기본 구조

```javascript
/패턴/옵션
```

예시는 다음과 같다.

```javascript
const regex = /^[A-Za-z0-9]+$/i
```

| 구분 | 의미 |
| --- | --- |
| `/ /` | 정규식의 시작과 끝 |
| `^[A-Za-z0-9]+$` | 검사할 패턴 |
| `i` | 옵션 |

---

## 4. 자주 사용하는 정규식 패턴

| 패턴 | 의미 |
| --- | --- |
| `a` | 문자 `a` |
| `abc` | 문자열 `abc` |
| `.` | 아무 문자 1개 |
| `[abc]` | `a`, `b`, `c` 중 하나 |
| `[a-z]` | 알파벳 소문자 `a`부터 `z` |
| `[A-Z]` | 알파벳 대문자 `A`부터 `Z` |
| `[가-힣]` | 한글 음절 범위 |
| `[0-9]` | 숫자 |
| `[^0-9]` | 숫자가 아닌 문자 |
| `*` | 0번 이상 반복 |
| `+` | 1번 이상 반복 |
| `{n}` | 정확히 n번 반복 |
| `{n,}` | n번 이상 반복 |
| `{n,m}` | n번 이상 m번 이하 반복 |
| `^` | 문자열 시작 |
| `$` | 문자열 끝 |
| `\d` | 숫자 |
| `\D` | 숫자가 아닌 문자 |
| `\w` | 문자, 숫자, `_` |
| `\W` | 문자, 숫자, `_`가 아닌 문자 |
| `\s` | 공백 문자 |
| `\S` | 공백이 아닌 문자 |

---

## 5. 정규식 옵션

| 옵션 | 의미 |
| --- | --- |
| `g` | 전체 검색 |
| `i` | 대소문자 구분 없음 |
| `m` | 여러 줄 처리 |

### 예제

```javascript
const text = "Apple apple APPLE"

console.log(text.match(/apple/))
console.log(text.match(/apple/i))
console.log(text.match(/apple/gi))
```

### 출력 결과

```text
["apple"]
["Apple"]
["Apple", "apple", "APPLE"]
```

`i` 옵션은 대소문자를 무시하고, `g` 옵션은 일치하는 값을 전체 검색한다.

---

## 6. 정규식 메서드

### 6.1 `test()`

`test()`는 문자열이 패턴을 만족하는지 검사하고 `true` 또는 `false`를 반환한다.

```javascript
const reg = /^[0-9]+$/

console.log(reg.test("a123"))
console.log(reg.test("1234"))
```

### 출력 결과

```text
false
true
```

### 6.2 `match()`

`match()`는 문자열에서 정규식과 일치하는 결과를 반환한다.

```javascript
const result = "abc123".match(/\d+/)

console.log(result)
```

### 출력 결과

```text
["123"]
```

`\d+`는 숫자가 1개 이상 연속되는 패턴이다.

### 6.3 `replace()`

`replace()`는 정규식과 일치하는 문자열을 다른 문자열로 치환한다.

```javascript
const phone = "010-1234-5678"
const result = phone.replace(/-/g, "")

console.log(result)
```

### 출력 결과

```text
01012345678
```

`/-/g`는 문자열 전체에서 `-`를 모두 찾는다는 의미다.

### 6.4 `search()`

`search()`는 정규식과 일치하는 위치의 인덱스를 반환한다.

```javascript
console.log("hello".search(/e/))
```

### 출력 결과

```text
1
```

인덱스는 0부터 시작한다.

---

## 7. 이메일과 휴대폰 번호 검사

### HTML

```html
<button id="checkBtn">검색하기</button>
```

### JavaScript

```javascript
document.getElementById("checkBtn").addEventListener("click", function () {
    const email = "apple@apple.com"
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    console.log("이메일 검사:", emailRegex.test(email))

    const phone = "010-1234-5678"
    const phoneRegex = /^010-\d{3,4}-\d{4}$/

    console.log("휴대폰 번호 검사:", phoneRegex.test(phone))
})
```

### 출력 결과

```text
이메일 검사: true
휴대폰 번호 검사: true
```

### 이메일 정규식 분석

```javascript
/^[^\s@]+@[^\s@]+\.[^\s@]+$/
```

| 부분 | 의미 |
| --- | --- |
| `^` | 문자열 시작 |
| `[^\s@]+` | 공백과 `@`가 아닌 문자가 1개 이상 |
| `@` | `@` 문자 |
| `[^\s@]+` | 공백과 `@`가 아닌 문자가 1개 이상 |
| `\.` | 점 `.` 문자 |
| `[^\s@]+` | 공백과 `@`가 아닌 문자가 1개 이상 |
| `$` | 문자열 끝 |

### 휴대폰 번호 정규식 분석

```javascript
/^010-\d{3,4}-\d{4}$/
```

| 부분 | 의미 |
| --- | --- |
| `^010-` | `010-`으로 시작 |
| `\d{3,4}` | 숫자 3자리 또는 4자리 |
| `-` | 하이픈 |
| `\d{4}` | 숫자 4자리 |
| `$` | 문자열 끝 |

---

## 8. 회원가입 페이지 구조

회원가입 페이지는 사용자가 입력한 정보를 서버로 보내기 전 JavaScript로 먼저 검사한다.

```html
<form action="/regist" method="post" onsubmit="return sendit()">
    <input type="hidden" name="ssncheck" id="ssncheck" value="n">

    <p>아이디:
        <input type="text" name="userid" id="userid" maxlength="20" placeholder="아이디를 입력하세요.">
    </p>

    <p>비밀번호:
        <input type="password" name="userpw" id="userpw" maxlength="20" placeholder="비밀번호를 입력하세요.">
    </p>

    <p>비밀번호 확인:
        <input type="password" name="userpw_re" id="userpw_re" maxlength="20" placeholder="비밀번호를 다시 한번 입력하세요.">
    </p>

    <p>이름:
        <input type="text" name="name" id="name" maxlength="10" placeholder="이름을 입력하세요.">
    </p>

    <p>휴대폰번호:
        <input type="text" name="hp" id="hp" maxlength="20" placeholder="휴대폰 번호를 입력하세요 (- 포함)">
    </p>

    <p>이메일:
        <input type="email" name="email" id="email" maxlength="50" placeholder="이메일을 입력하세요.">
    </p>

    <p>주민등록번호:
        <input type="text" name="ssn1" id="ssn1" maxlength="6" placeholder="주민번호 앞자리" class="ssn">
        -
        <input type="password" name="ssn2" id="ssn2" maxlength="7" placeholder="주민번호 뒷자리" class="ssn">
        <button type="button" onclick="return checkSsn()">인증</button>
    </p>

    <p>우편번호:
        <input type="text" name="zipcode" id="sample6_postcode" maxlength="5" placeholder="우편번호를 입력하세요.">
        <button type="button" onclick="sample6_execDaumPostcode()">검색</button>
    </p>

    <p>주소:
        <input type="text" name="address1" id="sample6_address" placeholder="주소를 입력하세요">
    </p>

    <p>상세 주소:
        <input type="text" name="address2" id="sample6_detailAddress" placeholder="상세 주소를 입력하세요">
    </p>

    <p>참고 항목:
        <input type="text" name="address3" id="sample6_extraAddress" placeholder="참고 항목을 입력하세요">
    </p>

    <p>
        <button type="submit">가입완료</button>
        <button type="reset">다시작성</button>
    </p>
</form>
```

`onsubmit="return sendit()"`은 폼이 제출되기 전에 `sendit()` 함수를 실행한다.

```text
sendit()이 true 반환  → 폼 제출
sendit()이 false 반환 → 폼 제출 중단
```

---

## 9. 페이지 로드 후 이벤트 등록

`window.onload`는 페이지가 모두 로드된 뒤 실행된다.

```javascript
window.onload = function () {
    const ssn1 = document.getElementById("ssn1")

    ssn1.addEventListener("keyup", () => {
        if (ssn1.value.length >= 6) {
            document.getElementById("ssn2").focus()
        }
    })

    const ssn = document.querySelectorAll(".ssn")

    ssn.forEach((s) => {
        s.addEventListener("input", () => {
            document.getElementById("ssncheck").value = "n"
        })
    })
}
```

### 동작 흐름

```text
페이지 로드
    ↓
ssn1 요소 선택
    ↓
주민등록번호 앞자리 6자리 입력
    ↓
ssn2 입력칸으로 자동 포커스 이동
```

주민등록번호 입력값이 변경되면 hidden input인 `ssncheck` 값을 다시 `"n"`으로 바꾼다.

```text
주민등록번호 인증 완료 → ssncheck = "y"
주민등록번호 다시 수정 → ssncheck = "n"
```

이렇게 해야 사용자가 인증 후 주민등록번호를 수정했을 때 다시 인증하도록 만들 수 있다.

---

## 10. 회원가입 입력 검증 흐름

`sendit()` 함수는 회원가입 폼이 서버로 전송되기 전에 입력값을 검사한다.

```javascript
function sendit() {
    const userid = document.getElementById("userid")
    const userpw = document.getElementById("userpw")
    const userpw_re = document.getElementById("userpw_re")
    const name = document.getElementById("name")
    const hp = document.getElementById("hp")
    const email = document.getElementById("email")
    const ssncheck = document.getElementById("ssncheck")

    const expIdText = /^[A-Za-z0-9]{4,20}$/
    const expPwText = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$/
    const expNameText = /^[가-힣]+$/
    const expHpText = /^\d{3}-\d{3,4}-\d{4}$/
    const expEmailText = /^[A-Za-z0-9\-.]+@[A-Za-z0-9-]+\.[A-Za-z]+$/

    if (userid.value === "") {
        alert("아이디를 입력하세요")
        userid.focus()
        return false
    }

    if (!expIdText.test(userid.value)) {
        alert("아이디는 4자 이상 20자 이하의 영문자 또는 숫자로 입력하세요.")
        userid.focus()
        return false
    }

    if (!expPwText.test(userpw.value)) {
        alert("비밀번호는 8자 이상 20자 이하의 영문자, 숫자, 특수문자를 한 자 이상 꼭 포함해야 합니다.")
        userpw.focus()
        return false
    }

    if (userpw.value !== userpw_re.value) {
        alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        userpw_re.focus()
        return false
    }

    if (!expNameText.test(name.value)) {
        alert("이름은 한글로 입력하세요.")
        name.focus()
        return false
    }

    if (!expHpText.test(hp.value)) {
        alert("휴대폰 번호 형식이 일치하지 않습니다.\n하이픈을 꼭 입력하세요.")
        hp.focus()
        return false
    }

    if (!expEmailText.test(email.value)) {
        alert("이메일 형식이 일치하지 않습니다.")
        email.focus()
        return false
    }

    if (ssncheck.value === "n") {
        alert("주민등록번호 검증 버튼을 눌러주세요.")
        return false
    }

    return true
}
```

원본 코드의 `email.focue()`는 오타이므로 `email.focus()`로 작성해야 한다.

---

## 11. 회원가입 정규식 분석

### 11.1 아이디 검사

```javascript
/^[A-Za-z0-9]{4,20}$/
```

| 부분 | 의미 |
| --- | --- |
| `^` | 문자열 시작 |
| `[A-Za-z0-9]` | 영문 대소문자 또는 숫자 |
| `{4,20}` | 4자 이상 20자 이하 |
| `$` | 문자열 끝 |

허용 예시는 다음과 같다.

```text
apple
apple123
User2026
```

허용하지 않는 예시는 다음과 같다.

```text
ab
apple!
사과123
```

### 11.2 비밀번호 검사

```javascript
/^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$/
```

비밀번호 조건은 다음과 같다.

- 8자 이상 20자 이하
- 영문자 최소 1개 이상
- 숫자 최소 1개 이상
- 특수문자 `!@#$%^&*()` 중 최소 1개 이상
- 허용된 문자만 사용

### 긍정형 전방 탐색

```javascript
(?=.*[A-Za-z])
(?=.*\d)
(?=.*[!@#$%^&*()])
```

`(?=.*패턴)`은 문자열 어딘가에 해당 패턴이 최소 1개 이상 있어야 한다는 의미다.

| 패턴 | 의미 |
| --- | --- |
| `(?=.*[A-Za-z])` | 영문자가 최소 1개 이상 있어야 함 |
| `(?=.*\d)` | 숫자가 최소 1개 이상 있어야 함 |
| `(?=.*[!@#$%^&*()])` | 특수문자가 최소 1개 이상 있어야 함 |

허용 예시는 다음과 같다.

```text
apple123!
Test2026@
JavaScript1!
```

허용하지 않는 예시는 다음과 같다.

```text
apple123
12345678!
apple!!!!!
```

### 11.3 이름 검사

```javascript
/^[가-힣]+$/
```

한글만 입력할 수 있다.

```text
김사과  → 가능
apple   → 불가능
김사과1 → 불가능
```

### 11.4 휴대폰 번호 검사

```javascript
/^\d{3}-\d{3,4}-\d{4}$/
```

형식은 다음과 같다.

```text
010-1234-5678
010-123-4567
```

하이픈을 반드시 포함해야 한다.

### 11.5 이메일 검사

```javascript
/^[A-Za-z0-9\-.]+@[A-Za-z0-9-]+\.[A-Za-z]+$/
```

| 부분 | 의미 |
| --- | --- |
| `[A-Za-z0-9\-.]+` | 이메일 아이디 부분 |
| `@` | 이메일 구분 문자 |
| `[A-Za-z0-9-]+` | 도메인 이름 |
| `\.` | 점 문자 |
| `[A-Za-z]+` | 최상위 도메인 |

예시는 다음과 같다.

```text
apple@apple.com
test-2026@example.co
```

> 실제 서비스의 이메일 형식은 매우 다양하다. 학습용 정규식은 기본적인 형태를 검사하는 용도로 이해하는 것이 좋다.

---

## 12. 주민등록번호 검증 로직

주민등록번호 검증은 앞 12자리와 가중치를 곱해 검증 숫자를 계산한 뒤 마지막 숫자와 비교하는 방식이다.

예시 구조는 다음과 같다.

```text
주민번호 13자리
9 8 0 8 0 8 1 0 4 7 4 2 8

가중치 12자리
2 3 4 5 6 7 8 9 2 3 4 5
```

앞 12자리와 가중치를 각각 곱한 뒤 모두 더한다.

```text
18 + 24 + 0 + 40 + 0 + 56 + 8 + 0 + 8 + 21 + 16 + 10 = 201
201 % 11 = 3
11 - 3 = 8
```

계산 결과가 마지막 숫자와 같으면 유효한 번호로 판단한다.

---

## 13. 주민등록번호 검증 코드

```javascript
function checkSsn() {
    const ssncheck = document.getElementById("ssncheck")
    const ssn1 = document.getElementById("ssn1").value
    const ssn2 = document.getElementById("ssn2").value

    const ssn = ssn1 + ssn2.substring(0, 6)
    const cond = Number(ssn2[6])

    const weight = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]

    let check = 0

    for (let i = 0; i < ssn.length; i++) {
        check += Number(ssn[i]) * weight[i]
    }

    check = (11 - (check % 11)) % 10

    if (check !== cond) {
        alert("유효하지 않은 주민등록 번호입니다.")
    } else {
        alert("유효한 주민등록 번호입니다.")
        ssncheck.value = "y"
    }
}
```

### 코드 흐름

```text
ssn1, ssn2 값 가져오기
        ↓
앞 12자리 만들기
        ↓
가중치 배열과 각 자리 숫자를 곱함
        ↓
합계를 이용해 검증 숫자 계산
        ↓
마지막 자리와 비교
        ↓
일치하면 ssncheck 값을 "y"로 변경
```

### 주의할 점

실제 서비스에서 주민등록번호 같은 민감 정보를 클라이언트 JavaScript만으로 검증하거나 보관해서는 안 된다.

클라이언트 검증은 사용자의 편의를 위한 1차 검증일 뿐이다. 실제 검증과 저장은 반드시 서버에서 안전하게 처리해야 한다.

---

## 14. 다음 주소 API 연결

회원가입 페이지에서는 우편번호와 주소를 입력하기 위해 카카오에서 제공하는 우편번호 서비스를 사용한다.

HTML에서 다음 스크립트를 불러온다.

```html
<script src="//t1.kakaocdn.net/mapjsapi/bundle/postcode/prod/postcode.v2.js"></script>
```

주소 검색 버튼을 누르면 다음 함수가 실행된다.

```html
<button type="button" onclick="sample6_execDaumPostcode()">검색</button>
```

---

## 15. 주소 검색 코드 흐름

```javascript
function sample6_execDaumPostcode() {
    new kakao.Postcode({
        oncomplete: function (data) {
            let addr = ""
            let extraAddr = ""

            if (data.userSelectedType === "R") {
                addr = data.roadAddress
            } else {
                addr = data.jibunAddress
            }

            if (data.userSelectedType === "R") {
                if (data.bname !== "" && /[동로가]$/.test(data.bname)) {
                    extraAddr += data.bname
                }

                if (data.buildingName !== "" && data.apartment === "Y") {
                    extraAddr += extraAddr !== "" ? ", " + data.buildingName : data.buildingName
                }

                if (extraAddr !== "") {
                    extraAddr = " (" + extraAddr + ")"
                }

                document.getElementById("sample6_extraAddress").value = extraAddr
            } else {
                document.getElementById("sample6_extraAddress").value = ""
            }

            document.getElementById("sample6_postcode").value = data.zonecode
            document.getElementById("sample6_address").value = addr
            document.getElementById("sample6_detailAddress").focus()
        }
    }).open()
}
```

### 동작 흐름

```text
주소 검색 버튼 클릭
        ↓
카카오 우편번호 검색 팝업 열림
        ↓
사용자가 주소 선택
        ↓
oncomplete 콜백 실행
        ↓
우편번호, 주소, 참고 항목 입력
        ↓
상세 주소 입력칸으로 포커스 이동
```

### 도로명 주소와 지번 주소

```javascript
if (data.userSelectedType === "R") {
    addr = data.roadAddress
} else {
    addr = data.jibunAddress
}
```

`R`은 도로명 주소를 의미하고, `J`는 지번 주소를 의미한다.

### 참고 항목 만들기

```javascript
if (data.bname !== "" && /[동로가]$/.test(data.bname)) {
    extraAddr += data.bname
}
```

`/[동로가]$/`는 문자열이 `동`, `로`, `가` 중 하나로 끝나는지 검사한다.

---

## 16. 전체 검증 흐름 정리

회원가입 페이지의 전체 흐름은 다음과 같다.

```text
사용자 입력
    ↓
주민등록번호 앞자리 6자리 입력 시 뒷자리 칸으로 이동
    ↓
주민등록번호 인증 버튼 클릭
    ↓
검증 성공 시 ssncheck = "y"
    ↓
가입완료 버튼 클릭
    ↓
sendit() 실행
    ↓
아이디, 비밀번호, 이름, 휴대폰, 이메일 검사
    ↓
ssncheck 값 확인
    ↓
모든 조건 통과 시 폼 제출
```

---

## 17. 핵심 코드 연결

아래 코드는 회원가입 검증에 필요한 핵심만 줄인 예제다.

```html
<form action="/regist" method="post" onsubmit="return sendit()">
    <input type="hidden" id="ssncheck" value="n">

    <input type="text" id="userid" placeholder="아이디">
    <input type="password" id="userpw" placeholder="비밀번호">
    <input type="password" id="userpw_re" placeholder="비밀번호 확인">
    <input type="text" id="name" placeholder="이름">
    <input type="text" id="hp" placeholder="010-1234-5678">
    <input type="email" id="email" placeholder="apple@apple.com">

    <button type="submit">가입완료</button>
</form>
```

```javascript
function sendit() {
    const userid = document.getElementById("userid")
    const userpw = document.getElementById("userpw")
    const userpw_re = document.getElementById("userpw_re")
    const name = document.getElementById("name")
    const hp = document.getElementById("hp")
    const email = document.getElementById("email")

    const expIdText = /^[A-Za-z0-9]{4,20}$/
    const expPwText = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$/
    const expNameText = /^[가-힣]+$/
    const expHpText = /^\d{3}-\d{3,4}-\d{4}$/
    const expEmailText = /^[A-Za-z0-9\-.]+@[A-Za-z0-9-]+\.[A-Za-z]+$/

    if (!expIdText.test(userid.value)) {
        alert("아이디는 4자 이상 20자 이하의 영문자 또는 숫자로 입력하세요.")
        userid.focus()
        return false
    }

    if (!expPwText.test(userpw.value)) {
        alert("비밀번호는 영문자, 숫자, 특수문자를 포함해 8자 이상 입력하세요.")
        userpw.focus()
        return false
    }

    if (userpw.value !== userpw_re.value) {
        alert("비밀번호가 일치하지 않습니다.")
        userpw_re.focus()
        return false
    }

    if (!expNameText.test(name.value)) {
        alert("이름은 한글로 입력하세요.")
        name.focus()
        return false
    }

    if (!expHpText.test(hp.value)) {
        alert("휴대폰 번호 형식이 올바르지 않습니다.")
        hp.focus()
        return false
    }

    if (!expEmailText.test(email.value)) {
        alert("이메일 형식이 올바르지 않습니다.")
        email.focus()
        return false
    }

    return true
}
```

---

## 18. 핵심 정리

### 정규식

- 정규식은 문자열 패턴을 검사, 검색, 치환할 때 사용한다.
- `/패턴/옵션` 형태로 작성한다.
- `test()`는 패턴 일치 여부를 `true` 또는 `false`로 반환한다.
- `match()`는 일치 결과를 반환한다.
- `replace()`는 일치하는 문자열을 치환한다.
- `search()`는 일치하는 위치를 반환한다.

### 회원가입 검증

- `onsubmit="return sendit()"`으로 폼 제출 전 검증할 수 있다.
- 검증에 실패하면 `return false`로 제출을 막는다.
- `focus()`를 사용하면 문제가 있는 입력칸으로 커서를 이동할 수 있다.
- hidden input을 사용해 주민등록번호 인증 여부를 저장할 수 있다.
- 입력값이 변경되면 인증 상태를 다시 초기화해야 한다.

### 주의할 점

- 클라이언트 검증은 사용자의 편의를 위한 1차 검증이다.
- 실제 보안 검증은 반드시 서버에서 다시 해야 한다.
- 주민등록번호 같은 민감 정보는 실제 서비스에서 수집과 저장에 매우 주의해야 한다.
- 이메일, 비밀번호 정규식은 서비스 정책에 따라 달라질 수 있다.
