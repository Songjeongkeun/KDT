# [9일차] Python, 데이터분석

## 모듈, 패키지, 가상환경 그리고 NumPy 기초 정리

이번 글에서는 파이썬 코드를 파일 단위로 재사용하는 **모듈(module)**, 여러 모듈을 폴더 단위로 묶는 **패키지(package)**, 외부 라이브러리를 관리하는 **가상환경과 requirements.txt**, 그리고 데이터 분석의 핵심 라이브러리인 **NumPy**를 정리한다.

-----------

파이썬을 어느 정도 익히고 나면 코드가 점점 길어진다. 이때 모듈과 패키지를 사용하면 코드를 기능별로 나눌 수 있고, NumPy를 사용하면 대량의 수치 데이터를 빠르고 편리하게 처리할 수 있다.

## 1. 모듈

모듈(module)은 관련된 함수, 클래스, 변수들을 하나의 `.py` 파일로 묶어 재사용할 수 있게 만든 코드 단위이다.

모듈을 사용하면 다음과 같은 장점이 있다.

- 기능별로 코드를 나눌 수 있다.
- 같은 코드를 여러 파일에서 재사용할 수 있다.
- 파일이 짧아져 가독성과 유지보수성이 좋아진다.
- 이름 공간(namespace)이 분리되어 이름 충돌을 줄일 수 있다.

### 1.1 모듈 파일 만들기

예를 들어 과일과 관련된 기능을 `fruit.py`라는 파일로 분리할 수 있다.

```python
# fruit.py

PI = 3.14


def print_fruit(name):
    print(f"{name}입니다.")


def add_quantity(quantity, amount):
    return quantity + amount


class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def print_info(self):
        print(f"과일 이름: {self.name}")
        print(f"수량: {self.quantity}")
```

`fruit.py` 안에는 변수, 함수, 클래스가 함께 들어 있다. 이 파일 자체가 하나의 모듈이다.

### 1.2 다른 파일에서 모듈 전체 가져오기

같은 폴더에 있는 `main.py`에서 `fruit.py`를 사용할 수 있다.

```python
# main.py

import fruit

fruit.print_fruit("사과")

result = fruit.add_quantity(10, 5)
print(result)

apple = fruit.Fruit("사과", 10)
apple.print_info()
```

출력 결과:

```text
사과입니다.
15
과일 이름: 사과
수량: 10
```

`import fruit`로 모듈 전체를 가져오면 `fruit.print_fruit()`처럼 `모듈명.이름` 형태로 접근한다.

### 1.3 필요한 이름만 가져오기

모듈 전체가 아니라 필요한 함수나 클래스만 가져올 수도 있다.

```python
from fruit import Fruit, add_quantity

apple = Fruit("사과", 10)
apple.print_info()

print(add_quantity(10, 5))
```

출력 결과:

```text
과일 이름: 사과
수량: 10
15
```

이 방식은 코드가 짧아지는 장점이 있지만, 어떤 모듈에서 가져온 이름인지 덜 명확할 수 있다.

### 1.4 별칭 사용하기

모듈 이름이 길거나 자주 사용할 때는 `as`로 별칭을 붙일 수 있다.

```python
import fruit as fr

fr.print_fruit("바나나")
```

출력 결과:

```text
바나나입니다.
```

NumPy를 사용할 때 `import numpy as np`라고 쓰는 것도 같은 방식이다.

### 1.5 import 방식 비교

| 방식 | 예시 | 특징 |
| --- | --- | --- |
| 모듈 전체 가져오기 | `import fruit` | 이름 출처가 명확하다. |
| 일부만 가져오기 | `from fruit import Fruit` | 코드가 짧지만 이름 충돌에 주의해야 한다. |
| 별칭 사용 | `import fruit as fr` | 긴 이름을 짧게 줄일 수 있다. |

---

## 2. `__name__`과 직접 실행 여부

`__name__`은 현재 실행 중인 모듈의 이름을 담고 있는 내장 변수이다.

- 파일을 직접 실행하면 `__name__`은 `"__main__"`이 된다.
- 다른 파일에서 import되면 `__name__`은 모듈 이름이 된다.

### 2.1 직접 실행되는 코드와 import되는 코드 구분하기

```python
# fruit.py

def hello():
    print("과일 모듈입니다.")


print("__name__ 값:", __name__)

if __name__ == "__main__":
    print("직접 실행되었습니다.")
    hello()
```

터미널에서 직접 실행하면 다음과 같다.

```bash
python fruit.py
```

출력 결과:

```text
__name__ 값: __main__
직접 실행되었습니다.
과일 모듈입니다.
```

다른 파일에서 import하면 `if __name__ == "__main__":` 블록은 실행되지 않는다.

```python
# main.py

import fruit
```

출력 결과:

```text
__name__ 값: fruit
```

`if __name__ == "__main__":`는 테스트 코드나 직접 실행용 코드를 분리할 때 자주 사용한다.

---

## 3. 패키지

패키지(package)는 관련된 여러 모듈을 하나의 폴더로 묶어 계층적으로 관리하는 단위이다.

프로젝트가 커지면 하나의 파일에 모든 코드를 작성하기 어렵다. 이때 기능별로 모듈을 나누고, 관련 모듈들을 패키지로 묶으면 구조가 깔끔해진다.

### 3.1 패키지 구조

```text
myproject/
├── main.py
└── fruits/
    ├── __init__.py
    ├── apple.py
    └── banana.py
```

`fruits` 폴더가 패키지이고, 그 안의 `apple.py`, `banana.py`가 모듈이다.

### 3.2 `__init__.py`

`__init__.py`는 패키지가 import될 때 실행되는 파일이다. 패키지의 공개 API를 정리할 때 사용할 수 있다.

```python
# fruits/__init__.py

from .apple import info as apple_info
from .banana import info as banana_info

__all__ = ["apple_info", "banana_info"]
```

`.`은 현재 패키지를 의미한다. 즉, `.apple`은 같은 `fruits` 패키지 안의 `apple.py`를 뜻한다.

```python
# fruits/apple.py

def info():
    return "사과입니다."
# fruits/banana.py

def info():
    return "바나나입니다."
# main.py

from fruits import apple_info, banana_info

print(apple_info())
print(banana_info())
```

출력 결과:

```text
사과입니다.
바나나입니다.
```

패키지를 사용하면 `fruits.apple`, `fruits.banana`처럼 이름 공간을 나눌 수 있어 모듈 이름 충돌을 줄일 수 있다.

---

## 4. `random` 모듈

`random` 모듈은 무작위 값을 생성할 때 사용하는 파이썬 표준 라이브러리이다. 별도 설치 없이 사용할 수 있다.

```python
import random
```

### 4.1 자주 사용하는 함수

아래 예제는 실행할 때마다 결과가 달라질 수 있다.

```python
import random

print("random():", random.random())
print("randint(1, 6):", random.randint(1, 6))
print("randrange(1, 10):", random.randrange(1, 10))

fruits = ["사과", "바나나", "오렌지"]
print("choice:", random.choice(fruits))

numbers = list(range(1, 11))
print("sample:", random.sample(numbers, 3))

cards = ["A", "K", "Q", "J"]
random.shuffle(cards)
print("shuffle:", cards)
```

출력 결과 예시:

```text
random(): 0.731...
randint(1, 6): 4
randrange(1, 10): 8
choice: 바나나
sample: [2, 9, 5]
shuffle: ['Q', 'A', 'J', 'K']
```

| 함수 | 설명 |
| --- | --- |
| `random.random()` | `0` 이상 `1` 미만의 실수 반환 |
| `random.randint(a, b)` | `a` 이상 `b` 이하의 정수 반환 |
| `random.randrange(a, b)` | `a` 이상 `b` 미만의 정수 반환 |
| `random.choice(seq)` | 시퀀스에서 값 하나 선택 |
| `random.sample(seq, k)` | 중복 없이 `k`개 선택 |
| `random.shuffle(list)` | 리스트 자체를 섞음 |

### 4.2 `seed()`

`random.seed()`는 난수 생성기의 초기값을 설정한다. 같은 시드를 사용하면 같은 순서의 난수가 생성된다.

```python
import random

random.seed(2026)

print(random.randint(1, 10))
print(random.randint(1, 10))
print(random.randint(1, 10))
```

출력 결과:

```text
2
6
9
```

난수 결과를 재현해야 하는 테스트, 디버깅, 머신러닝 실험에서 `seed()`가 중요하다.

### 4.3 의사난수

의사난수(pseudo-random number)는 완전히 무작위로 만들어진 값이 아니라 알고리즘에 의해 만들어진 “랜덤처럼 보이는 숫자”이다.

같은 시작값인 시드(seed)를 주면 같은 난수 순서가 만들어진다. 이 특성 덕분에 실험 결과를 재현할 수 있다.

> 보안이 중요한 난수에는 `random`보다 `secrets` 모듈을 사용하는 것이 적합하다. 예를 들어 인증 토큰이나 비밀번호 재설정 토큰을 만들 때는 `secrets`를 사용한다.

---

## 5. 가상환경과 모듈 설치

외부 라이브러리를 설치할 때는 프로젝트별로 독립된 가상환경을 사용하는 것이 좋다.

가상환경을 사용하면 프로젝트마다 서로 다른 패키지 버전을 사용할 수 있고, 전역 Python 환경이 지저분해지는 것을 막을 수 있다.

### 5.1 가상환경 생성

```bash
python -m venv venv
```

### 5.2 가상환경 활성화

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 5.3 pip와 python 경로 확인

Windows:

```bash
where pip
where python
```

macOS/Linux:

```bash
which pip
which python
```

경로가 현재 프로젝트의 `venv` 안을 가리키는지 확인해야 한다.

### 5.4 패키지 설치

```bash
pip install numpy pandas
```

더 안전하게는 현재 실행 중인 Python의 pip를 사용하도록 다음 명령을 쓸 수 있다.

```bash
python -m pip install numpy pandas
```

`pip`이 다른 Python을 가리킬 수 있으므로, 실무에서는 `python -m pip install ...` 형태를 자주 사용한다.

### 5.5 패키지 목록 확인

```bash
pip list
```

현재 환경에 설치된 패키지 이름과 버전을 확인할 수 있다.

---

## 6. `requirements.txt`

`requirements.txt`는 프로젝트에 필요한 외부 패키지와 버전을 기록하는 파일이다. 이 파일이 있으면 다른 사람도 같은 환경을 쉽게 재현할 수 있다.

### 6.1 requirements.txt 생성

```bash
pip freeze > requirements.txt
```

생성된 파일 예시는 다음과 같다.

```text
numpy==2.4.6
pandas==2.3.3
```

직접 작성할 수도 있다.

```text
numpy
pandas
```

버전을 고정하지 않으면 설치 시점의 최신 버전이 설치될 수 있다.

### 6.2 requirements.txt로 설치

```bash
pip install -r requirements.txt
```

다른 환경에서 이 명령을 실행하면 `requirements.txt`에 적힌 패키지가 자동으로 설치된다.

---

## 7. NumPy란?

NumPy는 Python에서 수치 계산과 데이터 분석을 효율적으로 수행하기 위해 사용하는 대표적인 라이브러리이다.

NumPy의 핵심은 `ndarray`라는 다차원 배열 객체이다.

NumPy가 자주 사용되는 이유는 다음과 같다.

- 일반 Python 리스트보다 대량 연산이 빠르다.
- 다차원 배열을 쉽게 다룰 수 있다.
- 반복문 없이 배열 전체에 연산을 적용할 수 있다.
- 행렬 연산, 통계, 선형대수, 난수 생성 기능을 제공한다.
- pandas, scikit-learn, TensorFlow 등 많은 데이터 분석 라이브러리의 기반이 된다.

### 7.1 설치와 import

```bash
pip install numpy
```

또는 다음처럼 설치할 수 있다.

```bash
python -m pip install numpy
```

NumPy는 관례적으로 `np`라는 별칭으로 import한다.

```python
import numpy as np
```

---

## 8. ndarray

`ndarray`는 N-dimensional array의 줄임말로, NumPy의 핵심 자료구조이다. 같은 자료형의 데이터를 다차원 형태로 저장하고 빠르게 연산할 수 있다.

### 8.1 1차원 배열과 2차원 배열

```python
import numpy as np

ndarr1 = np.array([1, 2, 3, 4])
print(ndarr1)
print(type(ndarr1))
print(type(ndarr1[0]))

ndarr2 = np.array([[1, 2, 3], [4, 5, 6]])
print(ndarr2)
print(type(ndarr2))
print(type(ndarr2[0]))
```

출력 결과:

```text
[1 2 3 4]
<class 'numpy.ndarray'>
<class 'numpy.int64'>
[[1 2 3]
 [4 5 6]]
<class 'numpy.ndarray'>
<class 'numpy.ndarray'>
```

### 8.2 리스트와 ndarray 변환

```python
import numpy as np

list1 = [1, 2, 3, 4]
ndarr1 = np.array(list1)
print(ndarr1)
print(type(ndarr1))

list2 = ndarr1.tolist()
print(list2)
print(type(list2))
```

출력 결과:

```text
[1 2 3 4]
<class 'numpy.ndarray'>
[1, 2, 3, 4]
<class 'list'>
```

### 8.3 ndarray의 자료형 통일

Python 리스트는 서로 다른 타입을 함께 담을 수 있다.

```python
list1 = [1, 3.14, "Python", True]

print(list1)
print(type(list1[0]))
print(type(list1[1]))
print(type(list1[2]))
print(type(list1[3]))
```

출력 결과:

```text
[1, 3.14, 'Python', True]
<class 'int'>
<class 'float'>
<class 'str'>
<class 'bool'>
```

반면 NumPy 배열은 하나의 `dtype`으로 통일된다.

```python
import numpy as np

ndarr1 = np.array([1, 2, 3.14, True])

print(ndarr1)
print(ndarr1.dtype)
print(type(ndarr1[0]))
```

출력 결과:

```text
[1.   2.   3.14 1.  ]
float64
<class 'numpy.float64'>
```

정수, 실수, 불리언이 섞여 있지만 NumPy는 더 넓은 표현이 가능한 `float64`로 통일한다.

문자열이 섞이면 전체가 문자열 타입으로 변환될 수 있다.

```python
import numpy as np

ndarr2 = np.array(["1", 2, 3.14, True])

print(ndarr2)
print(ndarr2.dtype)
print(type(ndarr2[0]))
```

출력 결과:

```text
['1' '2' '3.14' 'True']
<U32
<class 'numpy.str_'>
```

### 8.4 dtype 직접 지정하기

```python
import numpy as np

ndarr = np.array([1, 2, 3.14, True], dtype=int)

print(ndarr)
print(ndarr.dtype)
```

출력 결과:

```text
[1 2 3 1]
int64
```

`dtype=int`를 지정하면 가능한 값들이 정수로 변환된다. `3.14`는 `3`, `True`는 `1`로 변환된다.

### 8.5 shape, ndim, dtype

NumPy 배열을 다룰 때는 배열의 구조를 확인하는 속성이 중요하다.

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("shape:", arr.shape)
print("ndim:", arr.ndim)
print("dtype:", arr.dtype)
print("size:", arr.size)
```

출력 결과:

```text
shape: (2, 3)
ndim: 2
dtype: int64
size: 6
```

| 속성 | 의미 |
| --- | --- |
| `shape` | 배열의 형태 |
| `ndim` | 배열의 차원 수 |
| `dtype` | 배열 원소의 자료형 |
| `size` | 전체 원소 개수 |

---

## 9. 인덱싱과 슬라이싱

NumPy 배열은 리스트처럼 인덱싱과 슬라이싱을 지원한다. 다차원 배열에서는 `arr[행, 열]` 형태로 접근할 수 있다.

### 9.1 1차원 배열 인덱싱과 슬라이싱

```python
import numpy as np

fruits = np.array(["딸기", "수박", "바나나", "체리", "복숭아"])

print(fruits)
print(fruits.shape)

print(fruits[0])
print(fruits[4])
print(fruits[-1])
print(fruits[-2])

print(fruits[0:3])
print(fruits[2:])
print(fruits[:3])
```

출력 결과:

```text
['딸기' '수박' '바나나' '체리' '복숭아']
(5,)
딸기
복숭아
복숭아
체리
['딸기' '수박' '바나나']
['바나나' '체리' '복숭아']
['딸기' '수박' '바나나']
```

### 9.2 2차원 배열 인덱싱

```python
import numpy as np

arr = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
])

print(arr)
print(arr.shape)

print(arr[0, :])
print(arr[0])
print(arr[:, 0])
print(arr[1, 2])
```

출력 결과:

```text
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]]
(3, 4)
[1 2 3 4]
[1 2 3 4]
[1 5 9]
7
```

### 9.3 Fancy Indexing

Fancy indexing은 인덱스 목록을 이용해 원하는 위치의 값들을 한 번에 가져오는 방식이다.

```python
import numpy as np

arr = np.array([10, 15, 2, 8, 20, 90, 85, 44, 23, 32])
idx = [2, 5, 9]

print(arr[idx])

arr2d = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
])

print(arr2d[[0, 1], :])
```

출력 결과:

```text
[ 2 90 32]
[[1 2 3 4]
 [5 6 7 8]]
```

### 9.4 Boolean Indexing

Boolean indexing은 조건에 맞는 값만 선택하는 방식이다.

```python
import numpy as np

arr = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
])

print(arr > 7)
print(arr[arr > 7])
```

출력 결과:

```text
[[False False False False]
 [False False False  True]
 [ True  True  True  True]]
[ 8  9 10 11 12]
```

Boolean indexing은 조건 필터링에 매우 자주 사용된다.

---

## 10. 행렬 연산

NumPy는 다차원 배열을 이용해 행렬 연산을 수행할 수 있다. 행렬 연산은 데이터 과학, 머신러닝, 통계, 컴퓨터 그래픽스 등에서 중요하게 사용된다.

### 10.1 스칼라, 벡터, 행렬

| 개념 | 의미 | 예시 |
| --- | --- | --- |
| 스칼라 | 숫자 하나 | `3`, `3.14` |
| 벡터 | 숫자가 1차원으로 나열된 구조 | `[1, 2, 3]` |
| 행렬 | 숫자가 행과 열을 가진 2차원 표 형태로 저장된 구조 | `[[1, 2], [3, 4]]` |

### 10.2 원소별 연산

크기가 같은 배열끼리는 같은 위치의 원소끼리 연산된다.

```python
import numpy as np

a = np.array([[1, 2, 3],
              [2, 3, 4]])
b = np.array([[3, 4, 5],
              [1, 2, 3]])

print(a.shape, b.shape)
print(a + b)
print(a - b)
print(a * b)
print(a / b)
```

출력 결과:

```text
(2, 3) (2, 3)
[[4 6 8]
 [3 5 7]]
[[-2 -2 -2]
 [ 1  1  1]]
[[ 3  8 15]
 [ 2  6 12]]
[[0.33333333 0.5        0.6       ]
 [2.         1.5        1.33333333]]
```

`a * b`는 행렬 곱셈이 아니라 같은 위치의 원소끼리 곱하는 연산이다.

### 10.3 행렬 곱셈

행렬 곱셈은 앞 행렬의 열 개수와 뒤 행렬의 행 개수가 같아야 가능하다.

```python
import numpy as np

a = np.array([
    [1, 2, 3],
    [1, 2, 3],
    [2, 3, 4],
])

b = np.array([
    [1, 2],
    [3, 4],
    [5, 6],
])

print(a.shape)
print(b.shape)

print(a @ b)
print(np.dot(a, b))
```

출력 결과:

```text
(3, 3)
(3, 2)
[[22 28]
 [22 28]
 [31 40]]
[[22 28]
 [22 28]
 [31 40]]
```

`@`와 `np.dot()`은 위 예제에서 행렬 곱셈을 수행한다.

### 10.4 벡터 내적

내적은 두 벡터를 곱해 하나의 숫자인 스칼라를 만드는 연산이다.

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.dot(a, b))
```

출력 결과:

```text
32
```

계산 과정은 `1*4 + 2*5 + 3*6 = 32`이다.

### 10.5 브로드캐스팅

브로드캐스팅(broadcasting)은 모양이 다른 배열끼리도 규칙에 맞으면 자동으로 형태를 맞춰 연산하는 기능이다.

```python
import numpy as np

scores = np.array([70, 80, 90])

print(scores + 10)
```

출력 결과:

```text
[ 80  90 100]
```

스칼라 `10`이 배열의 모든 원소에 더해진다. 반복문 없이 배열 전체에 연산을 적용할 수 있는 것이 NumPy의 큰 장점이다.

---

## 11. 정렬

NumPy의 `np.sort()`는 배열을 정렬한 복사본을 반환한다. 원본 배열은 기본적으로 변경되지 않는다.

### 11.1 1차원 배열 정렬

```python
import numpy as np

arr = np.array([1, 10, 5, 7, 2, 4, 3, 6, 8, 9])

print(arr)
print(np.sort(arr))
print(arr)
print(np.sort(arr)[::-1])
```

출력 결과:

```text
[ 1 10  5  7  2  4  3  6  8  9]
[ 1  2  3  4  5  6  7  8  9 10]
[ 1 10  5  7  2  4  3  6  8  9]
[10  9  8  7  6  5  4  3  2  1]
```

### 11.2 2차원 배열 정렬

```python
import numpy as np

arr = np.array([
    [11, 10, 12, 9],
    [3, 1, 4, 2],
    [5, 6, 7, 8],
])

print(np.sort(arr, axis=0))
print(np.sort(arr, axis=1))
print(np.sort(arr, axis=1)[:, ::-1])
```

출력 결과:

```text
[[ 3  1  4  2]
 [ 5  6  7  8]
 [11 10 12  9]]
[[ 9 10 11 12]
 [ 1  2  3  4]
 [ 5  6  7  8]]
[[12 11 10  9]
 [ 4  3  2  1]
 [ 8  7  6  5]]
```

`axis=0`은 열 방향, `axis=1`은 행 방향으로 정렬한다.

### 11.3 3차원 배열 정렬

```python
import numpy as np

arr = np.array([
    [
        [9, 3, 5],
        [8, 1, 7],
    ],
    [
        [4, 6, 2],
        [10, 0, 11],
    ],
])

print(arr.shape)

result = np.sort(arr, axis=-1)
print(result)
```

출력 결과:

```text
(2, 2, 3)
[[[ 3  5  9]
  [ 1  7  8]]

 [[ 2  4  6]
  [ 0 10 11]]]
```

`axis=-1`은 마지막 축을 기준으로 정렬한다.

---

## 12. 자주 쓰는 NumPy 기능

원문 내용에 추가로, NumPy를 사용할 때 자주 만나는 기능 몇 가지를 정리한다.

### 12.1 배열 생성 함수

```python
import numpy as np

print(np.zeros((2, 3)))
print(np.ones((2, 3)))
print(np.arange(1, 10, 2))
print(np.linspace(0, 1, 5))
```

출력 결과:

```text
[[0. 0. 0.]
 [0. 0. 0.]]
[[1. 1. 1.]
 [1. 1. 1.]]
[1 3 5 7 9]
[0.   0.25 0.5  0.75 1.  ]
```

| 함수 | 설명 |
| --- | --- |
| `np.zeros(shape)` | 0으로 채운 배열 생성 |
| `np.ones(shape)` | 1로 채운 배열 생성 |
| `np.arange(start, stop, step)` | 범위 기반 배열 생성 |
| `np.linspace(start, stop, count)` | 구간을 균등하게 나눈 배열 생성 |

### 12.2 reshape

`reshape()`는 배열의 전체 원소 개수를 유지하면서 모양을 바꾼다.

```python
import numpy as np

arr = np.arange(1, 7)
reshaped = arr.reshape(2, 3)

print(arr)
print(reshaped)
```

출력 결과:

```text
[1 2 3 4 5 6]
[[1 2 3]
 [4 5 6]]
```

### 12.3 통계 함수

```python
import numpy as np

scores = np.array([70, 80, 90, 100])

print("합계:", np.sum(scores))
print("평균:", np.mean(scores))
print("최댓값:", np.max(scores))
print("최솟값:", np.min(scores))
```

출력 결과:

```text
합계: 340
평균: 85.0
최댓값: 100
최솟값: 70
```

---

## 13. 마무리

이번 글에서는 파이썬의 코드 재사용과 데이터 분석 기초를 함께 정리했다.

| 주제 | 핵심 |
| --- | --- |
| 모듈 | `.py` 파일 단위로 코드 재사용 |
| 패키지 | 여러 모듈을 폴더 단위로 묶어 관리 |
| `__name__` | 직접 실행과 import 실행 구분 |
| 가상환경 | 프로젝트별 패키지 환경 분리 |
| `requirements.txt` | 패키지 설치 환경 재현 |
| NumPy | 빠른 수치 계산을 위한 배열 라이브러리 |
| ndarray | NumPy의 핵심 다차원 배열 객체 |
| 인덱싱/슬라이싱 | 배열에서 원하는 위치나 조건의 데이터 선택 |
| 행렬 연산 | 벡터, 행렬 기반 계산 수행 |
| 정렬 | 축(axis)을 기준으로 배열 정렬 |

모듈과 패키지는 프로젝트 구조를 정리하는 도구이고, 가상환경과 `requirements.txt`는 실행 환경을 안정적으로 관리하는 도구이다. NumPy는 대량의 수치 데이터를 빠르게 처리하기 위한 기본 라이브러리이므로 데이터 분석을 공부한다면 반드시 익숙해져야 한다.

