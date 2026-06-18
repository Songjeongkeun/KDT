# [7일차] Python

## 사용자 정의 함수와 객체지향 프로그래밍 정리

파이썬에서 함수와 클래스는 코드를 구조화하는 핵심 도구이다.

함수는 중복되는 작업을 묶고, 클래스는 데이터와 동작을 하나의 객체로 표현할 수 있게 해준다.

이번 글에서는 변수의 범위, 클로저, 콜백함수, 람다 함수, 프로그래밍 방법론, 클래스와 객체지향 개념을 예제와 함께 정리한다.



## 사용자 정의 함수

## 1. 변수의 범위

변수의 범위 (scope) 는 변수를 참조하거나 변경할 수 있는 영역을 의미한다.

파이썬은 이름을 찾을 때 **LEGB 규칙** 을 따른다.

| 순서 | 범위      | 의미                                 |
| :--- | :-------- | :----------------------------------- |
| L    | Local     | 현재 함수 내부 범위                  |
| E    | Enclosing | 내부 함수를 감싸는 외부 함수의 범위  |
| G    | Global    | 모듈 전체 범위                       |
| B    | Built-in  | 파이썬이 기본으로 제공하는 내장 범위 |

파이썬은 변수를 사용할 때 `Local ➡ Enclosing ➡ Global ➡ Built-in`순서로 이름을 찾는다.

### 1.1 지역 변수

지역 변수(local variable) 는 함수 내부에서 정의된 변수이다. 함수가 실행되는 동안에만 사용할 수 있으며, 함수 밖에서는 접근할 수 없다.

```python
def local_example():
  local_var = "로컬 변수"
  print(local_var)
  
local_example()

# print(local_var) # NameError: name 'local_var' is not defined
```

출력 결과 :

```python
로컬 변수
```

`local_var` 는 `local_example()` 함수 안에서 만들어졌기 때문에 함수 내부에서만 사용할 수 있다.



### 1.2 전역 변수

전역 변수(global variable) 는 함수 밖, 즉 모듈 전체 범위에 정의된 변수이다. 함수 내부에서도 읽을 수 있다.

```python
global_var = "전역 변수"

def test_global_scope():
  print(global_var)
  
test_global_scope()
```

출력 결과 :

```python
전역 변수
```

다만 함수 내부에서 전역 변수의 값을 변경하려면 `global` 키워드가 필요하다.

```python
global_var = 10

def modify_global():
  global global_var
  global_var = 20
  
modify_global()
print(global_var)
```

출력 결과 :

```tex
20
```

`global` 을 사용하면 함수 내부에서 전역 변수 자체를 수정할 수 있다. 하지만 전역 변수 변경은 코드 흐름을 추적하기 어렵게 만들 수 있으므로 꼭 필요한 경우에만 사용하는 편이 좋다.



### 1.3 둘러싼 범위와 클로저

함수 안에 또 다른 함수를 정의하면, 내부 함수는 외부 함수의 지역 변수를 참조할 수 있다. 이때 외부 함수의 범위를 **둘러싼 범위(enclosing scope)** 라고 한다.

```python
def outer_function():
  enclosing_var = "둘러싼 범위 변수"
  
  def inner_function():
    print(enclosing_var)
    
  return inner_function

f = outer_function()
f()
```

출력 결괴 :

```tex
둘러싼 범위 변수
```

`outer_function()` 의 실행이 끝났는데도 `inner_function()` 은 `enclosing_var`를 사용할 수 있다. 내부 함수가 외부 함수의 변수를 계속 참조하기 때문에 파이썬이 해당 값을 콜로져 공간에 보관하기 때문이다.



### 1.4 클로저 공간

클로저(closure)는 내부 함수가 외부 함수의 변수를 기억하는 구조이다. 일반적으로 함수가 종료되면 그 안의 지역 변수는 사라진다. 하지만 내부 함수가 외부 함수의 변수를 참조하고 있다면 파이썬은 그 값을 바로 제거하지 않고 함수 객체 안에 보관한다.

```python
def make_counter():
  count = 0
 	
  def counter():
    return count + 1
  
  return counter

counter_func = make_counter()
print(counter_func()) # 1
```

출력 결과 :

```tex
1
```

예제 :

```python
def outer_function(msg):
  message = "hello, " + msg
   
  def inner_function():
  	print(message)
  
  return inner_function

func = outer_function("Python") # 클로저 생성

print(func()) # "hello, Python" 출력
```

출력 결과 :

```tex
hello Python
```

출력 과정 :

1. `outer_function` 함수에 `"Python"` 를 매개변수 값으로 넘겨주며 실행한다.
2. `message` 변수에 매개변수를 이용해 `"hello Python"` 라는 문자열을 저장한다.
3. `inner_fuction` 함수가 `message`변수를 참조
4.  `inner_function` 함수 리턴
5. `func` 변수가 `inner_function` 함수를 참조
6. `func` 변수 실행(`inner_function` 함수 실행)
7. `func`변수는 `message`변수를 출력

➡ 4번 단계에서 `outer_function` 함수는 역할을 마치고 종료되었다. 함수가 종료되면 원래 메모리에서 삭제되어야 한다. 하지만 삭제되지 않고 메모리에 남은 이유가 `closure` 공간 때문이다.

`closure`  가 성립하려면 3가지 조건이 필요하다.

1. 함수 안에 함수가 있어야한다. (중첩 함수)
2. 내부 함수가 외부 함수의 변수를 참조해야 한다.
3. 외부 함수가 내부 함수를 반환해야 한다.

클로저에 저장된 값은 함수 객체의 `__closure__` 속성에서 확인할 수 있다.

```python
print(func.__closure__)
print(type(func.__closure))
```

출력 결과 :

```tex
(<cell at 0x108434f10: str object at 0x10849d2b0>,)
<class 'tuple'>
```

```python
print(dir(func.__closure__[0]))
```

출력 결과 : 

```tex
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'cell_contents']
```

마지막에 `cell_contents` 값이 있는데 이 부분을 출력해보자.

```python
print(func.__closure__[0].cell_contents)
```

출력 결과 :

```tex
hello, Python
```

`message` 가 여기에 저장된다. 즉 클로저가 저장되는 경로는 `__closure__[0].cell_contents` 정도로 생각할 수 있다.

> `__closure__` 튜플은 모든 함수 객체가 가지고 있다. 다만 조건을 만족하지 않아 클로저가 생성되지 않으면, 그 값이 None 으로 고정된다.

**클로저의 장점**

1. 함수가 상태를 기억할 수 있다.
2. 전역 변수 없이 데이터 유지가 가능하다.
3. 데이터 은닉이 가능하다.
4. 함수별 독립 상태 생성이 가능하다.
5. 데코레이터 구현이 가능하다.

클로저에서 외부 함수의 변수를 수정해야 한다면 `nonlocal` 키워드를  사용한다.

```python
def make_counter():
  count = 0
  
  def counter():
    nonlocal count
    count += 1
    return count
 	
  return count

counter_func = make_counter()

print(counter_fun()) # 1
print(counter_fun()) # 2
print(counter_fun()) # 3
```

> `global` 은 전역 변수를 수정할 때 사용하고, `nonlocal` 은 바깥 함수의 지역 변수를 수정할 때 사용한다.

### 1.5 빌트인(Built-in) 범위

빌트인(built-int) 범위에는 파이썬이 기본으로 제공하는 이름들이 들어 있다. `print()` , `len()`, `type()` , `range()` 같은 함수가 여기에 해당한다.

```python
print(len([1, 2, 3])) # 3
print(type("Python")) # <class 'str'> 
```

내장 함수와 같은 이름으로 변수를 만들면 내장 함수가 가려질 수 있다.

```python
len = 5

# print(len([1, 2, 3])) # TypeError: 'int' object is not callable
```

위 코드에서 `len` 은 더 이상 내장 함수가 아니라 정수 `5` 를 가리키는 변수로 인식된다. 따라서 `len()` 처럼 호출 할 수 있다.

> 내장 함수 이름인 `len`, `list`, `dict`, `sum` `type` 등을 변수명으로 사용하는 것은 피하는 것이 좋다.



## 2. 함수 객체와 메모리

파이썬에서 함수도 객체이다. 즉, 함수는 변수에 저장할 수 있고, 다른 함수에 전달할 수 있으며, 필요 없어지면 가비지 컬렉션 대상이 될 수 있다. 

### 2.1 함수도 변수에 담을 수 있다.

```python
def greet():
  print("안녕하세요.")
  
hello = greet

greet()
hello()
```

출력 결과 :

```tex
안녕하세요.
안녕하세요.
```

`hello = greet` 는 함수를 실행하는 코드가 아니다. `greet` 함수 객체에 `hello` 라는 이름을 하나 더 붙이는 코드이다.

### 2.2 del은 이름을 삭제한다.

`del` 은 함수 객체 자체를 즉시 삭제한다기보다, 해당 객체를 가리키는 이름을 제거한다.

```python 
def func1():
  print("처음으로 만드는 함수")
 
func1()

del func1

# func1() # NameError: name 'func1' is not defined
```

출력 결과 :

```tex
처음으로 만드는 함수
```

함수를 가리키는 다른 참조가 남아 있다면 함수 객체는 계속 사용할 수 있다.

```python
def func1():
  	print("함수 객체")

alias = func1
del func1

alias() # 함수 객체
```

출력 결과 :

```tex
함수 객체
```

함수 객체를 참조하는 이름이나 자료구조가 더 이상 없으면 파이썬은 해당 객체를 나중에 메모리에서 정리할 수 있다. 단, 정확히 언제 제거되는지는 구현과 상황에 따라 달라질 수 있다.



## 3. 콜백 함수

콜백 함수(callback function) 는 다른 함수에 인자로 전달되어, 특정 시점에 나중에 호출되는 함수이다. 파이썬에서는 함수도 객체이므로 함수의 인자로 다른 함수로 전달할 수 있다.

### 3.1 기본 콜백 예제

```python
def say_hello(name):
  print(f"{name}님 안녕하세요.")
  
del execute(callback):
  print("작업을 시작한다.")
  callback("김사과")
  print("작업을 종료한다.")
  
execute(say_hello)
```

출력 결과 :

```tex
작업을 시작한다.
김사과님 안녕하세요.
작업을 종료한다.
```

위 코드에서 `say_hello`가 콜백 함수이다. `execute()` 는 직접 인사 문구를 알 필요 없이, 전달받은 함수를 필요한 시점에 호출한다.



### 3.2 공통 흐름은 유지하고 세부 동작만 바꾸기

콜백 함수는 공통 작업은 그대로 두고, 세부 동작만 바꾸고 싶을 때 유용하다.

```python
def print_score(score):
    print(f"점수: {score}")

def print_pass_fail(score):
    if score >= 80:
        print(f"{score}점: 합격")
    else:
        print(f"{score}점: 불합격")

def print_bonus_score(score):
    print(f"보너스 적용 점수: {score + 5}")

def process_scores(scores, callback):
    for score in scores:
        callback(score)

scores = [80, 95, 70, 100, 60]

print("원점수 출력")
process_scores(scores, print_score)

print("합격 여부 출력")
process_scores(scores, print_pass_fail)

print("보너스 점수 출력")
process_scores(scores, print_bonus_score)
```

출력 결과 :

```tex
원점수 출력
점수: 80
점수: 95
점수: 70
점수: 100
점수: 60
합격 여부 출력
80점: 합격
95점: 합격
70점: 불합격
100점: 합격
60점: 불합격
보너스 점수 출력
보너스 적용 점수: 85
보너스 적용 점수: 100
보너스 적용 점수: 75
보너스 적용 점수: 105
보너스 적용 점수: 65
```

`process_scores()` 는 점수 목록을 순회하는 공통 로직만 담당한다. 점수를 어떻게 처리할지는 콜백 함수가 결정한다.

### 3.3 sorted() 의 key 도 콜백이다.

파이썬의 `sorted()` 함수는 `key` 인자로 함수를 받을 수 있다. `sorted()` 는 각 요소를 비교하기 전에 `key` 함수를 호출해 정렬 기준값을 얻는다.

```python
students = [
    {"name": "김사과", "score": 90},
    {"name": "반하나", "score": 75},
    {"name": "오렌지", "score": 100}
]

def get_score(student):
    return student["score"]

result = sorted(students, key=get_score)

print(result)
```

출력 결과 :

```tex
[{'name': '반하나', 'score': 75}, {'name': '김사과', 'score': 90}, {'name': '오렌지', 'score': 100}]
```

이 코드에서는 `get_score()` 가 콜백 함수 역할을 한다.

## 3.4 콜백 함수의 필수조건

1. 객체로서의 전달 : 콜백 함수는 호출될 때 괄호 `()` 를 제외한 함수 이름(객체 자체)을 인자로 넘겨야 한다.
2. 호출 가능(Callable) : 전달받는 메인 함수 내부에서 콜백 함수를 실행할 수 있어야 한다. (일반 함수, 람다 함수, 클래스 메서드 등 모두 가능)
3. 서명(Signature) 일치 : 메인 함수가 콜백 함수를 호출할 때 전달하는 인자(Arguments)의 개수와 형태를 콜백 함수가 정상적으로 받을 수 있어야 한다.



## 4. 람다 함수

람다 함수(lambda function) 는 이름 없이 간단한 함수를 한 줄로 정의하는 익명 함수이다. 보통 짧고 일회성으로 사용할 함수를 만들 때 활용한다.

```tex
lambda 매개변수 : 반활한_표현식
```

### 4.1 일반 함수와 람다 함수 비교

```python
def square(x):
  return x * x

print(square(5)) # 25

square_lambda = lambda x : x * x

print(square_lambda(5)) # 25
```

출력 결과 :

```tex
25
25
```

람다 함수는 표현식 하나만 가질 수 있다. 여러 줄의 복잡한 로직이 필요하다면 `def` 로 일반 함수를 정의하는 편이 좋다.



### 4.2 여러 매개변수 사용하기

```python
multiply = lambda a, b: a * b

print(multiply(3, 4)) # 12
```

출력 결과 :

```tex
12
```



### 4.3 조건부 표현식과 함께 사용하기

```python
pass_fail = lambda score: "합격" if score >= 60 else "불합격"

print(pass_fail(80)) 
print(pass_fail(45)) 
```

```tex
합격
불합격
```



### 4.4 sorted() 에서 람다 사용하기

짧은 정렬 기준 함수는 람다로 표현하면 간결하다.

```python
students = [
    {"name": "김사과", "score": 90},
    {"name": "반하나", "score": 75},
    {"name": "오렌지", "score": 100},
]

result = sorted(students, key=lambda student: student["score"], reverse=True)

print(result)
```

출력 결과 :

```tex
[{'name': '오렌지', 'score': 100}, {'name': '김사과', 'score': 90}, {'name': '반하나', 'score': 75}]
```



### 4.5 map() 과 filter()

`map()` 은 반복 가능한 객체의 각 요소에 같은 작업을 적용할 때 사용한다.

```python
scores = [70, 80, 90]

result = list(map(lambda score: score + 10, scores))
print(result)
```

출력 결과 :

```tex
[80, 90, 100]
```



`filter()` 조건을 만족하는 값만 골라낼 때 사용한다.

```python
socres = [45, 70, 88, 52, 100]

passed = list(filter(lambda score: score >= 60, scores))
print(passed)
```

출력 결과 :

```tex
[70, 88, 100]
```

단순한 변환이나 필터링은 리스트 컴프리헨션으로 더 읽기 쉽게 작성할 수도 있다.

```python
scores = [45, 70, 88, 52, 100]

bonus_scores = [score + 10 for score in scores]
passed = [score for score in scores if score >= 60]

print(bonus_scores)
print(passed)
```

출력 결과 :

```
[55, 80, 98, 62, 110]
[70, 88, 100]
```



## 객체지향 프로그래밍

## 1. 프로그래밍 방법론

프로그래밍 방법론은 프로그램을 개발하는 접근 방식이나 사고방식을 의미한다. 프로젝트 규모, 요구 사항, 개발팀의 특성에 따라 적합한 방식이 달라질 수 있다.

| 방법론              | 중심 개념   | 특징                                                         |
| :------------------ | :---------- | :----------------------------------------------------------- |
| 절차적 프로그래밍   | 순서와 절차 | 명령을 순서대로 실행하며 함수를 이용해 작업을 분리한다.      |
| 객체지향 프로그래밍 | 객체        | 데이터와 기능을 객체 단위로 묶어 관리한다.                   |
| 함수형 프로그래밍   | 함수        | 함수를 중심으로 데이터를 변환하고 부수 효과를 줄이는 데 집중한다. |

### 1.1 절차적 프로그래밍

절차적 프로그래밍 (Procedural Programming) 은 작업을 순서대로 실행하도록 프로그램을 구성하는 방식이다. 코드 흐림이 비교적 직관적이며, 작은 츠로그램이나 순서가 중요한 작업에 적합하다.

```python
price = 10000
quantity = 3
discount_rate = 0.1

total = price * quantity
discounted_total = total * (1 - discount_rate)

print(discounted_total)
```

출력 결과 :

```tex
27000.0
```

코드가 길어질수록 중복을 줄이기 위해 함수를 사용한다.

```python
def calculate_total(price, quantity, discount_rate):
  	total = price * quantity
    return total * (1 - discount_rate)
  
print(calculate_total(10000, 3, 0.1))
```

출력 결과 :

```tex
27000.0
```

### 1.2 객체지향 프로그래밍

객체지향 프로그래밍(Object-Oriented Programming, OOP)은 데이터와 기능을 하나의 객체로 묶어 프로그램을 구성하는 방식이다.

```python
class Order:
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity


order = Order(10000, 3)
print(order.total_price())
```

출력 결과 :

```tex
30000
```

객체지향 프로그래밍은 캡슐화, 상속, 다형성 같은 개념을 활용해 코드를 재사용하고 확장하기 좋다.



### 1.3 함수형 프로그래밍

함수형 프로그래밍(Functional Programming) 은 함수를 중심으로 데이터를 처리하는 방식이다. 파이썬은 완전한 함수형 언어는 아니지만 `map()`, `filter()`, `sorted()`, 람다 함수, 컴프리헨션 등을 활용해 함수형 스타일을 작성할 수 있다.

```python
scores = [45, 70, 88, 52, 100]

passed = list(filter(lambda score: score >= 60, scores))
print(passed)
```

출력 결과 :

```tex
[70, 88, 100]
```



## 2. 클래스와 객체

클래스(class) 는 객체를 만들기 위한 설계도이다. 객체가 가져야 할 데이터와 동작을 클래스 안에 정의한다.

```tex
class 클래스이름:
    클래스_속성 = 초기값

    def __init__(self, 매개변수):
        self.인스턴스_속성 = 매개변수

    def 메서드(self):
        실행할 코드
```



### 2.1 빈 클래스 만들기

클래스 내부에 아직 작성할 코드가 없다면 `pass`를 사용할 수 있다.

```python
class Fruit:
    pass


apple = Fruit()
banana = Fruit()

print(apple)
print(type(apple))
print(id(apple))

print(banana)
print(type(banana))
print(id(banana))
```

출력 결과 :

```tex
<__main__.Fruit object at ...>
<class '__main__.Fruit'>
...
<__main__.Fruit object at ...>
<class '__main__.Fruit'>
...
```

`apple` 과 `banana` 는 같은 `Fruit` 클래스로 만들었지만 서로 다른 객체이다. 따라서 `id()` 값도 다르다.



### 2.2 객체와 인스턴스

객체(object)는 메모리에 생성된 모든 실체를 의미하는 넓은 개념이다. 파이썬에서는 숫자, 문자열, 리스트, 함수, 클래스 인스턴스가 모두 객체이다.

인스턴스(instance)는 특정 클래스에 의해 생성된 객체를 말할 때 사용하는 관계 중심의 표현이다.

```python
class Fruit:
    pass


apple = Fruit()

print(isinstance(apple, Fruit))  # True
```

출력 결과 :

```tex
True
```

`apple`은 객체이면서 동시에 `Fruit` 클래스의 인스턴스이다.



## 3. 생성자와 인스턴스 변수

생성자(constructor)는 객체가 생성될 때 초기 설정을 담당하는 특별한 메서드이다. 파이썬에서는 `__init__()` 메서드가 생성자 역할을 한다.



### 3.1 `__init__()` 기본 구조

```python
class Fruit:
    def __init__(self):
        print(self, "init 호출")


apple = Fruit()
```

출력 결과 :

```tex
<__main__.Fruit object at ...> init 호출
```

객체를 생성하면 `__init__()` 이 자동으로 호출된다. 이때 `self`는 생성된 인스턴스 자신을 가르킨다.

### 3.2 인스턴스 변수

인스턴스 변수는 각 객체마다 따로 저장되는 변수이다. 보통 `__init()__` 안에서 `self.변수명` 형태로 만든다.

```python
class Fruit:
    def __init__(self):
        self.name = ""
        self.quantity = 0


apple = Fruit()
banana = Fruit()

apple.name = "사과"
apple.quantity = 10

banana.name = "바나나"
banana.quantity = 5

print(apple.name, apple.quantity)    
print(banana.name, banana.quantity)  
```

출력 결과 :

```tex
사과 10
바나나 5
```

`apple` 의 값을 바꿔도 `banana` 의 값은 바뀌지 않는다. 인스턴스 변수는 객체마다 독립적으로 저장되기 때문이다.



### 3.3 생성자 매개변수로 초기화하기

객체를 만들 때 필요한 값을 생성자 매개변수로 전달할 수 있다.

```python
class Fruit:
    def __init__(self, name, quantity, origin="원산지 미상"):
        self.name = name
        self.quantity = quantity
        self.origin = origin


apple = Fruit("사과", 10, "한국")
banana = Fruit("바나나", 5, "필리핀")
melon = Fruit("멜론", 3)

print(apple.name, apple.quantity, apple.origin)    
print(banana.name, banana.quantity, banana.origin) 
print(melon.name, melon.quantity, melon.origin)    
```

출력 결과 :

```tex
사과 10 한국
바나나 5 필리핀
멜론 3 원산지 미상
```

필수 매개변수를 전달하지 않으면 오류가 발생한다.

```python
# Fruit()  # TypeError: __init__() missing required arguments
```



## 4. 메서드

메서드(method)는 클래스 내부에 정의된 함수이다. 메서드는 객체나 클래스와 관련된 동작을 수행한다.

| 종류            | 첫 번째 매개변수 | 사용 목적                                                    |
| :-------------- | :--------------- | :----------------------------------------------------------- |
| 인스턴스 메서드 | self             | 인스턴스의 속성을 읽거나 변경한다.                           |
| 클래스 메서드   | cls              | 클래스 자체의 상태를 읽거나 변경한다.                        |
| 정적 메서드     | 없음             | 클래스와 관련은 있지만 인스턴스나 클래스 상태를 직접 쓰지 않는다. |



### 4.1 인스턴스 메서드

인스턴스 메서드는 첫 번째 매개변수로 `self` 를 받는다. `self` 를 통해 인스턴스 변수에 접근한다.

```python
class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def print_info(self):
        print(f"과일 이름: {self.name}")
        print(f"수량: {self.quantity}")

    def add_quantity(self, amount):
        self.quantity += amount
        print(f"{amount}개 추가되었다.")


apple = Fruit("사과", 10)

apple.print_info()
apple.add_quantity(5)
apple.print_info()
```

출력 결과 :

```tex
과일 이름: 사과
수량: 10
5개 추가되었다.
과일 이름: 사과
수량: 15
```



### 4.2 클래스 메서드와 정적 메서드

클래스 메서드는 `@classmethod` 데코레이터를 사용하고, 첫 번째 매개변수로 `cls` 를 받는다. 정적 메서드는 `@staticmethod` 데코레이터를 사용하며, `self`나 `cls` 를 자동으로 받지 않는다.

```python
class Order:
    tax_rate = 0.1

    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity

    @classmethod
    def set_tax_rate(cls, rate):
        cls.tax_rate = rate

    @staticmethod
    def calculate_discount(price, discount_rate):
        return price * (1 - discount_rate)


order1 = Order(10000, 2)

print("총 가격:", order1.total_price())  # 20000

discounted = Order.calculate_discount(order1.total_price(), 0.2)
print("할인 적용 가격:", discounted)  # 16000.0

Order.set_tax_rate(0.2)
print("변경된 세율:", Order.tax_rate)  # 0.2
```

출력 결과 :

```tex
총 가격: 20000
할인 적용 가격: 16000.0
변경된 세율: 0.2
```



### 4.3 데코레이터

데코레이터(decorator) 는 기존 함수나 메서드를 직접 수정하지 않고 기능을 감싸서 추가 동작을 붙이는 문법이다.

```python
def trace(func):
    def wrapper():
        print("함수 실행 전")
        func()
        print("함수 실행 후")

    return wrapper


@trace
def hello():
    print("hello")


hello()
```

출력 결과 :

```tex
함수 실행 전
hello
함수 실행 후
```

위 코드는 다음 코드와 같은 의미이다.

```python
def trace(func):
    def wrapper():
        print("함수 실행 전")
        func()
        print("함수 실행 후")

    return wrapper


def hello():
    print("hello")


hello = trace(hello)
hello()
```

`@classmethod` , `@staticmethod` 도 데코레이터이다. 메서드가 클래스와 연결되는 방식을 바꿔준다.



## 5. 클래스 변수

클래스 변수는 클래스에 속하는 변수이다. 해당 클래스로 만든 모든 인스턴스가 공유하는 값이다. 객체마다 다른 값을 가져야 한다면 인스턴스 변수를 사용하고, 모든 객체가 공유해야 한다면 클래스 변수를 사용한다.

```python
class Fruit:
    origin = "한국"

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def print_info(self):
        print(f"원산지: {Fruit.origin}")
        print(f"이름: {self.name}")
        print(f"수량: {self.quantity}")


apple = Fruit("사과", 10)
banana = Fruit("바나나", 5)

apple.print_info()
banana.print_info()

print("----- 클래스 변수 변경 -----")
Fruit.origin = "필리핀"

apple.print_info()
banana.print_info()
```

출력 결과 :

```tex
원산지: 한국
이름: 사과
수량: 10
원산지: 한국
이름: 바나나
수량: 5
----- 클래스 변수 변경 -----
원산지: 필리핀
이름: 사과
수량: 10
원산지: 필리핀
이름: 바나나
수량: 5
```

`Fruit.origin` 을 변경하면 모든 인스턴스가 변경된 클래스 변수 값을 참조한다.

### 5.1 인스턴스 변수로 같은 이름을 만들면?

인스턴스에 클래스 변수와 같은 이름의 변수를 만들면, 그 인스턴스에서는 인스턴스 변수가 우선 조회된다.

```python
class Fruit:
    origin = "한국"

    def __init__(self, name):
        self.name = name


apple = Fruit("사과")
banana = Fruit("바나나")

apple.origin = "미국"

print(apple.origin)   
print(banana.origin)  
print(Fruit.origin)   
```

출력 결과 : 

```tex
미국
한국
한국
```

`apple.origin = "미국"` 은 클래스 변수 `Fruit.origin`을 바꾼 것이 아니라, `apple` 인스턴스에 `origin` 이라는 인스턴스 변수를 새로 만든 것이다.



## 10. 마무리

이번 글에서 정리한 핵심은 다음과 같다.

| 주제          | 핵심                                                         |
| :------------ | :----------------------------------------------------------- |
| 변수의 범위   | 파이썬은 LEGB 규칙에 따라 이름을 찾는다.                     |
| 클로저        | 내부 함수가 외부 함수의 변수를 기억하는 구조이다.            |
| 함수 객체     | 함수도 객체이므로 변수에 담고 인자로 전달할 수 있다.         |
| 콜백 함수     | 다른 함수에 전달되어 나중에 호출되는 함수이다.               |
| 람다 함수     | 짧은 함수를 한 줄로 표현하는 익명 함수이다.                  |
| 클래스        | 객체를 만들기 위한 설계도이다.                               |
| 인스턴스 변수 | 객체마다 따로 저장되는 값이다.                               |
| 클래스 변수   | 같은 클래스의 모든 인스턴스가 공유하는 값이다.               |
| 메서드        | 클래스 내부에 정의된 함수로, 객체나 클래스의 동작을 표현한다. |

함수는 코드를 동작 단위로 나누는 도구이고, 클래스는 데이터와 동작을 하나의 구조로 묶는 도구이다. 두 개념을 함께 이해하면 프로그램을 더 읽기 쉽고 확장 가능한 형태로 설계할 수 있다.



# [Python] 객체지향 프로그래밍 4대 개념 정리

객체지향 프로그래밍(OOP, Object-Oriented Programming)은 프로그램을 객체 단위로 구성하는 방식이다. 객체는 데이터인 **속성(attribute)**과 동작인 **메서드(method)**를 함께 가진다.

객체지향 프로그래밍의 핵심 개념은 보통 다음 네 가지로 정리한다.

| 개념 | 핵심 의미 |
| --- | --- |
| 캡슐화 | 데이터와 메서드를 하나로 묶고, 외부의 직접 접근을 제한한다. |
| 상속 | 기존 클래스의 속성과 메서드를 물려받아 재사용하고 확장한다. |
| 다형성 | 같은 이름의 메서드가 객체 종류에 따라 다르게 동작한다. |
| 추상화 | 복잡한 내부 구현은 숨기고 핵심 기능만 외부에 제공한다. |

이 네 가지 개념을 활용하면 코드의 재사용성, 확장성, 유지보수성을 높일 수 있다.

---

## 1. 캡슐화

캡슐화(encapsulation)는 객체의 데이터와 기능을 하나로 묶고, 외부에서 내부 구현에 직접 접근하지 못하도록 제한하는 개념이다.

파이썬은 Java나 C++처럼 접근 제어자를 강제하지 않는다. 대신 이름 규칙으로 접근 수준을 표현한다.

| 형태 | 이름 예시 | 의미 |
| --- | --- | --- |
| public | `name` | 외부에서 자유롭게 접근 가능 |
| protected 관례 | `_name` | 클래스 내부 또는 자식 클래스에서 사용하자는 관례 |
| private 네임 맹글링 | `__name` | 외부 직접 접근을 어렵게 만들기 위해 이름을 변경 |

### 1.1 getter와 setter로 값 보호하기

가격처럼 잘못된 값이 들어오면 안 되는 데이터는 직접 수정하게 두기보다 메서드를 통해 검증하는 것이 좋다.

```python
class Fruit:
    def __init__(self, name, price):
        self.name = name          # public
        self.__price = price      # private처럼 사용

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price > 0:
            self.__price = price
        else:
            print("가격은 0보다 커야 한다.")

    def print_info(self):
        print(f"과일: {self.name}")
        print(f"가격: {self.__price}")


class Apple(Fruit):
    def __init__(self, name, price, origin):
        super().__init__(name, price)
        self.origin = origin

    def print_origin(self):
        print(f"{self.name}의 원산지: {self.origin}")


apple = Apple("사과", 3000, "한국")

apple.print_info()
apple.print_origin()

print("가격 조회:", apple.get_price())

print("----- 가격 수정 -----")
apple.set_price(3500)
print("수정된 가격:", apple.get_price())

print("----- 잘못된 값 입력 -----")
apple.set_price(-1000)

print("----- 외부 접근 시도 -----")
apple.__price = 10000

print("getter로 확인:", apple.get_price())
print("직접 접근:", apple.__price)
```

출력 결과:

```text
과일: 사과
가격: 3000
사과의 원산지: 한국
가격 조회: 3000
----- 가격 수정 -----
수정된 가격: 3500
----- 잘못된 값 입력 -----
가격은 0보다 커야 한다.
----- 외부 접근 시도 -----
getter로 확인: 3500
직접 접근: 10000
```

`self.__price`는 실제로 완전한 private이 되는 것이 아니다. 파이썬 내부에서 `_Fruit__price`라는 이름으로 바뀐다. 이를 **네임 맹글링(name mangling)**이라고 한다.

```python
class Fruit:
    def __init__(self, price):
        self.__price = price


fruit = Fruit(3000)

print(fruit.__dict__)
print(fruit._Fruit__price)
```

출력 결과:

```text
{'_Fruit__price': 3000}
3000
```

즉, `__price`는 외부 접근을 어렵게 만드는 장치이지 보안을 위한 완전한 차단 장치는 아니다.

### 1.2 `@property`로 Pythonic하게 캡슐화하기

파이썬에서는 getter/setter 메서드를 직접 호출하기보다 `@property`를 사용해 속성처럼 접근하는 방식을 자주 사용한다.

```python
class Fruit:
    def __init__(self, name, price):
        self.name = name
        self.__price = price

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value > 0:
            self.__price = value
        else:
            print("가격은 0보다 커야 한다.")

    def print_info(self):
        print(f"과일: {self.name}")
        print(f"가격: {self.price}")


class Apple(Fruit):
    def __init__(self, name, price, origin):
        super().__init__(name, price)
        self.origin = origin

    def print_origin(self):
        print(f"{self.name}의 원산지: {self.origin}")


apple = Apple("사과", 3000, "한국")

apple.print_info()
apple.print_origin()

print("가격 조회:", apple.price)

print("----- 가격 수정 -----")
apple.price = 3500
print("수정된 가격:", apple.price)

print("----- 잘못된 값 입력 -----")
apple.price = -1000

print("----- 외부 접근 시도 -----")
apple.__price = 10000

print("실제 가격:", apple.price)
print("외부에서 만든 값:", apple.__price)
```

출력 결과:

```text
과일: 사과
가격: 3000
사과의 원산지: 한국
가격 조회: 3000
----- 가격 수정 -----
수정된 가격: 3500
----- 잘못된 값 입력 -----
가격은 0보다 커야 한다.
----- 외부 접근 시도 -----
실제 가격: 3500
외부에서 만든 값: 10000
```

`@property`를 사용하면 메서드로 검증 로직을 유지하면서도 외부에서는 속성처럼 읽고 쓸 수 있다.

---

## 2. 상속

상속(inheritance)은 기존 클래스의 속성과 메서드를 새로운 클래스가 물려받는 구조이다. 기존 클래스를 **부모 클래스**, 상속받는 클래스를 **자식 클래스**라고 부른다.

```python
class Parent:
    pass


class Child(Parent):
    pass
```

출력 결과:

```text
출력 결과 없음
```

### 2.1 상속 구조

자식 클래스는 부모 클래스의 생성자와 메서드를 사용할 수 있다.

```python
class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def store(self, place):
        print(f"{self.name}를 {place}에 보관한다.")

    def sell(self, amount):
        print(f"{self.name}를 {amount}개 판매한다.")


class Apple(Fruit):
    pass


fruit = Fruit("배", 100)
fruit.store("창고")
fruit.sell(10)

apple = Apple("사과", 50)
apple.store("냉장고")
apple.sell(5)
```

출력 결과:

```text
배를 창고에 보관한다.
배를 10개 판매한다.
사과를 냉장고에 보관한다.
사과를 5개 판매한다.
```

`Apple` 클래스에는 아무 메서드도 직접 정의하지 않았지만 `Fruit`를 상속했기 때문에 `store()`와 `sell()`을 사용할 수 있다.

### 2.2 자식 클래스에 생성자가 없을 때

자식 클래스에 `__init__()`이 없으면 부모 클래스의 생성자가 자동으로 호출된다.

```python
class Fruit:
    def __init__(self, name):
        print("Fruit 생성자 호출")
        self.name = name


class Apple(Fruit):
    pass


apple = Apple("사과")
print(apple.name)
```

출력 결과:

```text
Fruit 생성자 호출
사과
```

### 2.3 자식 클래스에 생성자를 직접 정의할 때

자식 클래스에 `__init__()`을 직접 정의하면 부모 생성자는 자동으로 호출되지 않는다.

```python
class Fruit:
    def __init__(self, name):
        print("Fruit 생성자 호출")
        self.name = name


class Apple(Fruit):
    def __init__(self, name):
        print("Apple 생성자 호출")


apple = Apple("사과")
# print(apple.name)  # AttributeError: 'Apple' object has no attribute 'name'
```

출력 결과:

```text
Apple 생성자 호출
```

부모 클래스의 초기화 로직이 필요하다면 `super()`로 부모 생성자를 명시적으로 호출해야 한다.

```python
class Fruit:
    def __init__(self, name):
        print("Fruit 생성자 호출")
        self.name = name


class Apple(Fruit):
    def __init__(self, name):
        super().__init__(name)
        print("Apple 생성자 호출")


apple = Apple("사과")
print(apple.name)
```

출력 결과:

```text
Fruit 생성자 호출
Apple 생성자 호출
사과
```

---

## 3. 오버라이딩

오버라이딩(overriding)은 부모 클래스에 정의된 메서드를 자식 클래스에서 같은 이름으로 다시 정의하는 것이다. 자식 클래스는 부모의 기본 동작을 자신에게 맞게 변경할 수 있다.

```python
class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def eat(self):
        print(f"{self.name}를 먹는다.")

    def store(self, place):
        print(f"{self.name}를 {place}에 보관한다.")


class Apple(Fruit):
    def wash(self):
        print(f"{self.name}를 깨끗이 씻는다.")

    def eat(self):
        print(f"{self.name}를 아주 맛있게 먹는다.")

    def super_eat(self):
        super().eat()


apple = Apple("사과", 10)

apple.eat()
apple.store("냉장고")
apple.wash()

print("----- 부모 메서드 호출 -----")
apple.super_eat()

fruit = Fruit("배", 20)
fruit.eat()
fruit.store("창고")
```

출력 결과:

```text
사과를 아주 맛있게 먹는다.
사과를 냉장고에 보관한다.
사과를 깨끗이 씻는다.
----- 부모 메서드 호출 -----
사과를 먹는다.
배를 먹는다.
배를 창고에 보관한다.
```

`Apple.eat()`은 `Fruit.eat()`을 오버라이딩한다. 따라서 `apple.eat()`을 호출하면 자식 클래스의 메서드가 실행된다.

---

## 4. 다중 상속과 MRO

다중 상속은 하나의 클래스가 둘 이상의 부모 클래스를 상속받는 기능이다.

```python
class Parent1:
    pass


class Parent2:
    pass


class Child(Parent1, Parent2):
    pass
```

출력 결과:

```text
출력 결과 없음
```

파이썬은 다중 상속을 지원하지만, 부모 클래스에 같은 이름의 메서드가 있을 때 어떤 메서드를 먼저 찾을지 정해야 한다. 이 순서를 **MRO(Method Resolution Order)**라고 한다.

### 4.1 다중 상속 예제

```python
class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def eat(self):
        print(f"{self.name}를 먹는다.")

    def sleep(self, hour):
        print(f"{self.name}를 {hour}시간 동안 보관한다.")


class Storage:
    def process(self, hour):
        print(f"{self.name}를 {hour}시간 동안 가공한다.")

    def sleep(self, hour):
        print(f"{self.name}를 {hour}시간 동안 저온 숙성한다.")


class ProcessedFruit(Fruit, Storage):
    pass


fruit = ProcessedFruit("사과", 10)

fruit.eat()
fruit.process(2)
fruit.sleep(8)

print(ProcessedFruit.mro())
```

출력 결과:

```text
사과를 먹는다.
사과를 2시간 동안 가공한다.
사과를 8시간 동안 보관한다.
[<class '__main__.ProcessedFruit'>, <class '__main__.Fruit'>, <class '__main__.Storage'>, <class 'object'>]
```

`ProcessedFruit(Fruit, Storage)`처럼 작성했기 때문에 `sleep()`을 찾을 때 `Fruit`를 먼저 확인한다. 따라서 `Storage.sleep()`이 아니라 `Fruit.sleep()`이 실행된다.

### 4.2 `object` 클래스

파이썬의 모든 클래스는 명시적으로 상속하지 않아도 최상위 부모인 `object` 클래스를 상속한다.

```python
class Fruit:
    pass


print(Fruit.mro())
print(isinstance(Fruit(), object))
```

출력 결과:

```text
[<class '__main__.Fruit'>, <class 'object'>]
True
```

`object`는 모든 객체가 가져야 할 최소한의 공통 기능을 제공한다. `__str__`, `__repr__`, `__eq__` 같은 기본 매직 메서드도 `object`로부터 시작된다.

### 4.3 MRO와 `super()`

`super()`는 단순히 “부모 클래스 하나”를 의미하는 것이 아니라, MRO 순서상 다음 클래스를 찾아가는 도구이다.

```python
class Base:
    def hello(self):
        print("Base")


class Clean(Base):
    def hello(self):
        print("Clean")
        super().hello()


class Pack(Base):
    def hello(self):
        print("Pack")
        super().hello()


class Product(Clean, Pack):
    def hello(self):
        print("Product")
        super().hello()


p = Product()
p.hello()

print(Product.mro())
```

출력 결과:

```text
Product
Clean
Pack
Base
[<class '__main__.Product'>, <class '__main__.Clean'>, <class '__main__.Pack'>, <class '__main__.Base'>, <class 'object'>]
```

`Product`의 MRO는 `Product -> Clean -> Pack -> Base -> object` 순서이다. 각 클래스에서 `super().hello()`를 호출하면 이 순서대로 다음 클래스의 `hello()`가 실행된다.

---