

# [3일차] Python

## 파이썬 변수

### 3. 변수

변수는 프로그램에서 데이터를 저장하고 사용하기 위해 붙이는 **이름**이다.

Python에서 변수는 값을 직접 저장하는 공간이라기보다, **메모리에 생성된 객체를 참조하는 이름**에 가깝다.

```python
a = "memory"
```

위 코드는 `"memory"` 라는 문자열 객체를 메모리에 생성하고, 변수 `a`가 그 객체를 참조하도록 만든다.

즉, Python에서는 다음과 같이 이해할 수 있다.

```tex
변수 이름 a ➡ 문자열 객체 "memory"
```

![img](https://blog.kakaocdn.net/dna/HOpEd/dJMcaciqTVT/AAAAAAAAAAAAAAAAAAAAAA5EO3wBeMFcqoZKBT-oeOq7Z9-6mdxGg6V5kGG8ajBk/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1780239599&allow_ip=&allow_referer=&signature=hjVh2qXYDVajCmDf9D%2BLCtBSJFY%3D)

**1. Python의 변수 동작 방식**

```python
x = 10
```

위 코드가 실행되면 Python 내부에서는 다음과 같은 일이 일어난다.

1. `10`이라는 정수 객체가 메모리에 생성된다.
2. 변수 이름 `x`가 해당 객체를 참조한다.
3. 변수 이름과 객체의 연결 정보는 네임스페이스에 저장된다.

Python에서 변수는 "값을 담는 상자"라기보다 **객체를 가리키는 이름**이라고 보는 것이 더 정확하다.

```python
x = 10
y = x 
```

이 경우 `x` 와 `y`가 같은 객체 `10` 을 참조한다.

```python
print(x is y) # True
print(id(x)  # 4351736152
print(id(y))  # 4351736152
```

- `is` : 두 변수가 같은 객체를 참조하는지 확인하는 연산자
- `id()` : 객체의 고유 식별값을 확인하는 함수

> **메모리 구조**
>
> 프로그램이 실행되면 메모리는 역할에 따라 여러 영역으로 나뉘어 사용된다.
>
> 1. Code 영역
>    - 프로그램의 실행 코드가 저장되는 영역이다.
>    - 작성한 명령문이나 함수의 코드 정보가 이 영역에 올라간다.
> 2. Stack 영역
>    - 함수 호출과 관련된 정보가 저장되는 영역이다.
>    - 지역 변수, 함수의 실행 흐름, 호출 정보 등이 저장되며, 함수 실행이 끝나면 해당 정보는 제거된다.
> 3. Heap 영역
>    - 객체가 저장되는 영역이다.
>    - Python에서 숫자, 문자열, 리스트, 딕셔너리 같은 객체들은 주로 Heap 영역에 생성된다.

 **네임스페이스**

Python에서 변수 이름은 네임스페이스(namespace)에 저장된다.

네임스페이스는 이름과 객체의 연결 관계를 관리하는 공간이며, 딕셔너리 형태로 동작한다.

전역 네임스페이스는 `globals()` 함수를 통해 확인할 수 있다.

```python
name = "김사과"
age = 20

print(globals())
```

출력 예시 :

```tex
{'__name__': '__main__', '__doc__': 'Automatically created module for IPython interactive environment', '__package__': None, '__loader__': ...
```

`globals()` 는 현재 모듈의 전역 네임스페이스를 딕션너리 형태로 반환한다.

이를 통해 변수 이름이 어떤 객체와 연결되어 있는지 확인할 수 있다.



**2. 변수 이름 작성하는 방법**

Python에서 변수 이름을 작성할 때는 다음 규칙을 지켜야 한다.

1. 알파벳, 숫자, 밑줄`_` 을 사용할 수 있다.
2. 숫자로 시작할 수 없다.
3. 공백을 포함할 수 없다.
4. Python 예약어는 변수 이름으로 사용할 수 없다.
5. 대소문자를 구분한다.

```python
name = "Python"
user_age = 20
_count = 10
```

잘못된 예시는 다음과 같다.

```python
1name = "Python" # 숫자로 시작할 수 없음
user age = 20		 # 공백 사용 불가
class = "A"			 # 예약어 사용 불가
```

> **예약어(Keyword)**
>
> 이미 Python 문법에서 특별한 의미로 사용되고 있는 단어이다.
>
> 즉, 예약어는 변수명, 함수명, 클래스명 등으로 사용할 수 없다.
>
> 예를 들어, `if`, `for`, `class` 같은 단어들은 Python 문법 자체에 사용되기 때문에 다른 용도로 이름을 지을 수 없다.

### 4.자료형

자료형은 데이터의 종류를 의미한다.

Python은 변수에 저장되는 값에 따라 자료형이 자동으로 결정되는 **동적 타입 언어**이다.

```python
a = 10
b = "Python"
c = True
```

> **동적 타입 언어(Dynamic Typed Language)**
>
> 동적 타입 언어는 **변수를 선언할 때 자료형을 미리 지정하지 않아도 되는 언어**이다.
>
> 즉, 값이 들어갈 때 자동으로 타입이 결정된다.
>
> 대표적인 동적 타입 언어 :
>
> - Python
> - JavaScript
> - Ruby
> - PHP
>
> vs 
>
> 
>
> **정적 타입 언어(Static Typed Language)**
>
> 정적 타입 언어는 **변수를 선언할 때 자료형을 미리 지정해야 하는 언어**이다.
>
> 그리고 한 번 정한 타입은 기본적으로 변경할 수 없다.
>
> 대표적인 정적 타입 언어 :
>
> - Java
> - C / C++
> - Go
> - Rust

**1. 기본 자료형 (Primitive Data Types)**

- 숫자형(Number)

  숫자를 표현하는 자료형이다.

  ```python
  a = 10		# int
  b = 3.14	# float
  ```

  - `int` : 정수형
  - `float` : 실수형

- 문자열형 (str)

  문자들의 집합을 표현하는 자료형이다.

  ```python
  name = "Python"
  message = 'Hello'
  ```

  문자열은 큰따옴표 `"` 또는 작은따옴표 `'`를 사용해서 작성할 수 있다.

- 불린형(bool)

  참과 거짓을 표현하는 자료형이다.

  ```python
  is_active = True
  is_login = False
  ```

  불린형은 조건문에서 자주 사용된다.

### 5. 자료형 변환

자료형 변환(Type Casting)은 하나의 데이터 타입을 다른 타입으로 바꾸는 것을 의미한다.

입력값을 계산하거나 출력 형식을 맞출 때 자주 사용된다.

1. 정수형 ➡ 실수형

   ```python
   a = 10
   b = float(a)
   
   print(b) # 10.0
   ```

2. 실수형 ➡ 정수형

   ```python
   c = 3.14
   d = int(c)
   
   print(d) # 3
   ```

   `int()` 를 사용하면 소수점 아래 값은 버려진다.

3. 문자형 ➡ 정수형, 실수형

   ```python
   e = "100"
   
   f = int(e)
   g = float(e) 
   
   print(f)	# 100
   print(g)	# 100.0
   ```

   단, 숫자로 바꿀 수 없는 문자열은 오류가 발생한다.

   ```python
   int("Hello")	# ValueError
   ```

4. 정수형, 실수형 ➡ 문자형

   ```python
   h = 42
   i = str(h)
   
   j = 3.14
   k = str(j)
   
   print(i)	# "42"
   print(k) 	# "3.14"
   ```

### 6. 변수 삭제하기

변수를 삭제할 때는 `del` 문을 사용할 수 있다.

```python
name = "Python"

del name

print(name) # NameError
```

`del name`을 실행하면 변수 이름 `name` 이 네임스페이스에서 제거된다.

따라서 이후에는 해당 이름으로 값에 접근할 수 없다.

다만 `del` 은 변수 이름과 객체의 연결을 끊는 것이며, 객체 자체가 항상 즉시 삭제되는 것은 아니다.

해당 객체를 다른 변수가 참조하고 있다면 객체는 계속 메모리에 남아 있다.

```python
a = [1, 2, 3]
b = a

del a

print(b)	# [1, 2, 3]
```

위 코드에서 `a` 는 삭제되었지만, `b`가 여전히 리스트 객체를 참조하고 있으므로 리스트는 사라지지 않는다.

**참조 횟수와 가비지 컬렉션**

Python 객체는 자신을 참조하는 대상이 몇 개인지 나타내는 **참조 횟수(reference count)** 정보를 가진다.

```python
a = [1, 2, 3]
b = a 
```

위 코드에서 리스트 객체 [1, 2, 3] 은 `a` 와 `b`가 함께 참조하고 있다.

```python
del a
```

`a`를 삭제해도 `b`가 여전히 리스트를 참조하고 있기 때문에 객체는 메모리에서 바로 제거되지 않는다.

```python
del b
```

이제 리스트를 참조하는 이름이 없어지면 참조 횟수가 0이 되고, Python은 해당 객체를 더 이상 사용하지 않는 객체로 판단하여 메모리에서 정리할 수 있다.

이처럼 Python은 사용하지 않는 객체를 자동으로 정리하는 **가비지 컬렉션(Garbage Collection)** 기능을 제공한다.



## 문자열 다루기

### 1. 컴퓨터에서 문자를 저장하는 방법

컴퓨터는 문자를 사람이 보는 글자 그대로 저장하지 않는다. 대신 각 문자에 대응되는 **숫자 코드**로 변환한 뒤, 이 숫자를 0과 1의 이진수 형태로 저장한다.

이처럼 문자와 숫자를 서로 대응시키는 규칙을 **문자 인코딩(Character Encoding)** 이라고 한다. 대표적인 문자 인코딩 방식으로는 ASCII와 Unicode가 있다.

```text
문자 → 숫자 코드 → 이진수 저장 → 문자로 출력
```

#### 1. ASCII

ASCII는 **American Standard Code for Information Interchange**의 약자로, 미국에서 개발된 문자 인코딩 표준이다.

ASCII는 7비트로 구성되어 있으며, 총 128개의 문자(0~127)를 표현할 수 있다.

- 영어 알파벳
- 숫자
- 일부 특수문자
- 제어 문자

하지만 ASCII는 영어 중심의 문자만 표현할 수 있기 때문에 한글, 한자, 일본어 등 다양한 문자를 표현하기에는 한계가 있다.

#### 2. Unicode

Unicode는 전 세계의 다양한 문자와 기호를 표현하기 위해 만들어진 문자 표준이다. Unicode는 각 문자에 고유한 번호인 **코드 포인트(Code Point)** 를 부여한다.

```text
A → U+0041
가 → U+AC00
```

Unicode 자체는 문자에 번호를 부여하는 표준이고, 실제로 컴퓨터에 저장하거나 전송하기 위해서는 UTF-8, UTF-16, UTF-32 같은 인코딩 방식이 사용된다.

#### 3. UTF

UTF는 **Unicode Transformation Format**의 약자로, Unicode 문자를 실제 바이트 형태로 저장하거나 전송하기 위한 인코딩 방식이다.

대표적인 UTF 인코딩 방식은 다음과 같다.

- **UTF-8**
- **UTF-16**
- **UTF-32**

그중 **UTF-8**은 가장 널리 사용되는 인코딩 방식이다. UTF-8은 가변 길이 인코딩 방식으로, 문자에 따라 사용하는 바이트 수가 달라진다.

```text
영어 문자 → 보통 1바이트
한글 문자 → 보통 3바이트
```

UTF-8은 ASCII와 호환되고 저장 효율이 좋아 웹, 파일, 데이터 통신 등에서 많이 사용된다.

#### 4. 컴퓨터의 용량 단위

컴퓨터는 데이터를 0과 1로 저장한다. 가장 작은 단위는 **bit**이고, 8bit가 모이면 **1Byte**가 된다.

> 일반적으로 컴퓨터 용량 단위는 1024를 기준으로 커진다.

```text
1 Byte = 8 bit

1 KB = 1024 Byte
1 MB = 1024 KB
1 GB = 1024 MB
1 TB = 1024 GB
```

---

### 2. Python의 문자열

문자열(String)은 문자들이 순서대로 모인 자료형이다. Python에서는 작은따옴표 `' '` 또는 큰따옴표 `" "`를 사용해 문자열을 표현한다.

```python
str1 = '오늘도 즐거운 파이썬 수업'
print(str1)	# 오늘도 즐거운 파이썬 수업

str2 = "오늘도 즐거운 파이썬 수업"
print(str2)	# 오늘도 즐거운 파이썬 수업
```

여러 줄 문자열은 큰따옴표 세 개 `""" """` 또는 작은따옴표 세 개 `''' '''`를 사용해 작성할 수 있다.

```python
str3 = '''김사과 :
오늘도 즐거운 파이썬
수업'''
print(str3)	# 김사과 : 
						# 오늘도 즐거운 파이썬
  					# 수업
```

Python의 문자열은 내부적으로 Unicode 기반으로 처리된다. 따라서 영어뿐만 아니라 한글, 이모지, 다양한 기호도 문자열로 다룰 수 있다.

```python
text = "Python 문자열 😊"
print(text)	# Python 문자열 😊
```

>**문자열 포매팅**
>
>Python에서는 f-string을 사용해 변수 값을 문자열 안에 쉽게 넣을 수 있다.
>
>```python
>name = "김사과"
>age = 20
>
>message = f"{name}님은 {age}살입니다."
>print(message) # 김사과님은 20살입니다.
>```

> **`str` 변수명은 피하기**
>
> `str` 은 Python 내장 타입 이름이라 보통 `text`같은 이름을  쓴다. 

-----------------------

### 3. 문자열의 인덱스

인덱스(Index)는 문자열이나 리스트처럼 순서가 있는 자료형에서 각 요소의 위치를 나타내는 번호이다. Python의 인덱스는 **0부터 시작**한다.

```python
text = "Hello"

print(text[0])   # H
print(text[1])   # e
print(text[-1])  # o
print(text[-2])  # l
```

음수 인덱스를 사용하면 뒤에서부터 접근할 수 있다.

```text
 H   e   l   l   o
 0   1   2   3   4
-5  -4  -3  -2  -1
```

---

### 4. 문자열의 불변성

Python의 문자열은 **불변(Immutable) 데이터 타입**이다. 즉, 한 번 생성된 문자열 객체의 내용은 직접 수정할 수 없다.

```python
text = "Hello"
text[0] = "h"  # TypeError
```

문자열을 변경하는 것처럼 보이는 코드는 실제로 기존 문자열을 수정하는 것이 아니라, 새로운 문자열 객체를 생성한다.

```python
text = "Hello"
print(id(text))

text = "Python"
print(id(text))
```

위 코드에서 `text` 변수는 처음에는 `"Hello"` 객체를 참조하다가, 이후 `"Python"`이라는 새로운 문자열 객체를 참조하게 된다.

---

### 5. 리터럴 공유

Python은 메모리 효율을 위해 같은 값을 가지는 불변 객체를 공유하기도 한다. 이를 **리터럴 공유(Literal Sharing)** 또는 **인터닝(Interning)** 이라고 한다.

```python
a = "Hello"
b = "Hello"

print(a is b)  # True
```

다만 모든 문자열이 항상 공유되는 것은 아니다. 짧고 단순한 문자열이나 컴파일 시점에 결정 가능한 문자열은 공유될 가능성이 높지만, 런타임에 새로 생성된 문자열은 다른 객체로 만들어질 수 있다.

```python
a = "Hello"
b = "".join(["H", "e", "l", "l", "o"])

print(a == b)  # True
print(a is b)  # 실행 환경에 따라 다를 수 있음
```

- `==`: 값이 같은지 비교
- `is`: 같은 객체를 참조하는지 비교

> 일반적인 값 비교에는 `is` 가 아니라 `==` 를 사용한다.
>
> `is`는 두 변수가 같은 객체를 참조하는지 확인할 때 사용한다.

---

### 6. 문자열 함수와 연산자

#### 1. 문자열 길이 확인

`len()` 함수를 사용하면 문자열의 길이를 확인할 수 있다.

```python
text = "Hello, Python!"
print(len(text))  # 14
```

#### 2. 문자열 합치기

`+` 연산자를 사용하면 문자열을 연결할 수 있다.

```python
name = "김사과"
age = "20살"

message = name + ", " + age
print(message)  # 김사과, 20살
```

#### 3. 문자열 반복하기

`*` 연산자를 사용하면 문자열을 반복할 수 있다.

```python
apple = "🍎" * 10
print(apple) # 🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎
```

#### 4. 문자열 인덱싱

인덱싱(Indexing)은 문자열에서 특정 위치의 문자를 가져오는 방법이다.

```python
text = "문자열 내부의 문자에 인덱스를 사용하여 접근할 수 있습니다."

print(text[0])	# 문
print(text[1])	# 자
print(text[-1])	# .
print(text[-2])	# 다
```

#### 5. 문자열 슬라이싱

슬라이싱(Slicing)은 문자열에서 원하는 범위만 잘라 가져오는 방법이다.

```python
text = "문자열 내부의 문자에 인덱스를 사용하여 접근하거나 슬라이스할 수 있습니다."

print(text[0:6])	# 문자열 내부
print(text[8:16])	# 문자에 인덱스를
print(text[:16])	# 문자열 내부의 문자에 인덱스를
print(text[8:])		# 문자에 인덱스를 사용하여 접근하거나 슬라이스할 수 있습니다.
```

슬라이싱은 다음 형식으로 사용한다.

```python
문자열[start:end]
```

- `start`: 시작 인덱스
- `end`: 끝 인덱스
- `start`부터 `end - 1`까지 가져온다.

step 값을 추가하면 일정한 간격으로 문자를 가져올 수 있다.

>**step**
>
>슬라이싱에서는 'start' , 'end' 외에도 'step' 값을 사용할 수 있다.
>
>```python
>문자열[start:end:step]
>```
>
>- `start`: 시작 인덱스
>- `end`: 끝 인덱스
>- `step`: 몇 칸씩 건너뛰며 가져올지 지정
>
>예를 들어 `step`이 `2`이면 한 글자씩 건너뛰면서 가져온다.
>
>```python
>text = "Python"
>
>print(text[0:6:1])  # Python
>print(text[0:6:2])  # Pto
>print(text[1:6:2])  # yhn
>```
>
>`start`와 `end`를 생략하고 `step`만 사용할 수도 있다.
>
>```python
>text = "Python"
>
>print(text[::1])  # Python
>print(text[::2])  # Pto
>print(text[::3])  # Ph
>```
>
>`step`에 음수를 사용하면 문자열을 뒤에서 앞으로 가져온다.
>
>```python
>text = "Python"
>
>print(text[::-1])  # nohtyP
>print(text[::-2])  # nhy
>```
>
>특히 `[::-1]`은 문자열을 뒤집을 때 자주 사용된다.
>
>```python
>text = "Hello"
>
>reversed_text = text[::-1]
>
>print(reversed_text)  # olleH
>```

> **문자열 포함 여부 확인**
>
> `in` 연산자를 사용하면 특정 문자열이 포함되어 있는지 확인할 수 있다.
>
> ```python
> text = "Hello, Python!"
> 
> print("Python" in text)	# True
> print("Java" in text)		# False
> ```
>
> ➡ 반대로  `not in` 을 사용하면 특정 문자열이 포함되어 있지 않은지 확인할 수 있다.

---

### 7. 문자열 메서드

문자열 메서드는 문자열 객체에 사용할 수 있는 함수이다. 문자열을 변환하거나 검색, 분리, 결합하는 등 다양한 작업을 할 수 있다.

#### 1. 대소문자 변환

```python
text = "Hello, Python!"

print(text.upper())  # HELLO, PYTHON!
print(text.lower())  # hello, python!
```

> **이스케이프 문자 **
>
> 이스케이프 문자는 문자열 안에서 줄바꿈, 탭, 따옴표 등을 표현할 때 사용한다.
>
> ```python
> print("Hello\nPython")       # 줄바꿈
> print("Hello\tPython")       # 탭
> print("I said \"Hello\"")    # 큰따옴표 출력
> ```
>
> 대표적인 이스케이프 문자는 다음과 같다.
>
> | 문자 | 의미            |
> | ---- | --------------- |
> | `\n` | 줄바꿈          |
> | `\t` | 탭              |
> | `\\` | 역슬래시 출력   |
> | `\'` | 작은따옴표 출력 |
> | `\"` | 큰따옴표 출력   |

#### 2. 특정 문자열의 등장 횟수 확인

```python
text = "Hello, Python!"

print(text.count("l"))   # 2
print(text.count("ll"))  # 1
```

#### 3. 특정 문자열의 위치 확인

`find()`는 특정 문자열이 처음 등장하는 위치를 반환한다. 찾는 값이 없으면 `-1`을 반환한다.

```python
text = "Hello, Python!"

print(text.find("l"))     # 2
print(text.find("ll"))    # 2
print(text.find("z"))     # -1
print(text.rfind("l"))    # 3
print(text.find("o", 5))  # 11
```

- `find()`: 왼쪽부터 검색
- `rfind()`: 오른쪽부터 검색

> **find() 와 index() 차이**
>
> 둘 다 위치를 찾지만, `find()` 는 없으면 `-1` 을 반환하고 `index()`는 오류를 발생시킨다.
>
> ```python
> text = "Hello"
> 
> print(text.find("z"))   # -1
> print(text.index("z"))  # ValueError
> ```

#### 4. 문자열 대체

`replace()`는 특정 문자열을 다른 문자열로 바꾼 새 문자열을 반환한다.

```python
text = "Hello, Python!"
new_text = text.replace("Python", "World")

print(new_text)  # Hello, World!
```

문자열은 불변이므로 원본 문자열이 직접 바뀌는 것이 아니라 새로운 문자열이 생성된다.

#### 5. 양쪽 공백 제거

`strip()`은 문자열 양쪽의 공백을 제거한다.

```python
text = "   Hello, Python!   "

print(text)
print(text.strip())		# 공백 제거
print(text.lstrip())  # 왼쪽 공백 제거
print(text.rstrip())  # 오른쪽 공백 제거
```

#### 6. 문자열 분리

`split()`은 문자열을 특정 기준으로 나누어 리스트로 반환한다.

```python
text = "김사과 반하나 오렌지 이메론"
names = text.split()

print(names)	# ['김사과', '반하나', '오렌지', '이메론']
```

```python
text = "김사과,반하나,오렌지,이메론"
names = text.split(",")

print(names)	# ['김사과', '반하나', '오렌지', '이메론']
```

#### 7. 문자열 결합

`join()`은 여러 문자열을 하나의 문자열로 결합한다.

```python
city = "서울시"
district ="영등포구"
street = "버드나루로"

address = " ".join((city, district, street))

print("주소:", address)	# 주소: 서울시 영등포구 버드나루로
```

#### 8. 접두사와 접미사 확인

`startswith()`는 문자열이 특정 값으로 시작하는지 확인하고, `endswith()`는 특정 값으로 끝나는지 확인한다.

```python
text = "Hello, Python!"

starts_with_hello = text.startswith("Hello")
ends_with_world = text.endswith("World!")

print(starts_with_hello)  # True
print(ends_with_world)    # False
```

> ### 함수(Function) 와 메서드(Method) 의 차이
>
> ### 함수와 메서드의 차이
>
> 함수와 메서드는 모두 특정 작업을 수행하는 코드 묶음이다.  
> 차이는 함수가 어디에 소속되어 있는지이다.
>
> - **함수(Function)**  
>   독립적으로 호출할 수 있는 코드이다.
>
>   ```python
>   text = "Hello"
>   print(len(text))
>   ```
>
>   `len()`은 특정 객체에 소속되지 않고 독립적으로 사용할 수 있는 함수이다.
>
> - **메서드(Method)**
>   특정 객체에 소속된 함수이다.
>   보통 `객체.메서드()` 형태로 사용한다.
>
>   ```python
>   text = "Hello"
>   print(text.upper())
>   ```
>
>   `upper()` 는 문자열 객체가 가지고 있는 메서드이다.
>
>
> 간단히 말하면 : 
>
> ```text
> 함수: 함수이름()
> 메서드: 객체.메서드이름()
> ```



### 출처 및 참고 자료

본 정리는 강의 내용과 아래 자료를 참고하여 학습 목적으로 작성하였습니다.

https://ryuzyproject.tistory.com/278
https://ryuzyproject.tistory.com/279



