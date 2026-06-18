# JavaScript 객체, 클래스, 프로토타입 정리

JavaScript에서 객체는 여러 데이터를 하나로 묶고, 관련된 동작까지 함께 표현할 수 있는 핵심 자료형이다.

객체를 이해하면 클래스, 상속, 프로토타입, 스프레드 문법, 구조 분해 할당까지 자연스럽게 연결해서 이해할 수 있다.

이번 글에서는 다음 흐름으로 정리한다.

```text
객체 기초
  ↓
객체 생성 방식
  ↓
객체 복사와 스프레드 문법
  ↓
클래스와 상속
  ↓
private 필드, getter, setter
  ↓
프로토타입
```

---

## 1. 프로그래밍 방식 비교

같은 문제를 해결하더라도 코드를 구성하는 방식은 여러 가지가 있다.

### 1.1 절차 지향 프로그래밍

절차 지향 프로그래밍은 코드를 위에서 아래로 실행되는 순서 중심으로 구성하는 방식이다.

```javascript
const names = ["김사과", "반하나", "오렌지", "이메론"]

for (let i = 0; i < names.length; i++) {
    if (names[i].startsWith("김")) {
        console.log("안녕하세요, " + names[i] + "님!")
    }
}
```

### 출력 결과

```text
안녕하세요, 김사과님!
```

간단한 코드는 이해하기 쉽지만, 기능이 많아질수록 데이터와 동작이 흩어질 수 있다.

### 1.2 객체 지향 프로그래밍

객체 지향 프로그래밍은 데이터와 동작을 객체라는 단위로 묶어서 문제를 해결하는 방식이다.

```javascript
const greeter = {
    names: ["김사과", "반하나", "오렌지", "이메론"],

    greetKim: function () {
        for (let i = 0; i < this.names.length; i++) {
            if (this.names[i].startsWith("김")) {
                console.log("안녕하세요, " + this.names[i] + "님!")
            }
        }
    }
}

greeter.greetKim()
```

### 출력 결과

```text
안녕하세요, 김사과님!
```

`names`라는 데이터와 `greetKim()`이라는 동작이 `greeter` 객체 안에 함께 들어 있다.

### 1.3 함수형 프로그래밍

함수형 프로그래밍은 데이터를 직접 변경하기보다 함수를 조합해 결과를 만드는 방식이다.

```javascript
const names = ["김사과", "반하나", "오렌지", "이메론"]

names
    .filter(name => name.startsWith("김"))
    .forEach(name => console.log("안녕하세요, " + name + "님!"))
```

### 출력 결과

```text
안녕하세요, 김사과님!
```

`filter()`로 조건에 맞는 값만 고르고, `forEach()`로 각 값을 처리한다.

---

## 2. 객체란?

객체(Object)는 여러 값을 하나의 단위로 묶어 저장하는 자료형이다.

객체는 **키와 값의 쌍**으로 데이터를 저장한다.

```javascript
const person = {
    name: "김사과",
    age: 20
}
```

객체 안에 저장된 값을 **프로퍼티(Property)**라고 한다.

객체 안에 저장된 함수를 **메서드(Method)**라고 한다.

```javascript
const person = {
    name: "김사과",
    age: 20,
    greet: function () {
        console.log("안녕하세요, 저는 " + this.name + "입니다.")
    }
}
```

---

## 3. 객체를 만드는 방법

JavaScript에서는 객체를 여러 방식으로 만들 수 있다.

| 방식 | 특징 |
| --- | --- |
| 객체 리터럴 | `{}` 안에 직접 속성과 메서드를 작성한다 |
| `new Object()` | 빈 객체를 만든 뒤 속성을 추가한다 |
| 생성자 함수 | 같은 구조의 객체를 여러 개 만들 수 있다 |
| 클래스 | ES6 이후 사용하는 명확한 객체 생성 문법이다 |

---

## 4. 객체 리터럴

객체 리터럴은 가장 간단한 객체 생성 방식이다.

```javascript
const person1 = {
    name: "김사과",
    age: 20,
    greet: function () {
        console.log("안녕하세요, 저는 " + this.name + "입니다.")
    }
}

person1.greet()
```

### 출력 결과

```text
안녕하세요, 저는 김사과입니다.
```

`this.name`은 현재 객체인 `person1`의 `name` 값을 의미한다.

---

## 5. `new Object()`

`new Object()`를 사용하면 빈 객체를 먼저 만든 뒤 속성과 메서드를 추가할 수 있다.

```javascript
const person2 = new Object()

person2.name = "김사과"
person2.age = 20
person2.greet = function () {
    console.log("안녕하세요, 저는 " + this.name + "입니다.")
}

person2.greet()
```

### 출력 결과

```text
안녕하세요, 저는 김사과입니다.
```

객체 리터럴보다 코드가 길어지므로 일반적으로는 객체 리터럴을 더 자주 사용한다.

---

## 6. 생성자 함수

생성자 함수는 비슷한 구조의 객체를 여러 개 만들 때 사용한다.

생성자 함수 이름은 관례적으로 대문자로 시작한다.

```javascript
function Person(name, age) {
    this.name = name
    this.age = age
    this.greet = function () {
        console.log("안녕하세요, 저는 " + this.name + "입니다.")
    }
}

const person3 = new Person("김사과", 20)
person3.greet()
```

### 출력 결과

```text
안녕하세요, 저는 김사과입니다.
```

`new`를 사용하면 새로운 객체가 만들어지고, 생성자 함수 내부의 `this`는 새로 만들어진 객체를 가리킨다.

---

## 7. 클래스

클래스는 객체를 만들기 위한 설계도 역할을 한다.

```javascript
class Person {
    constructor(name, age) {
        this.name = name
        this.age = age
    }

    greet() {
        console.log("안녕하세요, 저는 " + this.name + "입니다.")
    }
}

const person4 = new Person("김사과", 20)
person4.greet()
```

### 출력 결과

```text
안녕하세요, 저는 김사과입니다.
```

`constructor()`는 객체가 생성될 때 자동으로 호출되는 메서드다.

---

## 8. 객체는 참조값이다

객체를 변수에 저장하면 객체 자체가 복사되는 것이 아니라 객체를 가리키는 참조가 저장된다.

```javascript
const obj1 = { name: "김사과" }
const obj2 = obj1

obj2.name = "반하나"

console.log(obj1.name)
console.log(obj2.name)
```

### 출력 결과

```text
반하나
반하나
```

`obj1`과 `obj2`는 같은 객체를 가리킨다. 따라서 `obj2.name`을 바꾸면 `obj1.name`도 바뀐 것처럼 보인다.

```text
obj1 ──┐
       ├──> { name: "반하나" }
obj2 ──┘
```

---

## 9. 얕은 복사

얕은 복사는 객체의 1단계 속성만 새 객체로 복사한다.

### 9.1 `Object.assign()`

```javascript
const obj1 = { name: "김사과", age: 20 }
const obj2 = Object.assign({}, obj1)

console.log(obj2)

obj2.name = "오렌지"

console.log(obj1)
console.log(obj2)
```

### 출력 결과

```text
{ name: "김사과", age: 20 }
{ name: "김사과", age: 20 }
{ name: "오렌지", age: 20 }
```

`obj2`는 새 객체이므로 `obj2.name`을 바꿔도 `obj1.name`은 바뀌지 않는다.

### 9.2 스프레드 문법

```javascript
const obj1 = { name: "김사과", age: 20 }
const obj3 = { ...obj1 }

obj3.age = 30

console.log(obj3)
console.log(obj1)
```

### 출력 결과

```text
{ name: "김사과", age: 30 }
{ name: "김사과", age: 20 }
```

---

## 10. 얕은 복사의 한계

객체 안에 또 다른 객체가 있으면 내부 객체는 참조만 복사된다.

```javascript
const obj4 = {
    name: "김사과",
    age: 20,
    address: {
        city: "서울"
    }
}

const obj5 = { ...obj4 }

obj5.address.city = "부산"

console.log(obj5)
console.log(obj4)
```

### 출력 결과

```text
{ name: "김사과", age: 20, address: { city: "부산" } }
{ name: "김사과", age: 20, address: { city: "부산" } }
```

`obj4`와 `obj5`는 서로 다른 객체지만, `address`는 같은 객체를 공유한다.

```text
obj4.address ──┐
               ├──> { city: "부산" }
obj5.address ──┘
```

객체 내부의 중첩 객체까지 모두 새로 복사하는 것을 깊은 복사라고 한다.

---

## 11. 스프레드 문법

스프레드 문법은 `...`을 사용해 배열이나 객체의 값을 펼치는 문법이다.

### 11.1 배열 펼치기

```javascript
function add(x, y, z) {
    return x + y + z
}

const nums = [1, 2, 3]

console.log(add(...nums))
```

### 출력 결과

```text
6
```

`add(...nums)`는 `add(1, 2, 3)`과 같은 의미다.

### 11.2 객체 병합

```javascript
const a = { name: "김사과" }
const b = { age: 20 }

const merged = { ...a, ...b }

console.log(merged)
```

### 출력 결과

```text
{ name: "김사과", age: 20 }
```

### 11.3 배열 구조 분해와 나머지 문법

```javascript
const numbers = [1, 2, 3, 4, 5]
const [first, second, ...rest] = numbers

console.log(first)
console.log(second)
console.log(rest)
```

### 출력 결과

```text
1
2
[3, 4, 5]
```

### 11.4 객체 구조 분해와 나머지 문법

```javascript
const user = {
    name: "김사과",
    age: 20,
    city: "서울"
}

const { name, ...rest2 } = user

console.log(name)
console.log(rest2)
```

### 출력 결과

```text
김사과
{ age: 20, city: "서울" }
```

---

## 12. 구조 분해 할당 활용

객체를 함수의 매개변수로 받을 때 구조 분해 할당을 사용할 수 있다.

```javascript
function display({ name, age, address, job }) {
    console.log(name, age, address, job)
}

const apple = {
    name: "김사과",
    age: 20,
    address: {
        si: "서울시",
        gu: "서초구",
        dong: "양재동"
    }
}

const newApple = { ...apple, job: "프로그래머" }

display(newApple)
```

### 출력 결과

```text
김사과 20 { si: "서울시", gu: "서초구", dong: "양재동" } 프로그래머
```

### 기본값 설정

```javascript
const { pet = "루시" } = newApple

console.log(pet)
```

### 출력 결과

```text
루시
```

`newApple`에 `pet` 속성이 없으므로 기본값 `"루시"`가 사용된다.

### 속성 이름 바꾸기

```javascript
const { job: hobby } = newApple

console.log(hobby)
```

### 출력 결과

```text
프로그래머
```

`job`이라는 속성 값을 `hobby`라는 변수명으로 꺼낸다.

### 중첩 객체 구조 분해

```javascript
const component = {
    name: "Button",
    styles: {
        size: 20,
        color: "black"
    }
}

function changeColor({ styles: { color } }) {
    console.log(color)
}

changeColor(component)
```

### 출력 결과

```text
black
```

---

## 13. 클래스 기본 문법

클래스는 객체를 생성하기 위한 구조를 정의한다.

```javascript
class 클래스명 {
    constructor(매개변수1, 매개변수2) {
        속성 정의
    }

    메서드명() {
        객체가 할 수 있는 동작 정의
    }
}
```

### 예제

```javascript
class Animal {
    constructor(type) {
        this.type = type
    }

    bark() {
        console.log(`${this.type} 멍멍!`)
    }

    speak() {
        console.log("동물이 소리를 냅니다.")
    }
}

const dog = new Animal("강아지")

console.log(dog.type)
dog.bark()
```

### 출력 결과

```text
강아지
강아지 멍멍!
```

---

## 14. 클래스 상속

상속은 다른 클래스의 속성과 메서드를 물려받아 사용하는 기능이다.

JavaScript에서는 `extends`를 사용한다.

```javascript
class Dog extends Animal {
    constructor(type, color) {
        super(type)
        this.color = color
    }

    showInfo() {
        console.log(`${this.type}는 ${this.color}입니다.`)
    }
}

const rucy = new Dog("강아지", "흰색")

rucy.speak()
rucy.bark()
rucy.showInfo()
```

### 출력 결과

```text
동물이 소리를 냅니다.
강아지 멍멍!
강아지는 흰색입니다.
```

`super(type)`은 부모 클래스인 `Animal`의 `constructor`를 호출한다.

자식 클래스에서 `constructor`를 직접 정의한다면 `this`를 사용하기 전에 반드시 `super()`를 먼저 호출해야 한다.

---

## 15. 정적 메서드

정적 메서드는 객체를 만들지 않고 클래스 이름으로 직접 호출하는 메서드다.

```javascript
class MathTool {
    static add(a, b) {
        return a + b
    }
}

console.log(MathTool.add(3, 4))
```

### 출력 결과

```text
7
```

정적 메서드는 인스턴스의 개별 상태보다 클래스 차원의 기능을 제공할 때 사용한다.

```javascript
const tool = new MathTool()

// tool.add(3, 4)  // TypeError
```

---

## 16. 클래스 필드

클래스 필드는 `constructor` 밖에서 속성을 바로 정의하는 문법이다.

```javascript
class Product {
    name = "상품명 없음"
    price = 0

    showInfo() {
        console.log(`${this.name}의 가격은 ${this.price}원입니다.`)
    }
}

const product = new Product()
product.showInfo()
```

### 출력 결과

```text
상품명 없음의 가격은 0원입니다.
```

클래스 필드는 기본값을 설정하거나 private 필드를 선언할 때 유용하다.

---

## 17. getter와 setter

`get`과 `set`은 객체의 속성처럼 값을 읽고 쓰면서 내부 로직을 실행하게 해준다.

```javascript
class User {
    #password = ""

    constructor(name, password) {
        this._name = name
        this.#password = password
    }

    get name() {
        return this._name
    }

    set name(newName) {
        if (newName.length < 2) {
            console.log("이름은 두 글자 이상이어야 합니다.")
        } else {
            this._name = newName
        }
    }

    checkPassword(input) {
        return this.#password === input
    }
}

const user = new User("김사과", "1111")

user.name = "반"
user.name = "반하나"

console.log(user.name)
console.log(user.checkPassword("1111"))
console.log(user.checkPassword("2222"))
```

### 출력 결과

```text
이름은 두 글자 이상이어야 합니다.
반하나
true
false
```

`get name()`은 `user.name`으로 값을 읽을 때 실행된다.

`set name()`은 `user.name = "반하나"`처럼 값을 할당할 때 실행된다.

---

## 18. private 필드

private 필드는 클래스 내부에서만 접근할 수 있는 비공개 속성이다.

JavaScript에서는 필드 이름 앞에 `#`을 붙인다.

```javascript
class User {
    #password = ""

    constructor(password) {
        this.#password = password
    }

    checkPassword(input) {
        return this.#password === input
    }
}

const user = new User("1111")

console.log(user.checkPassword("1111"))
// console.log(user.#password)  // SyntaxError
```

### 출력 결과

```text
true
```

`#password`는 클래스 외부에서 직접 접근할 수 없다.

---

## 19. Account 클래스 예제

계좌 클래스를 통해 클래스 필드, private 필드, getter, setter, 정적 필드를 함께 사용해본다.

```javascript
class Account {
    static accountCount = 0

    #balance = 0

    constructor(owner) {
        this.owner = owner
        Account.accountCount++
    }

    get balance() {
        return this.#balance
    }

    set balance(value) {
        console.log("직접 잔액을 설정할 수 없습니다.")
    }

    deposit(amount) {
        if (amount > 0) {
            this.#balance += amount
            console.log(`${this.owner}님, ${amount}원 입금되었습니다.`)
        }
    }

    withdraw(amount) {
        if (amount <= this.#balance) {
            this.#balance -= amount
            console.log(`${this.owner}님, ${amount}원 출금되었습니다.`)
        } else {
            console.log("잔액이 부족합니다.")
        }
    }

    static getAccountCount() {
        return `총 계좌 수: ${Account.accountCount}`
    }
}

const user1 = new Account("김사과")
user1.deposit(1000)
console.log(user1.balance)

user1.withdraw(300)
console.log(user1.balance)

const user2 = new Account("반하나")
user2.deposit(6000)

console.log(Account.getAccountCount())
```

### 출력 결과

```text
김사과님, 1000원 입금되었습니다.
1000
김사과님, 300원 출금되었습니다.
700
반하나님, 6000원 입금되었습니다.
총 계좌 수: 2
```

`#balance`는 외부에서 직접 수정할 수 없다. 대신 `deposit()`과 `withdraw()` 메서드를 통해서만 변경한다.

이렇게 하면 객체의 상태를 안전하게 관리할 수 있다.

---

## 20. 프로토타입

프로토타입(Prototype)은 JavaScript 객체가 공통 속성과 메서드를 공유하도록 해주는 메커니즘이다.

JavaScript의 객체는 자신에게 없는 속성이나 메서드를 요청받으면 연결된 프로토타입 객체를 따라 올라가며 찾는다.

```text
객체 → 생성자.prototype → Object.prototype → null
```

이 연결 구조를 **프로토타입 체인**이라고 한다.

---

## 21. 프로토타입 예제

```javascript
function Person(name) {
    this.name = name
}

Person.prototype.study = function () {
    console.log(`${this.name}이 열심히 공부합니다.`)
}

const p1 = new Person("김사과")
const p2 = new Person("반하나")

p1.sayHello = function () {
    console.log(`안녕하세요. 저는 ${this.name}입니다.`)
}

p1.sayHello()
p1.study()
p2.study()
// p2.sayHello()
```

### 출력 결과

```text
안녕하세요. 저는 김사과입니다.
김사과이 열심히 공부합니다.
반하나이 열심히 공부합니다.
```

`study()`는 `p1`과 `p2`가 직접 가지고 있는 메서드가 아니다. `Person.prototype`에 저장된 공통 메서드다.

반면 `sayHello()`는 `p1`에만 직접 추가한 메서드다. 따라서 `p2.sayHello()`를 호출하면 오류가 발생한다.

```text
p1 ──┐
     ├──> Person.prototype ──> Object.prototype ──> null
p2 ──┘        └── study()
```

---

## 22. Object 객체

`Object`는 JavaScript의 기본 객체 생성자다.

대부분의 일반 객체는 최종적으로 `Object.prototype`을 프로토타입 체인의 끝부분에 가진다.

객체를 다루기 위한 여러 정적 메서드도 제공한다.

### 22.1 `Object.keys()`

객체의 키를 배열로 반환한다.

```javascript
const user = { name: "김사과", age: 20 }

console.log(Object.keys(user))
```

```text
["name", "age"]
```

### 22.2 `Object.values()`

객체의 값을 배열로 반환한다.

```javascript
console.log(Object.values(user))
```

```text
["김사과", 20]
```

### 22.3 `Object.entries()`

객체의 키와 값을 `[key, value]` 형태의 배열로 반환한다.

```javascript
console.log(Object.entries(user))
```

```text
[["name", "김사과"], ["age", 20]]
```

### 22.4 `Object.assign()`

객체를 복사하거나 병합할 때 사용한다.

```javascript
const user = { name: "김사과" }
const profile = { age: 20 }

const result = Object.assign({}, user, profile)

console.log(result)
```

```text
{ name: "김사과", age: 20 }
```

### 22.5 `Object.hasOwn()`

객체가 특정 속성을 직접 가지고 있는지 확인한다.

```javascript
const user = { name: "김사과", age: 20 }

console.log(Object.hasOwn(user, "name"))
console.log(Object.hasOwn(user, "job"))
```

```text
true
false
```

### 22.6 `Object.freeze()`

객체를 동결해 속성을 추가, 삭제, 수정할 수 없게 만든다.

```javascript
const config = { debug: true }

Object.freeze(config)
config.debug = false

console.log(config.debug)
```

```text
true
```

`Object.freeze()`는 객체의 1단계 속성을 동결한다. 중첩 객체까지 모두 동결하려면 별도의 처리가 필요하다.

---

## 23. 클래스와 프로토타입의 관계

JavaScript의 `class`는 완전히 새로운 객체 시스템이 아니라 기존 프로토타입 기반 문법을 더 읽기 좋게 만든 문법이다.

다음 클래스 메서드는 내부적으로 `Animal.prototype`에 저장된다.

```javascript
class Animal {
    speak() {
        console.log("동물이 소리를 냅니다.")
    }
}
```

대략 다음 구조와 비슷하게 이해할 수 있다.

```javascript
function Animal() {}

Animal.prototype.speak = function () {
    console.log("동물이 소리를 냅니다.")
}
```

즉, 클래스 문법을 사용해도 JavaScript 객체는 여전히 프로토타입 체인을 기반으로 동작한다.

---

## 24. 핵심 정리

### 객체

- 객체는 키와 값의 쌍으로 데이터를 저장한다.
- 객체 안의 값은 프로퍼티라고 한다.
- 객체 안의 함수는 메서드라고 한다.
- 객체는 참조값이므로 변수에 대입하면 같은 객체를 가리킬 수 있다.

### 복사와 스프레드 문법

- `Object.assign()`과 `{ ...obj }`는 얕은 복사를 수행한다.
- 중첩 객체는 얕은 복사 시 참조를 공유한다.
- 스프레드 문법은 배열이나 객체의 값을 펼칠 때 사용한다.
- 구조 분해 할당은 객체와 배열에서 필요한 값만 꺼낼 때 유용하다.

### 클래스

- `constructor()`는 객체 생성 시 자동으로 호출된다.
- `extends`로 상속을 구현한다.
- `super()`로 부모 클래스의 생성자를 호출한다.
- `static` 메서드는 클래스 이름으로 직접 호출한다.
- `get`과 `set`으로 속성 접근을 제어할 수 있다.
- `#`을 붙인 필드는 클래스 외부에서 접근할 수 없다.

### 프로토타입

- 프로토타입은 객체들이 공통 메서드를 공유하기 위한 구조다.
- 객체에 없는 속성이나 메서드는 프로토타입 체인을 따라 검색한다.
- `Person.prototype.study`처럼 공통 메서드를 정의하면 여러 객체가 같은 메서드를 공유한다.
- JavaScript의 클래스도 내부적으로 프로토타입 기반으로 동작한다.
