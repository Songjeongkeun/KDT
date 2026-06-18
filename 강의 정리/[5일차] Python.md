# [5일차] Python

파이썬을 배우며 가장 먼저 익숙해져야 할 부분은 **데이터를 어떻게 저장할지**와 **어떤 흐름으로 코드를 실행할지**이다.  
이번 글에서는 컬렉션 자료형인 `tuple`, `set`, `dict`와 제어문인 조건문, 반복문을 예제와 함께 정리한다.

> 예제는 Python 3 기준이며, `match-case`는 Python 3.10 이상에서 사용할 수 있다.

---

## 1. 컬렉션 자료형 한눈에 보기

파이썬에는 여러 데이터를 묶어 다룰 수 있는 컬렉션 자료형이 있다. 어떤 특징이 필요한지에 따라 알맞은 자료형을 선택하면 된다.

| 자료형 | 표기 예시 | 순서 | 중복 | 변경 가능 여부 | 주요 사용 상황 |
| --- | --- | --- | --- | --- | --- |
| 리스트 `list` | `[1, 2, 3]` | 있음 | 허용 | 가능 | 순서대로 저장하고 수정할 데이터 |
| 튜플 `tuple` | `(1, 2, 3)` | 있음 | 허용 | 불가능 | 변경하지 않을 묶음, 좌표, 반환값 |
| 세트 `set` | `{1, 2, 3}` | 없음 | 허용하지 않음 | 가능 | 중복 제거, 집합 연산 |
| 딕셔너리 `dict` | `{"name": "Kim"}` | 삽입 순서 유지 | 키 중복 불가 | 가능 | 키로 값을 조회하는 데이터 |

> `dict`는 Python 3.7부터 입력된 순서를 보장한다. 반면 `set`은 출력 순서에 의존해서는 안 된다.

---

## 2. 튜플(tuple)

튜플은 **순서가 있지만 요소를 변경할 수 없는(immutable) 컬렉션**이다. 한 번 정한 데이터 묶음을 안전하게 유지하고 싶을 때 유용하다.

### 2.1 튜플 생성하기

```python
empty = ()
numbers = (1, 3, 5, 7)
converted = tuple([10, 20, 30])
without_parentheses = "apple", "banana"

print(numbers)              # (1, 3, 5, 7)
print(converted)            # (10, 20, 30)
print(without_parentheses)  # ('apple', 'banana')
```

요소가 하나인 튜플은 반드시 쉼표를 붙여야 한다. 튜플을 만드는 핵심은 괄호보다 **쉼표**이다.

```python
not_tuple = (1)
one_item_tuple = (1,)

print(type(not_tuple))       # <class 'int'>
print(type(one_item_tuple))  # <class 'tuple'>
```

### 2.2 패킹과 언패킹

여러 값을 하나의 튜플로 묶는 것을 **패킹(packing)**, 튜플의 값을 각각의 변수에 나누어 저장하는 것을 **언패킹(unpacking)**이라고 한다.

```python
# 패킹
user = "apple", 25, "Seoul"

# 언패킹
user_id, age, city = user

print(user_id)  # apple
print(age)      # 25
print(city)     # Seoul
```

언패킹을 이용하면 두 변수의 값을 간단히 교환할 수도 있다.

```python
left = 10
right = 20

left, right = right, left
print(left, right)  # 20 10
```

### 2.3 인덱싱과 슬라이싱

튜플은 리스트처럼 위치를 이용해 데이터를 읽을 수 있다.

```python
fruits = ("apple", "banana", "orange", "melon")

print(fruits[0])    # apple
print(fruits[-1])   # melon
print(fruits[1:3])  # ('banana', 'orange')
```

하지만 이미 저장된 튜플의 요소를 다른 값으로 교체할 수는 없다.

```python
fruits = ("apple", "banana")
# fruits[0] = "orange"  # TypeError: 'tuple' object does not support item assignment
```

### 2.4 튜플의 불변성 이해하기

튜플이 변경 불가능하다는 말을 정확히 이해하려면 **변수**와 **객체**를 구분해야 한다.

#### 1. 변수는 객체를 가리키는 이름이다

```python
t = (1, 2)
```

위 코드는 `t`라는 변수가 튜플 `(1, 2)`를 가리키게 만든다. `t` 자체가 튜플 객체인 것이 아니라, 튜플 객체를 참조하는 이름이다.

```text
변수              메모리의 객체

t  ----------->  튜플 A
                 +---+---+
                 | 1 | 2 |
                 +---+---+
```

#### 2. 변수에 새 튜플을 재할당할 수 있다

```python
t = (1, 2)
t = (3, 4)
```

두 번째 줄은 기존 튜플의 내용을 바꾸는 코드가 아니다. 변수 `t`가 다른 튜플 객체를 가리키도록 변경하는 코드이다.

재할당 전의 구조는 다음과 같다.

```text
t  ----------->  튜플 A
                 +---+---+
                 | 1 | 2 |
                 +---+---+
```

재할당 후에는 `t`가 새 튜플을 가리킨다.

```text
                 튜플 A
                 +---+---+
                 | 1 | 2 |
                 +---+---+

t  ----------->  튜플 B
                 +---+---+
                 | 3 | 4 |
                 +---+---+
```

즉, 튜플 A가 튜플 B로 변한 것이 아니라 변수 `t`의 참조 대상이 바뀐 것이다. 더 이상 튜플 A를 가리키는 참조가 없다면 파이썬은 나중에 해당 객체를 정리할 수 있다.

#### 3. 튜플 내부의 요소는 교체할 수 없다

```python
t = (1, 2)
# t[0] = 99  # TypeError: 'tuple' object does not support item assignment
```

`t[0] = 99`는 이미 생성된 튜플의 첫 번째 자리가 가리키는 대상을 `1`에서 `99`로 교체하려는 시도이다. 이 동작은 허용되지 않는다.

```text
t  ----------->  튜플 객체
                 +---+---+
                 | 1 | 2 |
                 +---+---+
                   X
                 첫 번째 자리를 99로 교체할 수 없음
```

튜플은 생성된 뒤 각 자리가 가리키는 요소를 바꿀 수 없으므로 다음 오류가 발생한다.

```text
TypeError: 'tuple' object does not support item assignment
```

#### 4. 리스트와 비교하기

리스트는 변경 가능한 자료형이므로 내부 요소를 교체할 수 있다.

```python
numbers = [1, 2]
numbers[0] = 99

print(numbers)  # [99, 2]
리스트 객체
+---+---+          +----+---+
| 1 | 2 |  ----->  | 99 | 2 |
+---+---+          +----+---+
```

하지만 튜플에서는 같은 방식의 요소 교체가 불가능하다.

```python
numbers = (1, 2)
# numbers[0] = 99  # TypeError
튜플 객체
+---+---+
| 1 | 2 |
+---+---+
  X 첫 번째 자리 교체 불가
```

#### 5. 튜플 안에 리스트가 들어 있다면?

튜플 자체의 요소는 교체할 수 없지만, 요소가 리스트처럼 변경 가능한 객체라면 **그 객체의 내부 값**은 변경할 수 있다.

```python
t = ([1, 2], 3)

# t[0] = [9, 9]  # TypeError: 튜플의 첫 번째 요소를 교체할 수 없음
t[0][0] = 99

print(t)  # ([99, 2], 3)
```

이 경우 튜플의 첫 번째 자리는 처음부터 끝까지 같은 리스트를 가리킨다. 변한 것은 튜플의 연결이 아니라 리스트 객체의 내부 내용이다.

```text
t  ----------->  튜플 객체
                 +---------+---+
                 |    |    | 3 |
                 +----|----+---+
                      |
                      v
                 리스트 객체
                 +----+---+
                 | 99 | 2 |
                 +----+---+
```

> 변수 `t`는 다른 튜플을 가리키도록 바꿀 수 있지만, 한 번 만들어진 튜플 내부의 각 자리가 가리키는 대상은 교체할 수 없다.

```python
t = (1, 2)

t = (3, 4)      # 가능: 변수가 다른 튜플을 가리킴
# t[0] = 99     # 불가능: 튜플 내부 자리 교체
```

### 2.5 튜플 정렬하기

튜플은 변경 불가능하므로 `sort()` 메서드가 없다. 정렬된 결과가 필요하다면 `sorted()`를 사용한다. `sorted()`의 반환값은 리스트이다.

```python
scores = (70, 100, 85, 90)
sorted_scores = sorted(scores, reverse=True)

print(sorted_scores)         # [100, 90, 85, 70]
print(tuple(sorted_scores))  # (100, 90, 85, 70)
print(scores)                # (70, 100, 85, 90)
```

---

## 3. 세트(set)

세트는 **중복을 허용하지 않으며 순서가 없는 컬렉션**이다. 중복 데이터를 제거하거나 합집합, 교집합 같은 집합 연산을 할 때 편리하다.

### 3.1 세트 생성과 중복 제거

```python
numbers = {1, 3, 5, 7}
duplicates = [1, 3, 3, 5, 5, 7]
unique_numbers = set(duplicates)

print(numbers)         # 출력 순서는 달라질 수 있음
print(unique_numbers)  # {1, 3, 5, 7}
```

빈 세트를 만들 때는 주의해야 한다. `{}`는 빈 딕셔너리이고, 빈 세트는 `set()`으로 만든다.

```python
empty_dict = {}
empty_set = set()

print(type(empty_dict))  # <class 'dict'>
print(type(empty_set))   # <class 'set'>
```

리스트에서 중복을 제거하되 최초 등장 순서를 유지하고 싶다면 딕셔너리를 활용할 수 있다.

```python
tags = ["python", "web", "python", "data", "web"]
unique_tags = list(dict.fromkeys(tags))

print(unique_tags)  # ['python', 'web', 'data']
```

### 3.2 요소 추가와 삭제

```python
languages = {"Python", "Java"}

languages.add("JavaScript")
languages.add("Python")       # 이미 있는 값은 추가되지 않음
languages.update(["C", "Go"]) # 여러 요소를 한 번에 추가

languages.remove("Java")      # 없는 값을 삭제하면 KeyError 발생
languages.discard("C")        # 없는 값이어도 오류 없음

print(languages)
```

| 메서드 | 설명 | 주의할 점 |
| --- | --- | --- |
| `add(value)` | 요소 한 개를 추가한다. | 이미 있는 값이면 변화가 없다. |
| `update(iterable)` | 반복 가능한 객체의 요소를 여러 개 추가한다. | 리스트, 튜플, 다른 세트 등을 전달할 수 있다. |
| `remove(value)` | 특정 요소를 삭제한다. | 요소가 없으면 `KeyError`가 발생한다. |
| `discard(value)` | 특정 요소를 삭제한다. | 요소가 없어도 오류가 발생하지 않는다. |
| `pop()` | 임의의 요소 하나를 삭제하고 반환한다. | 빈 세트에서 호출하면 `KeyError`가 발생한다. |
| `clear()` | 모든 요소를 삭제한다. | 실행 후 빈 세트가 된다. |
| `copy()` | 독립된 얕은 복사본을 반환한다. | 원본과 복사본은 서로 다른 세트이다. |

`update()`는 여러 데이터를 한 번에 더할 때 사용한다. 중복된 값은 자동으로 제외된다.

```python
skills = {"Python"}
skills.update(["SQL", "Git", "Python"])

print(skills)  # {'Python', 'SQL', 'Git'}: 출력 순서는 달라질 수 있음
```

`remove()`와 `discard()`는 모두 요소를 제거하지만, 없는 값을 삭제할 때의 동작이 다르다.

```python
colors = {"red", "green", "blue"}

colors.remove("green")
print(colors)  # {'red', 'blue'}

colors.discard("yellow")  # 없는 값이어도 오류 없음
print(colors)             # {'red', 'blue'}

# colors.remove("yellow") # KeyError: 'yellow'
```

`pop()`은 리스트처럼 마지막 값을 꺼내는 메서드가 아니다. 세트에는 순서가 없으므로 어떤 요소가 반환될지에 의존해서는 안 된다.

```python
numbers = {10, 20, 30}
removed = numbers.pop()

print(removed)  # 임의의 요소 하나
print(numbers)  # 제거된 요소를 제외한 세트

numbers.clear()
print(numbers)  # set()
```

`copy()`는 원본과 별개로 변경할 수 있는 복사본을 만든다.

```python
original = {"Python", "SQL"}
copied = original.copy()

copied.add("Git")

print(original)  # {'Python', 'SQL'}
print(copied)    # {'Python', 'SQL', 'Git'}
```

### 3.3 집합 연산

세트의 집합 연산 메서드는 결과를 **새 세트로 반환하며 원본을 변경하지 않는다.**

```python
frontend = {"HTML", "CSS", "JavaScript"}
backend = {"Python", "Java", "JavaScript"}

print(frontend.union(backend))                # 합집합
print(frontend.intersection(backend))         # 교집합: {'JavaScript'}
print(frontend.difference(backend))           # 차집합: {'HTML', 'CSS'}
print(frontend.symmetric_difference(backend)) # 대칭 차집합

print(frontend)  # 원본은 변경되지 않음
```

| 연산 | 메서드 | 의미 |
| --- | --- | --- |
| `a \| b` | `a.union(b)` | 합집합 |
| `a & b` | `a.intersection(b)` | 교집합 |
| `a - b` | `a.difference(b)` | 차집합 |
| `a ^ b` | `a.symmetric_difference(b)` | 대칭 차집합 |

### 3.4 원본을 변경하는 집합 연산 메서드

연산 결과를 새 세트로 받지 않고 현재 세트에 바로 반영하려면 이름 끝에 `_update`가 붙는 메서드를 사용한다.

| 메서드 | 같은 의미의 연산 | 설명 |
| --- | --- | --- |
| `update(other)` | `a \|= b` | 합집합 결과로 원본을 변경한다. |
| `intersection_update(other)` | `a &= b` | 교집합 결과로 원본을 변경한다. |
| `difference_update(other)` | `a -= b` | 차집합 결과로 원본을 변경한다. |
| `symmetric_difference_update(other)` | `a ^= b` | 대칭 차집합 결과로 원본을 변경한다. |

```python
base = {"Python", "SQL", "Git"}
extra = {"Git", "Docker"}

skills = base.copy()
skills.update(extra)
print(skills)  # {'Python', 'SQL', 'Git', 'Docker'}

skills = base.copy()
skills.intersection_update({"Python", "Docker"})
print(skills)  # {'Python'}

skills = base.copy()
skills.difference_update({"SQL", "Java"})
print(skills)  # {'Python', 'Git'}

skills = base.copy()
skills.symmetric_difference_update({"Git", "Docker"})
print(skills)  # {'Python', 'SQL', 'Docker'}
```

원본을 계속 사용해야 하는 경우에는 `intersection()`처럼 새 세트를 반환하는 메서드를 사용하고, 원본 자체를 갱신해도 되는 경우에만 `_update()` 계열을 사용하는 편이 안전하다.

### 3.5 포함 관계와 서로소 확인

세트는 요소를 변경하는 것뿐 아니라, 두 집합 사이의 관계를 검사하는 메서드도 제공한다.

| 메서드 | 설명 | 반환값 |
| --- | --- | --- |
| `issubset(other)` | 현재 세트가 다른 세트의 부분집합인지 확인한다. | `bool` |
| `issuperset(other)` | 현재 세트가 다른 세트를 포함하는지 확인한다. | `bool` |
| `isdisjoint(other)` | 공통 요소가 하나도 없는지 확인한다. | `bool` |

```python
required = {"Python", "SQL"}
applicant = {"Python", "SQL", "Git"}
design = {"Figma", "Photoshop"}

print(required.issubset(applicant))    # True
print(applicant.issuperset(required))  # True
print(required.isdisjoint(design))     # True
```

연산자를 사용해 포함 관계를 표현할 수도 있다.

```python
basic = {"Python", "SQL"}
full = {"Python", "SQL", "Git"}

print(basic <= full)  # 부분집합 여부: True
print(basic < full)   # 진부분집합 여부: True
print(full >= basic)  # 상위집합 여부: True
```

### 3.6 세트 메서드 요약

| 목적 | 사용하는 메서드 |
| --- | --- |
| 요소 한 개 추가 | `add()` |
| 여러 요소 추가 | `update()` |
| 요소 삭제 | `remove()`, `discard()`, `pop()` |
| 모든 요소 삭제 | `clear()` |
| 복사본 생성 | `copy()` |
| 원본을 유지한 집합 연산 | `union()`, `intersection()`, `difference()`, `symmetric_difference()` |
| 원본을 변경하는 집합 연산 | `update()`, `intersection_update()`, `difference_update()`, `symmetric_difference_update()` |
| 집합 간 관계 확인 | `issubset()`, `issuperset()`, `isdisjoint()` |

---

## 4. 딕셔너리(dict)

딕셔너리는 **키(key)와 값(value)의 쌍**으로 데이터를 저장하는 변경 가능한 컬렉션이다. 이름으로 값을 빠르게 찾을 수 있어 사용자 정보나 설정값처럼 의미가 있는 데이터를 표현하기 좋다.

### 4.1 딕셔너리 만들기와 조회하기

```python
user = {
    "id": 1,
    "userid": "apple",
    "name": "김사과",
    "phone": "010-1234-5678",
}

print(user["userid"])       # apple
print(user.get("name"))     # 김사과
print(user.get("gender"))   # None
print(user.get("gender", "미입력"))  # 미입력
```

존재하지 않는 키를 `[]`로 조회하면 `KeyError`가 발생한다. 키가 없을 수도 있는 상황에서는 기본값을 지정할 수 있는 `get()`이 안전하다.

```python
# print(user["email"])            # KeyError
email = user.get("email", "없음")
print(email)                      # 없음
```

### 4.2 데이터 추가, 변경, 삭제

```python
user = {"name": "김사과", "age": 20}

user["city"] = "Seoul"   # 추가
user["age"] = 21         # 변경
removed = user.pop("city")  # 삭제 후 삭제된 값 반환

print(user)     # {'name': '김사과', 'age': 21}
print(removed)  # Seoul
```

### 4.3 딕셔너리의 키 조건

딕셔너리의 키는 변경 불가능한 자료형이어야 한다. 문자열, 숫자, 튜플은 키로 사용할 수 있지만 리스트나 딕셔너리는 사용할 수 없다.

```python
coordinates = {
    (37.5, 127.0): "Seoul",
    (35.1, 129.0): "Busan",
}

print(coordinates[(37.5, 127.0)])  # Seoul

# invalid = {[1, 2]: "list cannot be a key"}  # TypeError
```

### 4.4 반복하며 데이터 꺼내기

```python
scores = {"국어": 95, "영어": 88, "수학": 76}

print(scores.keys())    # 키 모음
print(scores.values())  # 값 모음
print(scores.items())   # (키, 값) 쌍 모음

for subject, score in scores.items():
    print(f"{subject}: {score}점")
```

`in` 연산자는 딕셔너리의 **키가 존재하는지** 확인한다.

```python
scores = {"국어": 95, "영어": 88}

print("국어" in scores)  # True
print(95 in scores)      # False: 값이 아니라 키를 검사함
```

### 4.5 딕셔너리 메서드 한눈에 보기

파이썬의 `dict`가 제공하는 표준 메서드는 다음과 같다.

| 메서드 | 설명 | 원본 변경 여부 |
| --- | --- | --- |
| `dict.fromkeys(keys, value)` | 전달한 키들로 새 딕셔너리를 만든다. | 새 딕셔너리 반환 |
| `get(key[, default])` | 키의 값을 조회하며, 키가 없으면 기본값을 반환한다. | 변경하지 않음 |
| `keys()` | 모든 키를 확인하는 뷰 객체를 반환한다. | 변경하지 않음 |
| `values()` | 모든 값을 확인하는 뷰 객체를 반환한다. | 변경하지 않음 |
| `items()` | 모든 `(키, 값)` 쌍의 뷰 객체를 반환한다. | 변경하지 않음 |
| `setdefault(key[, default])` | 키가 있으면 값을 반환하고, 없으면 기본값을 저장한 뒤 반환한다. | 키가 없으면 변경 |
| `update(other)` | 다른 딕셔너리나 키-값 쌍으로 데이터를 추가하거나 갱신한다. | 변경함 |
| `pop(key[, default])` | 특정 키를 삭제하고 해당 값을 반환한다. | 변경함 |
| `popitem()` | 마지막에 삽입된 키-값 쌍을 삭제하고 튜플로 반환한다. | 변경함 |
| `copy()` | 딕셔너리의 얕은 복사본을 반환한다. | 새 딕셔너리 반환 |
| `clear()` | 모든 키-값 쌍을 삭제한다. | 변경함 |

> `keys()`, `values()`, `items()`의 반환값은 리스트가 아니라 딕셔너리의 변화를 반영하는 **뷰(view) 객체**이다.

### 4.6 `fromkeys()`: 동일한 초기값으로 딕셔너리 만들기

`fromkeys()`는 여러 키에 같은 초기값을 넣어 새 딕셔너리를 만들 때 사용한다. 클래스 메서드이므로 보통 `dict.fromkeys()` 형태로 호출한다.

```python
subjects = ["국어", "영어", "수학"]
scores = dict.fromkeys(subjects, 0)

print(scores)  # {'국어': 0, '영어': 0, '수학': 0}
```

초기값으로 리스트처럼 변경 가능한 객체를 전달하면 모든 키가 같은 객체를 공유하므로 주의해야 한다.

```python
classes = dict.fromkeys(["A반", "B반"], [])
classes["A반"].append("김사과")

print(classes)  # {'A반': ['김사과'], 'B반': ['김사과']}

# 키마다 독립된 리스트가 필요할 때
classes = {name: [] for name in ["A반", "B반"]}
classes["A반"].append("김사과")
print(classes)  # {'A반': ['김사과'], 'B반': []}
```

### 4.7 `get()`: 오류 없이 값 조회하기

```python
user = {"name": "김사과", "city": "Seoul"}

print(user.get("name"))             # 김사과
print(user.get("age"))              # None
print(user.get("age", "미입력"))    # 미입력

# print(user["age"])                # KeyError
```

`get()`은 조회만 수행하며, 키가 없더라도 딕셔너리에 기본값을 추가하지 않는다.

### 4.8 `keys()`, `values()`, `items()`: 키와 값 순회하기

```python
scores = {"국어": 95, "영어": 88, "수학": 76}

print(list(scores.keys()))    # ['국어', '영어', '수학']
print(list(scores.values()))  # [95, 88, 76]
print(list(scores.items()))   # [('국어', 95), ('영어', 88), ('수학', 76)]

for subject, score in scores.items():
    print(f"{subject}: {score}점")
```

뷰 객체는 원본 딕셔너리에 값이 추가되면 그 변화를 반영한다.

```python
menu = {"coffee": 3000}
names = menu.keys()

menu["tea"] = 2500
print(list(names))  # ['coffee', 'tea']
```

### 4.9 `setdefault()`: 기본값을 저장하며 조회하기

`setdefault()`는 키가 이미 있으면 기존 값을 그대로 반환한다. 키가 없으면 기본값을 실제 딕셔너리에 추가한 뒤 반환한다.

```python
profile = {"name": "김사과"}

name = profile.setdefault("name", "익명")
city = profile.setdefault("city", "미입력")

print(name)     # 김사과
print(city)     # 미입력
print(profile)  # {'name': '김사과', 'city': '미입력'}
```

같은 분류의 데이터를 리스트에 모을 때도 사용할 수 있다.

```python
fruits = [("red", "apple"), ("yellow", "banana"), ("red", "strawberry")]
grouped = {}

for color, fruit in fruits:
    grouped.setdefault(color, []).append(fruit)

print(grouped)  # {'red': ['apple', 'strawberry'], 'yellow': ['banana']}
```

### 4.10 `update()`: 여러 데이터를 추가하거나 갱신하기

동일한 키가 있으면 새 값으로 변경하고, 없는 키는 새로 추가한다.

```python
user = {"name": "김사과", "age": 20}

user.update({"age": 21, "city": "Seoul"})
user.update(phone="010-1234-5678")

print(user)
# {'name': '김사과', 'age': 21, 'city': 'Seoul', 'phone': '010-1234-5678'}
```

`update()`에는 `(키, 값)` 형태의 튜플을 담은 리스트도 전달할 수 있다.

```python
settings = {"theme": "light"}
settings.update([("theme", "dark"), ("language", "korea")])

print(settings)  # {'theme': 'dark', 'language': 'korea'}
```

### 4.11 `pop()`과 `popitem()`: 항목 삭제하기

`pop()`은 삭제할 키를 지정하고, `popitem()`은 마지막에 삽입된 항목을 삭제한다. 딕셔너리는 Python 3.7부터 삽입 순서를 보장하므로 `popitem()`은 마지막 키-값 쌍을 반환한다.

```python
user = {"name": "김사과", "age": 20, "city": "Seoul"}

city = user.pop("city")
email = user.pop("email", "미입력")

print(city)   # Seoul
print(email)  # 미입력
print(user)   # {'name': '김사과', 'age': 20}
queue = {"first": "apple", "second": "banana", "third": "orange"}
last_item = queue.popitem()

print(last_item)  # ('third', 'orange')
print(queue)      # {'first': 'apple', 'second': 'banana'}
```

기본값 없이 존재하지 않는 키를 `pop()`으로 삭제하거나, 빈 딕셔너리에서 `popitem()`을 호출하면 `KeyError`가 발생한다.

### 4.12 `copy()`와 `clear()`: 복사하고 비우기

```python
original = {"name": "김사과", "age": 20}
copied = original.copy()

copied["age"] = 21

print(original)  # {'name': '김사과', 'age': 20}
print(copied)    # {'name': '김사과', 'age': 21}

copied.clear()
print(copied)    # {}
```

`copy()`는 얕은 복사(shallow copy)이므로 값으로 리스트 같은 변경 가능한 객체를 가지고 있다면 내부 객체는 공유된다.

```python
original = {"tags": ["python"]}
copied = original.copy()

copied["tags"].append("data")

print(original)  # {'tags': ['python', 'data']}
print(copied)    # {'tags': ['python', 'data']}
```

내부 객체까지 완전히 분리해야 한다면 데이터 구조에 맞게 새 객체를 만들거나 `copy.deepcopy()` 사용을 고려한다.

### 4.13 딕셔너리 메서드 요약

| 목적 | 사용하는 메서드 |
| --- | --- |
| 키로 초기화된 새 딕셔너리 생성 | `dict.fromkeys()` |
| 키를 안전하게 조회 | `get()` |
| 키, 값, 키-값 쌍 확인 | `keys()`, `values()`, `items()` |
| 없는 키에 기본값 추가 | `setdefault()` |
| 여러 항목 추가 또는 갱신 | `update()` |
| 지정한 키 삭제 | `pop()` |
| 마지막 삽입 항목 삭제 | `popitem()` |
| 복사본 생성 | `copy()` |
| 전체 항목 삭제 | `clear()` |

---

## 5. 조건문

조건문은 조건의 결과가 `True`인지 `False`인지에 따라 실행할 코드를 선택한다.

### 5.1 `if`, `elif`, `else`

```python
age = int(input("나이를 입력하세요: "))

if age >= 19:
    print("성인이다.")
elif age >= 13:
    print("청소년이다.")
elif age >= 0:
    print("어린이다.")
else:
    print("나이는 0 이상으로 입력해주세요.")
```

`if-elif-else`는 위에서부터 조건을 검사하고, 처음으로 참인 블록 하나만 실행한다. 조건의 범위가 겹친다면 **더 좁거나 큰 기준을 먼저 검사**하는 것이 중요하다.

### 5.2 참 같은 값과 거짓 같은 값

파이썬에서는 `True`, `False`뿐만 아니라 객체의 값 자체도 조건으로 사용할 수 있다.

| 평가 결과 | 예시 |
| --- | --- |
| `False`로 평가되는 값 | `False`, `None`, `0`, `""`, `[]`, `{}`, `set()` |
| `True`로 평가되는 값 | 비어 있지 않은 문자열/컬렉션, `0`이 아닌 숫자 |

```python
nickname = input("닉네임을 입력하세요: ")

if nickname:
    print(f"반갑다, {nickname}!")
else:
    print("닉네임이 비어 있다.")
```

### 5.3 여러 조건 결합하기

`and`, `or`, `not`을 이용해 조건을 결합할 수 있다.

```python
user_id = input("아이디: ")
password = input("비밀번호: ")

if user_id == "admin" and password == "1234":
    print("로그인되었다.")
else:
    print("아이디 또는 비밀번호를 확인해주세요.")
```

실제 서비스에서는 비밀번호를 코드에 직접 적거나 평문으로 저장하지 않고, 안전한 인증 처리와 암호화된 저장 방식을 사용해야 한다.

### 5.4 독립된 `if`와 `elif`의 차이

다음 코드는 조건 중 하나만 실행된다.

```python
score = 85

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("F")

# B
```

반면 `if`를 각각 사용하면 조건이 참일 때마다 모두 실행된다.

```python
score = 85

if score >= 80:
    print("80점 이상")
if score >= 70:
    print("70점 이상")

# 80점 이상
# 70점 이상
```

### 5.5 조건부 표현식

참과 거짓에 따라 단순히 값 하나를 선택할 때는 조건부 표현식을 사용할 수 있다.

```python
number = int(input("숫자를 입력하세요: "))
result = "짝수" if number % 2 == 0 else "홀수"

print(result)
참일 때의 값 if 조건 else 거짓일 때의 값
```

여러 조건을 한 줄에 중첩하면 오히려 읽기 어려워진다. 분기가 많을 때는 일반적인 `if-elif-else`가 더 좋은 선택이다.

### 5.6 왈러스 연산자 `:=`

Python 3.8부터는 표현식 안에서 값을 변수에 할당하는 **할당 표현식**을 사용할 수 있다. 같은 계산을 반복하지 않아도 될 때 유용하다.

```python
text = input("아이디를 입력하세요: ")

if (length := len(text)) < 3:
    print(f"아이디가 너무 짧다. ({length}글자)")
else:
    print(f"사용 가능한 아이디다. ({length}글자)")
```

간단한 상황에서는 편리하지만, 무리하게 사용하면 코드 흐름을 이해하기 어려워질 수 있다.

### 5.7 구조적 패턴 매칭: `match-case`

Python 3.10부터 사용할 수 있는 `match-case`는 하나의 값을 여러 패턴과 비교하거나, 데이터 구조를 분해하며 분기할 때 유용하다.

```python
month = int(input("월을 입력하세요 (1~12): "))

match month:
    case 1 | 3 | 5 | 7 | 8 | 10 | 12:
        print(f"{month}월은 31일까지 있다.")
    case 4 | 6 | 9 | 11:
        print(f"{month}월은 30일까지 있다.")
    case 2:
        print("2월은 평년에는 28일, 윤년에는 29일까지 있다.")
    case _:
        print("1부터 12 사이의 숫자를 입력해주세요.")
```

튜플이나 딕셔너리처럼 구조가 있는 데이터도 패턴으로 꺼낼 수 있다.

```python
user = ("김사과", 20)

match user:
    case (name, age) if age >= 19:
        print(f"{name}님은 성인이다.")
    case (name, age) if age >= 13:
        print(f"{name}님은 청소년이다.")
    case (name, age):
        print(f"{name}님은 어린이다.")
    case _:
        print("사용자 데이터 형식이 올바르지 않다.")
```

딕셔너리를 매칭하면 필요한 키의 값을 변수로 추출할 수도 있다.

```python
scores = {"국어": 95, "영어": 88, "수학": 76}

match scores:
    case {"국어": korean, "영어": english, "수학": math}:
        average = (korean + english + math) / 3
        print(f"평균: {average:.1f}점")
    case _:
        print("세 과목의 점수를 모두 입력해주세요.")
```

**MBTI 예제**

```python
print("MBTI 간단 성격 유형 검사에 오신 걸 환영합니다!")

# 첫 번째 질문: 외향/내향
answer1 = input("Q1. 새로운 사람들과 만나는 걸 좋아하시나요? (y/n): ")
if answer1.lower() == 'y':
    # 외향형으로 진행
    print("외향형으로 분석 중...")
    answer2 = input("Q2. 주변 환경에 대해 자주 인지하고 있나요? (y/n): ")
    if answer2.lower() == 'y':
        # 감각형(외향, 감각)
        answer3 = input("Q3. 결정을 내리고 문제를 해결할 때 구체적인 정보를 중요하게 생각하시나요? (y/n): ")
        # 사고형(외향, 감각, 사고)
        if answer3.lower() == 'y':
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            # 계획형(외향, 감각, 사고, 계획)
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 ESTJ입니다!")
            else:
                print("당신의 성격 유형은 ESTP입니다!")
        else:
            # 감정형(외향, 감각, 감정)
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 ESFJ입니다!")
            else:
                print("당신의 성격 유형은 ESFP입니다!")
    else:
        # 직관형(외향, 직관)
        answer3 = input("Q3. 결정을 내리고 문제를 해결할 때 구체적인 정보를 중요하게 생각하시나요? (y/n): ")
        if answer3.lower() == 'y':
        # 사고형(외향, 직관, 사고)
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 ENTJ입니다!")
            else:
                print("당신의 성격 유형은 ENTP입니다!")
        else:
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 ENFJ입니다!")
            else:
                print("당신의 성격 유형은 ENFP입니다!")
else:
    # 내향형으로 진행
    print("내향형으로 분석 중...")
    answer2 = input("Q2. 주변 환경에 대해 자주 인지하고 있나요? (y/n): ")
    if answer2.lower() == 'y':
        # 감각형(내향, 감각)
        answer3 = input("Q3. 결정을 내리고 문제를 해결할 때 구체적인 정보를 중요하게 생각하시나요? (y/n): ")
        if answer3.lower() == 'y':
            # 사고형(내향, 감각, 사고)
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 ISTJ입니다!")
            else:
                print("당신의 성격 유형은 ISTP입니다!")
        else:
            # 감정형(내향, 감각, 감정)
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 ISFJ입니다!")
            else:
                print("당신의 성격 유형은 ISFP입니다!")
    else:
        # 직관형(내향, 직관)
        answer3 = input("Q3. 결정을 내리고 문제를 해결할 때 구체적인 정보를 중요하게 생각하시나요? (y/n): ")
        if answer3.lower() == 'y':
        # 사고형(내향, 직관, 사고)
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 INTJ입니다!")
            else:
                print("당신의 성격 유형은 INTP입니다!")
        else:
            answer4 = input("Q4. 계획을 세우는 것을 좋아하시나요? (y/n): ")
            if answer4.lower() == 'y':
                print("당신의 성격 유형은 INFJ입니다!")
            else:
                print("당신의 성격 유형은 INFP입니다!")              
```





---

## 7. 마무리

이번 글에서 정리한 핵심은 다음과 같다.

| 주제 | 핵심 |
| --- | --- |
| 튜플 | 순서는 유지되지만 요소를 교체할 수 없는 컬렉션 |
| 세트 | 중복 제거와 집합 연산에 적합한 컬렉션 |
| 딕셔너리 | 키와 값으로 의미 있는 데이터를 표현하는 컬렉션 |
| 조건문 | 조건에 따라 실행 흐름을 선택하는 문법 |

자료형을 고르는 기준과 제어문의 흐름을 익히면, 단순한 문법 연습에서 벗어나 데이터를 가공하는 프로그램을 만들 수 있다. 다음 단계로는 리스트 컴프리헨션, 함수, 예외 처리를 공부하며 지금까지의 코드를 더 간결하고 안전하게 발전시켜볼 수 있다.