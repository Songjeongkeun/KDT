# [6일차] Python

프로그램을 작성하다 보면 같은 작업을 여러 번 수행해야 하는 순간이 많다. 파이썬은 반복 작업을 처리하기 위해 `while` 문과 `for` 문을 제공한다. 여기에 `range()`, `enumerate()`, `zip()`과 같은 도구를 함께 사용하면 반복 코드를 간결하고 읽기 쉽게 작성할 수 있다.

이번 글에서는 파이썬 반복문의 기본 사용법부터 흐름 제어, 중첩 반복문, 컴프리헨션까지 정리한다.

## 1. `while` 문

`while` 문은 조건식이 `True`인 동안 코드 블록을 반복해서 실행한다. 반복 횟수가 정해져 있지 않고, 특정 조건이 만족될 때까지 작업해야 할 때 유용하다.

```python
while 조건식:
    실행할 코드
```

`while` 문을 사용할 때는 언젠가 조건식이 `False`가 되도록 상태를 변경해야 한다. 그렇지 않으면 반복이 끝나지 않는 무한 루프가 발생한다.

### 1.1 기본 반복

```python
i = 1

while i <= 5:
    print("Hello Python")
    i += 1
```

위 코드는 `i`가 1부터 5까지 증가하는 동안 문자열을 다섯 번 출력한다. `i += 1`이 없다면 `i <= 5`가 계속 참이므로 반복이 종료되지 않는다.

### 1.2 1부터 10까지의 합 구하기

```python
i = 1
total = 0

while i <= 10:
    total += i
    i += 1

print(f"1부터 10까지의 합: {total}")
```

반복문 안에서 현재 숫자를 `total`에 누적하고, 다음 숫자를 처리하기 위해 `i`를 1씩 증가시킨다.

### 1.3 1부터 100까지 짝수의 합 구하기

```python
i = 1
total = 0

while i <= 100:
    if i % 2 == 0:
        total += i
    i += 1

print(f"1부터 100까지 짝수의 합: {total}")
```

`i % 2 == 0`은 `i`를 2로 나눈 나머지가 0인지 검사한다. 따라서 짝수만 합계에 포함된다.

### 1.4 입력받은 구구단 출력하기

```python
dan = int(input("원하는 단을 입력하세요: "))
print(f"{dan}단")

i = 1

while i <= 9:
    print(f"{dan} * {i} = {dan * i}")
    i += 1
```

사용자로부터 입력을 받거나 어떤 이벤트가 발생할 때까지 기다리는 로직에서는 `while` 문이 자연스럽게 사용된다.

## 2. `for` 문

`for` 문은 반복 가능한 객체(iterable)의 요소를 하나씩 꺼내 처리한다. 리스트, 튜플, 문자열, 딕셔너리, `range` 객체 등이 반복 가능한 객체에 해당한다.

```python
for 변수 in 반복_가능한_객체:
    실행할 코드
```

`while` 문이 조건 중심의 반복이라면, `for` 문은 데이터의 요소를 순회하는 데 적합하다.

### 2.1 문자열 순회하기

```python
for char in "Hello":
    print(char)
    
# 실행 결과
# H
# e
# l
# l
# o
```

문자열도 반복 가능한 객체이므로 문자 하나씩 꺼내 처리할 수 있다.

### 2.2 리스트 순회하기

```python
numbers = [10, 20, 30, 40]

for number in numbers:
    print(number)
    
# 실행 결과
# 10
# 20
# 30
# 40
```

`number`에는 반복할 때마다 리스트의 요소가 차례로 저장된다.

### 2.3 조건에 맞는 데이터 세기

```python
scores = [90, 30, 50, 60, 80, 70, 100, 40, 20, 10]
count = 0

for score in scores:
    if score >= 60:
        count += 1

print(f"60점 이상인 학생의 수는 {count}명이다.") # 60점 이상인 학생의 수는 6명이다.
```

반복문과 조건문을 함께 사용하면 원하는 조건에 맞는 데이터만 계산할 수 있다.

### 2.4 딕셔너리 순회하기

딕셔너리는 `key: value` 쌍으로 데이터를 관리한다. 딕셔너리를 그대로 반복하면 기본적으로 키가 나온다.

```python
user = {
    "no": 1,
    "userid": "apple",
    "name": "김사과",
    "phone": "010-1234-5678"
}

for key in user:
    print(key)
    
# 실행 결과
# no
# userid
# name
# phone

# 같은 의미의 코드
for key in user.key():
  print(key)
```

값만 필요하면 `values()`를 사용한다.

```python
for value in user.values():
    print(value)
    
# 실행 결과
# 1
# apple
# 김사과
# 010-1234-5678

# 같은 의미의 코드
for value in user():
  print(user[value])

for value in user():
  print(user.get(value))
```

키와 값을 함께 사용하려면 `items()`를 사용한다.

```python
for i in user.items():
  print(i)
 
# 실행 결과
# ('no', 1)
# ('userid', 'apple')
# ('name', '김사과')
# ('hp', '010-1234-5678')

for key, value in user.items():
	print(f"{key}: {value}")
 
# 실행 결과
# no: 1
# userid: apple
# name: 김사과
# phone: 010-1234-5678
```

## 3. `range()` 함수

`range()`는 일정한 규칙을 가진 정수 범위를 표현하는 객체를 반환한다. 실제 숫자 목록을 한꺼번에 저장하지 않고 필요한 시점에 값을 제공하므로, 반복문에서 효율적으로 사용할 수 있다.

```python
range(stop)
range(start, stop)
range(start, stop, step)
```

| 인자 | 설명 |
| --- | --- |
| `start` | 시작값이며, 생략하면 `0`이다. |
| `stop` | 종료 기준값이며, 이 값은 포함되지 않는다. |
| `step` | 증가 또는 감소 간격이며, 생략하면 `1`이다. |

### 3.1 기본 사용법

```python
for i in range(10):
    print(i, end=" ")
```

출력 결과는 다음과 같다.

```text
0 1 2 3 4 5 6 7 8 9
```

`range(10)`은 `0`부터 `9`까지의 값을 제공한다. 마지막 값인 `10`은 포함하지 않는다는 점이 중요하다.

### 3.2 시작값과 간격 지정하기

```python
for i in range(1, 10, 2):
    print(i, end=" ")
```

출력 결과는 다음과 같다.

```text
1 3 5 7 9
```

### 3.3 짝수 합 구하기

```python
total = 0

for number in range(0, 101, 2):
    total += number

print(f"1부터 100까지 짝수의 합: {total}")
```

짝수만 생성하도록 간격을 `2`로 설정하면 반복문 안에서 별도의 조건 검사를 하지 않아도 된다.

## 4. `enumerate()` 함수

반복문에서 데이터의 값뿐 아니라 인덱스도 필요할 때 `enumerate()`를 사용한다. `enumerate()`는 반복 가능한 객체의 각 요소를 `(인덱스, 값)` 형태로 제공한다.

```python
enumerate(iterable, start=0)
```

### 4.1 인덱스와 값 함께 출력하기

```python
fruits = ["apple", "banana", "orange"]

for index, fruit in enumerate(fruits):
    print(f"인덱스: {index}, 값: {fruit}")
```

출력 결과는 다음과 같다.

```text
인덱스: 0, 값: apple
인덱스: 1, 값: banana
인덱스: 2, 값: orange
```

### 4.2 시작 번호 변경하기

목록 번호처럼 1부터 출력하고 싶다면 `start=1`을 지정한다.

```python
fruits = ["apple", "banana", "orange"]

for number, fruit in enumerate(fruits, start=1):
    print(f"{number}. {fruit}")
```

출력 결과는 다음과 같다.

```text
1. apple
2. banana
3. orange
```

인덱스를 직접 관리하는 변수보다 `enumerate()`를 사용하면 코드의 목적이 더 분명해진다.

## 5. 이터러블과 이터레이터

반복문을 이해하려면 이터러블(iterable)과 이터레이터(iterator)의 차이를 알아두는 것이 좋다.

### 5.1 이터러블

이터러블은 요소를 하나씩 반복해서 꺼낼 수 있는 객체다. 리스트, 문자열, 튜플, 집합, 딕셔너리 등이 여기에 해당한다.

```python
numbers = [10, 20, 30]

for number in numbers:
    print(number)
```

### 5.2 이터레이터

이터레이터는 값을 하나씩 꺼낼 수 있는 상태를 가진 객체다. `iter()` 함수로 이터러블에서 이터레이터를 만들고, `next()` 함수로 다음 값을 가져올 수 있다.

```python
numbers = [10, 20, 30]
iterator = iter(numbers)

print(next(iterator))  # 10
print(next(iterator))  # 20
print(next(iterator))  # 30
```

더 이상 꺼낼 값이 없는데 `next()`를 호출하면 `StopIteration` 예외가 발생한다.

```python
# print(next(iterator))  # StopIteration 예외가 발생한다.
```

`for` 문은 내부적으로 이터레이터에서 값을 하나씩 꺼내고, 값이 모두 소진되면 반복을 종료하는 동작을 수행한다.

## 6. `zip()` 함수

`zip()`은 여러 반복 가능한 객체에서 같은 위치의 값을 하나씩 꺼내 튜플로 묶는다. 서로 관련된 두 개 이상의 데이터를 함께 순회할 때 유용하다.

```python
names = ["김사과", "반하나", "오렌지"]
scores = [95, 87, 100]

for name, score in zip(names, scores):
    print(f"{name}: {score}점")
```

출력 결과는 다음과 같다.

```text
김사과: 95점
반하나: 87점
오렌지: 100점
```

길이가 다른 반복 가능한 객체를 `zip()`에 전달하면 가장 짧은 객체의 길이에 맞춰 반복이 종료된다.

```python
names = ["김사과", "반하나", "오렌지"]
scores = [95, 87]

print(list(zip(names, scores)))
# [('김사과', 95), ('반하나', 87)]
```

## 7. `continue`와 `break`

반복문은 전체 요소를 끝까지 처리하는 경우가 많지만, 특정 상황에서는 현재 반복을 건너뛰거나 반복 자체를 끝내야 한다.

### `continue`: 현재 반복 건너뛰기

`continue`가 실행되면 그 아래의 코드는 수행하지 않고 다음 반복으로 이동한다.

```python
logs = [
    "INFO: 사용자 로그인 성공",
    "DEBUG: 세션 생성 중",
    "ERROR: 데이터베이스 연결 실패",
    "INFO: 요청 처리 완료",
    "ERROR: 파일 저장 실패"
]

error_logs = []

for log in logs:
    if not log.startswith("ERROR"):
        continue
    error_logs.append(log)

for error in error_logs:
    print(error)
```

이 코드는 `ERROR`로 시작하는 로그만 수집해 출력한다.

### `break`: 반복 종료하기

`break`가 실행되면 현재 반복문을 즉시 빠져나간다.

```python
orders = ["마우스", "키보드", "모니터", "그래픽카드", "프린터"]
stock = {
    "마우스": 10,
    "키보드": 5,
    "모니터": 0,
    "그래픽카드": 2,
    "프린터": 3
}

for item in orders:
    if stock[item] == 0:
        print(f"{item} 재고가 없어 주문 처리를 중단한다.")
        break
    print(f"{item} 주문을 완료한다.")
```

재고가 없는 상품을 발견한 뒤에는 뒤의 주문을 확인하지 않고 반복을 종료한다.

## 8. 중첩 반복문

중첩 반복문은 반복문 안에 또 다른 반복문을 작성한 구조다. 바깥 반복이 한 번 진행될 때마다 안쪽 반복은 처음부터 끝까지 수행된다.

```python
for outer in range(3):
    for inner in range(2):
        print(outer, inner)
```

위 코드는 바깥 반복 3회와 안쪽 반복 2회를 조합하므로 총 6번 출력한다.

```python
0 0
0 1
1 0
1 1
2 0
2 1
```

### 8.1 별 모양 출력하기

```python
for row in range(1, 6):
    for _ in range(row):
        print("*", end=" ")
    print()
```

출력 결과는 다음과 같다.

```text
*
* *
* * *
* * * *
* * * * *
```

사용하지 않는 반복 변수는 관례적으로 `_`로 작성한다.

### 8.2 2단부터 9단까지 출력하기

```python
for dan in range(2, 10):
    print(f"{dan}단")

    for number in range(1, 10):
        print(f"{dan} * {number} = {dan * number}")

    print()
```

중첩 반복문은 행과 열을 가진 데이터, 구구단, 좌표 조합 등을 처리할 때 자주 사용된다. 다만 반복 횟수는 두 반복 범위의 곱만큼 증가하므로 데이터가 클 때는 실행 비용을 살펴야 한다.

## 9. 컴프리헨션

컴프리헨션(comprehension)은 반복문을 사용해 새로운 컬렉션을 간결하게 생성하는 문법이다. 리스트, 집합, 딕셔너리를 만들 때 사용할 수 있다.

### 9.1 리스트 컴프리헨션

다음 코드는 0부터 9까지의 값을 가진 리스트를 생성한다.

```python
numbers = [number for number in range(10)]

print(numbers)
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

각 값에 연산을 적용할 수도 있다.

```python
numbers = [10, 20, 30, 40]
doubled = [number * 2 for number in numbers]

print(doubled)
# [20, 40, 60, 80]
```

### 9.2 필터링: 조건에 맞는 요소만 포함하기

`for` 문 뒤의 `if`는 결과에 포함할 요소를 고르는 필터 역할을 한다.

```python
even_numbers = [number for number in range(10) if number % 2 == 0]

print(even_numbers)
# [0, 2, 4, 6, 8]
```

위 문법은 다음 반복문과 같은 의미다.

```python
even_numbers = []

for number in range(10):
    if number % 2 == 0:
        even_numbers.append(number)
```

### 9.3 변환: 조건에 따라 저장할 값 바꾸기

모든 요소를 유지하면서 조건에 따라 값을 다르게 저장하려면 표현식 위치에 `if ... else ...`를 작성한다.

```python
numbers = [-1, 0, -4, 24, 5, -10, 2, 20]
converted = [number if number > 0 else 0 for number in numbers]

print(converted)
# [0, 0, 0, 24, 5, 0, 2, 20]
```

두 문법은 모양이 비슷하지만 목적이 다르다.

| 문법 | 목적 | 결과의 길이 |
| --- | --- | --- |
| `[값 for 요소 in 데이터 if 조건]` | 조건에 맞는 요소만 선택한다. | 줄어들 수 있다. |
| `[값1 if 조건 else 값2 for 요소 in 데이터]` | 모든 요소를 조건에 따라 변환한다. | 원본과 같다. |

`else`를 사용하는 조건 표현식은 `for` 앞에 작성해야 한다. 다음 문법은 필터 위치에서 `else`를 사용했으므로 오류가 발생한다.

```python
# SyntaxError가 발생한다.
# result = [number for number in numbers if number > 0 else 0]
```

### 9.4 중첩 리스트 컴프리헨션

```python
products = [i * j for i in range(1, 4) for j in range(1, 3)]

print(products)
# [1, 2, 2, 4, 3, 6]
```

이는 다음 중첩 반복문과 동일한 순서로 실행된다.

```python
products = []

for i in range(1, 4):
    for j in range(1, 3):
        products.append(i * j)
```

컴프리헨션이 지나치게 길거나 조건이 복잡해지면 일반 반복문이 더 읽기 쉬울 수 있다.

### 9.5 세트 컴프리헨션

세트은 중복 값을 허용하지 않는다. 따라서 중복을 제거하면서 값을 가공할 때 세트 컴프리헨션을 사용할 수 있다.

```python
numbers = [1, 2, 3, 4, 5, 2, 3, 4]
unique_numbers = {number for number in numbers}

print(unique_numbers)
# {1, 2, 3, 4, 5}
```

### 9.6 딕셔너리 컴프리헨션

딕셔너리 컴프리헨션은 키와 값을 함께 지정해 새로운 딕셔너리를 생성한다.

```python
names = ["apple", "banana", "orange"]
name_lengths = {name: len(name) for name in names}

print(name_lengths)
# {'apple': 5, 'banana': 6, 'orange': 6}
```

## 10. 반복문 선택 기준

반복 코드를 작성할 때는 목적에 맞는 문법을 선택하는 것이 중요하다.

| 상황 | 적합한 문법 |
| --- | --- |
| 조건이 참인 동안 반복해야 한다. | `while` 문 |
| 컬렉션의 요소를 순서대로 처리한다. | `for` 문 |
| 일정 범위의 숫자를 반복한다. | `for` 문과 `range()` |
| 순서 번호와 값을 함께 사용한다. | `enumerate()` |
| 여러 컬렉션의 값을 함께 처리한다. | `zip()` |
| 특정 요소를 건너뛴다. | `continue` |
| 특정 조건에서 반복을 종료한다. | `break` |
| 간단한 규칙으로 새 컬렉션을 만든다. | 컴프리헨션 |

## 11. 사용자 정의 함수

함수는 특정 작업을 하나의 이름으로 묶어 필요할 때 호출할 수 있게 만든 코드 단위다. 파이썬은 `print()`, `len()`, `range()` 같은 내장 함수를 제공하지만, 프로그램의 요구사항에 맞는 동작은 직접 함수로 정의해야 한다. 이렇게 사용자가 직접 작성한 함수를 사용자 정의 함수라고 한다.

함수를 사용하면 반복되는 코드를 줄이고, 프로그램을 역할별로 분리하며, 한 번 작성한 로직을 여러 곳에서 재사용할 수 있다.

### 11.1 함수 정의와 호출

함수는 `def` 키워드로 정의한다.

```python
def 함수명(매개변수1, 매개변수2):
    실행할 코드
    return 반환값
```

- 함수명은 함수 객체를 가리키는 이름이다.
- 매개변수는 함수가 실행될 때 외부에서 전달받을 값을 위한 이름이다.
- `return`은 실행 결과를 호출한 위치로 돌려준다.

```python
def hello():
    print("안녕하세요")

hello()
```

`def hello(): ...`가 실행되면 파이썬은 함수 객체를 생성하고 `hello`라는 이름을 그 객체에 연결한다. 따라서 함수는 문자열이나 리스트처럼 변수에 저장하거나 다른 함수에 전달할 수 있는 객체다.

### 11.2 함수 객체와 함수 호출 결과

함수 이름 뒤에 괄호를 붙이는지에 따라 의미가 달라진다.

```python
def hello():
    print("안녕하세요")
    return "실행 완료"

a = hello
b = hello()
```

`a = hello`는 함수를 실행하지 않고 함수 객체 자체를 `a`에도 연결한다.

```python
a = hello

print(a)
a()
```

개념적으로는 다음과 같은 상태다.

```text
hello ----┐
          ├----> 함수 객체
a --------┘
```

반면 `b = hello()`는 함수를 즉시 실행하고, `return`으로 반환된 값인 `"실행 완료"`를 `b`에 저장한다.

```python
b = hello()
print(b)
```

| 코드 | 의미 | 저장되는 값 |
| --- | --- | --- |
| `a = hello` | 함수 객체를 참조한다. | 함수 객체 |
| `a()` | `a`가 참조하는 함수를 실행한다. | 반환값을 사용할 수 있다. |
| `b = hello()` | 함수를 즉시 실행한다. | 함수의 반환값 |

함수 객체는 실행할 코드, 기본 매개변수 값, 전역 네임스페이스와의 연결, 클로저 정보 등을 가진다. 필요한 경우 다음 속성으로 확인할 수 있다.

```python
def hello():
    print("안녕하세요")

print(hello)          # 함수 객체를 확인한다.			 
print(hello.__code__) # 함수의 코드 객체를 확인한다. 

# 실행 결과
# <function hello at 0x108e6b420>
# <code object hello at 0x108e80ff0, file "/var/folders/cr/h0m56hfx095g2g1b7pwy0hgh0000gn/T/ipykernel_28955/2992541879.py", line 1>
```

### 11.3 함수 호출과 호출 프레임

함수를 호출하면 해당 호출을 실행하기 위한 독립적인 공간이 만들어진다. 이 공간을 호출 프레임(call frame)이라고 하며, 매개변수와 지역 변수, 현재 실행 위치 등의 정보를 관리한다.

```python
def add(a, b):
    result = a + b
    return result

x = add(3, 5)
print(x)
```

`add(3, 5)`가 실행되는 흐름은 다음과 같다.

1. `add` 이름이 가리키는 함수 객체를 찾는다.
2. 함수 호출을 위한 새로운 프레임을 만든다.
3. 매개변수 `a`에 `3`, `b`에 `5`를 연결한다.
4. 함수 본문을 실행해 지역 변수 `result`에 `8`을 연결한다.
5. `return`으로 결과를 호출 위치에 반환한다.
6. 더 이상 필요한 참조가 없다면 해당 호출 프레임은 정리된다.

같은 함수를 여러 번 호출해도 호출마다 별도의 프레임이 만들어지므로 지역 변수는 서로 충돌하지 않는다.

```python
def add_range(start, end):
    total = 0

    for number in range(start, end + 1):
        total += number

    return total

print(add_range(1, 10))
print(add_range(1, 100))
```

두 번의 호출에서 사용하는 `total`은 각각의 호출 프레임에 속한 별개의 지역 변수다.

### 11.4 매개변수와 반환값이 없는 함수

매개변수와 반환값이 없는 함수는 전달받을 데이터 없이 정해진 동작만 수행한다.

```python
def print_message():
    print("처음으로 만드는 함수다.")

print_message()
print_message()

for _ in range(3):
    print_message()
```

`return`을 작성하지 않은 함수도 실행이 끝나면 자동으로 `None`을 반환한다.

```python
def print_message():
    print("메시지를 출력한다.")

result = print_message()
print(result)  # None
```

### 11.5 매개변수가 있는 함수

매개변수는 함수가 작업에 사용할 값을 전달받는 통로다.

```python
def print_number(number):
    print(f"입력받은 숫자: {number}")

print_number(10)
print_number(4)
```

여러 개의 매개변수를 전달받을 수도 있다.

```python
def print_sum(start, end):
    total = 0

    for number in range(start, end + 1):
        total += number

    print(f"{start}부터 {end}까지의 합: {total}")

print_sum(1, 10)
print_sum(1, 100)
```

함수를 호출할 때는 필요한 인자의 개수에 맞게 값을 전달해야 한다.

```python
def add(num1, num2):
    return num1 + num2

print(add(10, 5))
# print(add(10))  # TypeError가 발생한다.
```

### 11.6 반환값이 있는 함수

`return`은 함수가 처리한 결과를 호출한 위치로 전달한다. 반환된 값은 출력하거나 다른 변수에 저장해 이후 연산에 사용할 수 있다.

```python
def add(num1, num2):
    total = num1 + num2
    return total

print(add(10, 5))

result = add(4, 3)
print(result)
```

함수를 호출한 결과와 함수 자체는 서로 다르다.

```python
def get_gift():
    return "선물"

function_object = get_gift
returned_value = get_gift()

print(function_object)  # 함수 객체가 출력된다.
print(returned_value)   # 선물이 출력된다.
```

### 11.7 중첩 함수 호출과 스택 구조

함수 안에서 다른 함수를 호출할 수 있다. 이때 새 함수 호출 프레임이 기존 프레임 위에 추가되고, 가장 마지막에 호출된 함수부터 실행을 마친다. 이러한 순서를 LIFO(Last In, First Out)라고 한다.

```python
def func_a():
    print("A 시작")
    result = func_b()
    print("A 끝")
    return result

def func_b():
    print("B 시작")
    result = func_c()
    print("B 끝")
    return result

def func_c():
    print("C 실행")
    return 100

value = func_a()
print("최종 결과:", value)
```

출력 순서는 다음과 같다.

```text
A 시작
B 시작
C 실행
B 끝
A 끝
최종 결과: 100
```

호출 순서는 `func_a()`에서 `func_b()`, 다시 `func_c()`로 들어가지만, 종료 순서는 `func_c()`, `func_b()`, `func_a()` 순서가 된다.

> 그림 표현
>
> ![image-20260527163145188](/Users/songjeong-geun/Desktop/KDT/1_PYTHON/images/stack.png)

### 11.8 기본값이 있는 매개변수

매개변수에 기본값을 지정하면 호출 시 해당 인자를 생략할 수 있다.

```python
def add(num1=0, num2=0):
    return num1 + num2

print(add())            # 0
print(add(10))          # 10
print(add(10, 3))       # 13
print(add(num2=3))      # 3
```

기본값이 있는 매개변수를 사용할 때는 변경 가능한 객체를 기본값으로 직접 지정하는 경우를 주의해야 한다. 기본값은 함수가 호출될 때마다 생성되는 것이 아니라, 함수가 정의될 때 한 번 만들어져 재사용된다.

```python
def add_item(item, items=[]): # items=[] 라는 리스트가 선언되면 해시 메모리에 저장되기 때문에 생기는 오류
    items.append(item)
    return items

print(add_item("사과"))   # ['사과']
print(add_item("바나나")) # ['사과', '바나나']
print(add_item("오렌지")) # ['사과', '바나나', '오렌지']
```

각 호출에서 새 리스트를 원했다면 의도하지 않은 결과다. 이러한 경우에는 기본값으로 `None`을 사용하고, 함수 내부에서 새 리스트를 생성한다.

```python
def add_item(item, items=None):
    if items is None:
        items = []

    items.append(item)
    return items

print(add_item("사과"))   # ['사과']
print(add_item("바나나")) # ['바나나']
print(add_item("오렌지")) # ['오렌지']
```

### 11.9 `None`

`None`은 값이 없음을 나타내는 파이썬의 특별한 객체다. 함수에서 `return`을 명시하지 않았을 때 반환되는 값이며, 아직 값이 정해지지 않은 상태를 나타낼 때도 자주 사용한다.

```python
result = None

if result is None:
    print("아직 결과가 없다.")
```

`None`인지 확인할 때는 `==`보다 `is`를 사용하는 것이 권장된다.

```python
value = None

print(value is None)  # True
```

`None`은 조건식에서 `False`로 평가되지만 `0`, 빈 문자열 `""`, 빈 리스트 `[]`와는 의미가 다르다.

### 11.10 가변 위치 인자: `*args`

함수 정의에서 `*args`를 사용하면 전달된 위치 인자를 개수와 관계없이 튜플로 받을 수 있다.

```python
def collect_numbers(*args):
    return args

print(collect_numbers())            # ()
print(collect_numbers(10))          # (10,)
print(collect_numbers(10, 30, 50))  # (10, 30, 50)
```

함수를 호출하는 위치에서 `*`를 사용하면 리스트나 튜플의 요소를 각각의 위치 인자로 펼쳐 전달할 수 있다.

```python
def add_three(a, b, c):
    return a + b + c

numbers = [1, 2, 3]

print(add_three(*numbers))  # add_three(1, 2, 3)과 같다.
```

함수 정의에서 사용하는 `*args`는 여러 인자를 모으는 역할을 하고, 함수 호출에서 사용하는 `*numbers`는 컬렉션의 요소를 펼치는 역할을 한다.

### 11.11 키워드 인자와 `**kwargs`

함수 호출 시 `매개변수명=값` 형태로 전달하면 순서에 관계없이 원하는 매개변수에 값을 연결할 수 있다.

```python
def print_user(user_id, name, age):
    print(f"아이디: {user_id}")
    print(f"이름: {name}")
    print(f"나이: {age}")

print_user("apple", "김사과", 20)
print_user(age=30, user_id="orange", name="오렌지")

# 실행 결과
# 아이디: apple
# 이름: 김사과
# 나이: 20
# 아이디: orange
# 이름: 오렌지
# 나이: 30
```

딕셔너리의 키가 매개변수 이름과 같다면 `**`를 사용해 키워드 인자로 펼칠 수 있다.

```python
user = {
    "age": 25,
    "user_id": "banana",
    "name": "반하나"
}

# 딕셔너리의 키는 반드시 문자열 형태
print_user(**user)

# 실행 결과
# 아이디: banana
# 이름: 반하나
# 나이: 25
```

이때 딕셔너리 키는 문자열이어야 하며 함수의 매개변수 이름과 일치해야 한다.

함수를 정의할 때 `**kwargs`를 사용하면 정해지지 않은 개수의 키워드 인자를 딕셔너리로 받을 수 있다.

```python
def print_profile(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_profile(name="김사과", age=20, city="서울")

# 실행 결과
# name: 김사과
# age: 20
# city: 서울
```

`*`와 `**`의 역할은 다음과 같이 정리할 수 있다.

| 사용 위치 | 문법 | 역할 |
| --- | --- | --- |
| 함수 정의 | `*args` | 여러 위치 인자를 튜플로 모은다. |
| 함수 호출 | `*numbers` | 시퀀스 요소를 위치 인자로 펼친다. |
| 함수 정의 | `**kwargs` | 여러 키워드 인자를 딕셔너리로 모은다. |
| 함수 호출 | `**user` | 딕셔너리를 키워드 인자로 펼친다. |

### 11.12 여러 개의 반환값

파이썬 함수는 여러 값을 쉼표로 구분해 반환할 수 있다. 실제로는 여러 값이 하나의 튜플로 묶여 반환된다.

```python
def calculate(num1=0, num2=1):
    return num1 + num2, num1 - num2, num1 * num2, num1 / num2

result = calculate(10, 3)
print(result)
# (13, 7, 30, 3.3333333333333335)
```

튜플 언패킹을 사용하면 각 결과를 별도의 변수에 저장할 수 있다.

```python
addition, subtraction, multiplication, division = calculate(10, 3)

print(f"덧셈: {addition}")
print(f"뺄셈: {subtraction}")
print(f"곱셈: {multiplication}")
print(f"나눗셈: {division}")
```

사용하지 않을 값은 관례적으로 `_`에 받는다.

```python
_, _, multiplication, _ = calculate(10, 3)

print(f"곱셈: {multiplication}")
```

이 방식은 `enumerate()`에서 인덱스가 필요하지 않은 경우에도 사용할 수 있다.

```python
numbers = [10, 20, 30, 40, 50]

for _, value in enumerate(numbers):
    print(f"값: {value}")
```

## 12. 변수의 범위

변수의 범위(scope)는 변수 이름을 참조하거나 변경할 수 있는 영역을 뜻한다. 함수 내부에서 만든 지역 변수와 함수 외부에서 만든 전역 변수는 접근 가능한 범위가 다르다.

### 12.1 지역 변수

지역 변수(local variable)는 함수 내부에서 정의된 변수다. 해당 함수의 호출 프레임 안에서 사용되며, 함수 밖에서는 직접 접근할 수 없다.

```python
def local_example():
    local_value = "지역 변수"
    print(local_value)

local_example()
# print(local_value)  # NameError가 발생한다.
```

함수를 다시 호출하면 새로운 프레임과 새로운 지역 변수가 만들어진다.

```python
def count_up():
    count = 0
    count += 1
    print(count)

count_up()  # 1
count_up()  # 1
```

각 호출의 `count`는 서로 다른 지역 변수이므로 값이 누적되지 않는다.

### 12.2 전역 변수

전역 변수(global variable)는 함수 외부에서 정의된 변수다. 같은 모듈 안의 함수에서는 전역 변수의 값을 참조할 수 있다.

```python
global_message = "전역 변수다."

def print_global_message():
    print(global_message)

print_global_message()
```

함수 내부에서 전역 변수와 같은 이름에 값을 대입하면 기본적으로 새로운 지역 변수를 만든다. 전역 변수 자체를 수정하려면 `global` 키워드를 명시해야 한다.

```python
global_number = 10

def modify_global():
    global global_number
    global_number = 20

modify_global()
print(global_number)  # 20
```

전역 변수의 수정은 프로그램의 여러 부분에 영향을 줄 수 있으므로 꼭 필요한 경우에만 사용하는 것이 좋다. 가능한 경우에는 함수가 값을 반환하고, 호출한 위치에서 결과를 저장하는 방식이 더 명확하다.

```python
number = 10

def doubled(value):
    return value * 2

number = doubled(number)
print(number)  # 20
```

### 12.3 이름 탐색 순서

함수 안에서 이름을 사용할 때 파이썬은 가까운 범위부터 차례대로 이름을 찾는다. 이를 LEGB 규칙이라고 한다.

| 순서 | 범위 | 의미 |
| --- | --- | --- |
| L | Local | 현재 함수의 지역 범위다. |
| E | Enclosing | 바깥 함수의 지역 범위다. |
| G | Global | 모듈의 전역 범위다. |
| B | Built-in | `print`, `len` 같은 내장 이름의 범위다. |

```python
message = "전역"

def outer():
    message = "바깥 함수"

    def inner():
        message = "현재 함수"
        print(message)

    inner()

outer()  # 현재 함수
```

`inner()`에서는 가장 가까운 지역 범위에 `message`가 있으므로 `"현재 함수"`를 출력한다.

## 마무리

파이썬의 반복문은 데이터를 처리하는 기본 도구이며, 함수는 반복되는 로직을 재사용 가능한 단위로 나누는 도구다. `while` 문과 `for` 문으로 흐름을 만들고, `range()`, `enumerate()`, `zip()`, 컴프리헨션으로 반복 코드를 명확하게 표현할 수 있다.

함수에서는 함수 객체와 함수 호출 결과의 차이를 이해하는 것이 중요하다. 또한 기본값으로 변경 가능한 객체를 사용할 때의 주의점, `*args`와 `**kwargs`의 역할, 지역 변수와 전역 변수의 범위를 알고 있으면 더 안전하고 읽기 쉬운 파이썬 코드를 작성할 수 있다.
