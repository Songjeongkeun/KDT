# [8일차] Python

객체지향 프로그래밍(OOP, Object-Oriented Programming)은 프로그램을 객체 단위로 구성하는 방식이다. 객체는 데이터인 **속성(attribute)**과 동작인 **메서드(method)**를 함께 가진다.

객체지향 프로그래밍의 핵심 개념은 보통 다음 네 가지로 정리한다.

| 개념   | 핵심 의미                                                   |
| :----- | :---------------------------------------------------------- |
| 캡슐화 | 데이터와 메서드를 하나로 묶고, 외부의 직접 접근을 제한한다. |
| 상속   | 기존 클래스의 속성과 메서드를 물려받아 재사용하고 확장한다. |
| 다형성 | 같은 이름의 메서드가 객체 종류에 따라 다르게 동작한다.      |
| 추상화 | 복잡한 내부 구현은 숨기고 핵심 기능만 외부에 제공한다.      |

이 네 가지 개념을 활용하면 코드의 재사용성, 확장성, 유지보수성을 높일 수 있다.

## 5. 다형성(Polymorphism)

다형성(polymorphism) 은 같은 이름의 메서드라도 객체의 종류에 따라 다르게 동작할 수 있는 특성이다.

파이썬은 정적 타입 언어처럼 명시적인 인터페이스 구현을 강제하지 않아도, 객체가 필요한 메서드를 가지고 있으면 사용할 수 있다. 이를 **덕 타이핑(duck typing)**이라고 한다.

> "오리처럼 걷고 오리처럼 소리 내면 오리로 볼 수 있다" 는 사고방식에서 나온 표현이다. 파이썬에서는 객체의 실제 타입보다 "필요한 동작을 할 수 있는가" 가 중요하다.

### 5.1 상속 기반 다형성

```python
class Fruit:
  def describe(self):
    print("과일이다.")

class Apple(Fruit):
    def describe(self):
        print("사과는 아삭하다.")


class Banana(Fruit):
    def describe(self):
        print("바나나는 달콤하다.")


fruits = [Apple(), Banana(), Fruit()]

for fruit in fruits:
    fruit.describe()
```

출력 결과 :

```tex
사과는 아삭하다.
바나나는 달콤하다.
과일이다.
```

반복문에서는 모두 `fruit.describe()` 라는 같은 코드를 호출한다. 하지만 실제 객체가 `Apple` 인지, `Banana` 인지, `Fruit` 인지에 따라 실행 결과가 달라진다.



### 5.2 덕 타이핑 기반 다형성

다형성은 반드시 상속이 있어야만 가능한 것은 아니다. 서로 다른 클래스라도 같은 이름의 메서드를 가지고 있으면 공통된 방식으로 처리할 수 있다.

```python
class CardPayment:
    def pay(self, amount):
        print(f"카드로 {amount}원 결제한다.")


class CashPayment:
    def pay(self, amount):
        print(f"현금으로 {amount}원 결제한다.")


class KakaoPay:
    def pay(self, amount):
        print(f"카카오페이로 {amount}원 결제한다.")


def process_payment(payment, amount):
    payment.pay(amount)


card = CardPayment()
cash = CashPayment()
kakao = KakaoPay()

process_payment(card, 10000)
process_payment(cash, 5000)
process_payment(kakao, 2000)
```

출력 결과 :

```tex
카드로 10000원 결제한다.
현금으로 5000원 결제한다.
카카오페이로 2000원 결제한다.
```

`process_payment()` 함수는 전달받은 객체가 어떤 클래스인지 검사하지 않는다. 그 객체에 `pay()` 메서드가 있다고 믿고 호출한다. 이처럼 같은 인터페이스를 가진 객체를 동일한 방식으로 다루는 것이 다형성의 핵심이다.

새로운 결제 수단을 추가할 때도 기존 `process_payment()` 함수를 수정할 필요가 없다.

```python
class NaverPay:
  def pay(self, amount):
    print(f"네이버페이로 {amount}원 결제한다.")
    
naver = NaverPay()
process_payment(naver, 3000)
```

출력 결과 :

```tex
네이버페이로 3000원 결제한다.
```

이 구조는 확장에 유리하다. 결제 수단이 늘어나도 각 클래스가 `pay()` 메서드만 제공하면 공통 처리 함수는 그대로 사용할 수 있다.



## 6. 추상화(abstraction)

추상화(abstraction) 는 복잡한 내부 구현은 숨기고, 외부에는 꼭 필요한 기능만 제공하는 개념이다.

사용자는 객체가 내부적으로 어떻게 동작하는지 몰라도, 제공된 메서드만으로 기능을 사용할 수 있다. 추상화는 "어떻게 동작하는가"보다 "무엇을 할 수 있는가" 에 집중하게 만드는 설계 방식이다.

파이썬에서는 일반 클래스 설계만으로도 추상화를 표현할 수 있고, 더 명확한 규칙이 필요하면 `abc` 모듈의 `ABC`, `abstractmethod` 를 사용해 추상 클래스를 만들 수 있다.



### 6.1 추상 클래스 기본 예제

```python
from abc import ABC, abstractmethod

class Fruit(ABC):
    @abstractmethod
    def eat(self):
        pass


class Apple(Fruit):
    def eat(self):
        print("사과를 먹는다.")


class Banana(Fruit):
    def eat(self):
        print("바나나를 먹는다.")


apple = Apple()
banana = Banana()

apple.eat()
banana.eat()

# fruit = Fruit()  # TypeError: 추상 클래스는 직접 인스턴스화할 수 없음
```

출력 결과 :

```tex
사과를 먹는다.
바나나를 먹는다.
```

추상 클래스는 "자식 클래스가 반드시 구현해야 하는 메서드" 를 정해준다. 위 예제에서 `Fruit` 를 상속받는 클래스는 `eat()` 메서드를 반드시 구현해야한다.



### 6.2 결제 기능으로 보는 추상화

결제 시스템을 만든다고 가정해보자. 카드 결제, 현금 결제, 카카오페이는 내부 처리 방식이 서로 다르다. 하지만 외부에서 볼 때는 모두 "금액을 결제한다." 는 공통 기능을 제공한다.

이때 `Payment` 라는 추상 클래스를 만들고, 모든 결제 클래스가 `pay()`를 반드시 구현하도록 강제할 수 있다.

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CardPayment(Payment):
    def pay(self, amount):
        print(f"카드로 {amount}원 결제한다.")


class CashPayment(Payment):
    def pay(self, amount):
        print(f"현금으로 {amount}원 결제한다.")


class KakaoPay(Payment):
    def pay(self, amount):
        print(f"카카오페이로 {amount}원 결제한다.")


def process_payment(payment: Payment, amount):
    payment.pay(amount)


card = CardPayment()
cash = CashPayment()
kakao = KakaoPay()

process_payment(card, 10000)
process_payment(cash, 5000)
process_payment(kakao, 2000)
```

출력 결과 :

```tex
카드로 10000원을 결제한다.
현금으로 5000원 결제한다.
카카오페이로 2000원 결제한다.
```

`process_payment()` 함수는 결제 객채의 내부 구현을 알 필요가 없다. 단지 `Payment`계열 객체가 `pay()` 메서드를 제공한다는 규치만 알고 있으면 된다.



### 6.3 추상 메서드를 구현하지 않으면?

추상 클래스를 상속받았는데 추상 메서드를 구현하지 않으면 해당 클래스는 인스턴스를 만들 수 없다.

```python
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class BankTransfer(Payment):
    pass

# bank = BankTransfer()
# TypeError: Can't instantiate abstract class BankTransfer with abstract method pay
```

이처럼 추상화는 자식 클래스가 지켜야 할 공통 규칙을 명확히 만든다.



### 6.4 다형성과 추상화의 관계

다형성과 추상화는 함께 쓰일 때 강력하다.

| 개념   | 결제 예제에서의 의미                                         |
| :----- | :----------------------------------------------------------- |
| 추상화 | 모든 결제 수단은 pay()를 제공해야 한다는 규칙을 만든다.      |
| 다형성 | process_payment()가 카드, 현금, 카카오페이를 같은 방식으로 처리한다. |

추상화가 공통 인터페이스를 설계하고, 다형성이 그 인터페이스를 통해 여러 객체를 유연하게 실행하게 만든다.



## 7. 마무리

객체지향 프로그래밍의 네 가지 핵심 개념은 서로 연결되어 있다.

| 개념   | 역할                                                     |
| :----- | :------------------------------------------------------- |
| 캡슐화 | 객체의 내부 상태를 보호하고 안전한 사용 방법을 제공한다. |
| 상속   | 공통 코드를 재사용하고 자식 클래스에서 확장한다.         |
| 다형성 | 같은 인터페이스로 다양한 객체를 다룰 수 있게 한다.       |
| 추상화 | 핵심 기능만 드러내고 세부 구현을 숨긴다.                 |

캡슐화는 객체를 안전하게 만들고, 상속은 코드를 재사용하게 해준다. 오버라이딩과 다형성은 같은 호출이 객체에 따라 다른 동작을 하게 만들며, 추상화는 클래스가 지켜야 할 공통 규칙을 정의한다. 이 개념들을 함께 이해하면 더 유연하고 유지보수하기 쉬운 코드를 작성할 수 있다.



# 예외 처리 정리

예외(exception)는 프로그램 실행 중 발생할 수 있는 오류 상황을 의미한다. 예외가 발생하면 프로그램은 기본적으로 중단된다. 따라서 예상 가능한 오류는 적절히 처리해 프로그램이 갑자기 종료되지 않도록 만들고, 사용자나 개발자에게 필요한 정보를 제공해야 한다.



## 1. 예외란?

예외는 실행 중에 발생하는 오류이다. 문법 오류처럼 실행 전에 발견되는 문제와 달리, 예외는 프로그램이 실행되다가 특정 상황에서 발생한다.

```python
print(int(10 / 3))
print(5 / 0)
print(4 / 2)
```

출력 결과 :

```tex
3
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```

`5/0` 에서 `ZeroDivisionError` 가 발생하면 프로그램은 그 지점에서 중단된다. 따라서 그 아래에 있는 `print(4 / 2)` 는 실행되지 않는다.

자주 만나는 예외는 다음과 같다.

| 타입                | 발생 상황        | 간단 예제          | 설명                      |
| ------------------- | ---------------- | :----------------- | :------------------------ |
| Exception           | 일반 적인 예외   | `except Exception` | 대부분 예외의 부모        |
| Value Error         | 값이 잘못 됨     | `int("abc")`       | 타입은 맞지만 값이 잘못됨 |
| TypeError           | 타입이 잘못됨    | `"10" + 10`        | 연산 불가능한 타입        |
| ZeroDivisionError   | 0으로 나눔       | `1 / 0 `           | 수학적 오류               |
| IndexError          | 리스트 범위 초과 | `list[5]`          | 인덱스 범위 오류          |
| KeyError            | 딕셔너리 키 없음 | `d["b"]`           | 존재하지 않는 키          |
| AttributeError      | 속성 없음        | `x.append()`       | 객체에 없는 메서드        |
| FileNotFoundError   | 파일 없음        | `open("x.txt")`    | 파일 경로 오류            |
| ModuleNotFoundError | 모듈 없음        | `import x`         | 모듈 import 실패          |
| StopIteration       | 반복 종료        | `next(iter([]))`   | 반복 끝                   |
| KeyboardInterrupt   | Ctrl + c         | 사용자 입력        | 강제 종료                 |
| SystemExit          | 프로그램 종료    | `exit()`           | 종료 요청                 |



## 2. 예외 계층 구조

파이썬 예외는 클래스 계층 구조를 가진다. 대표적인 구조는 다음과 같다.

```tex
BaseException
├── Exception
│   ├── ValueError
│   ├── TypeError
│   ├── ZeroDivisionError
│   ├── IndexError
│   └── ...
├── KeyboardInterrupt
└── SystemExit
```

일반적으로 우리가 처리하는 예외는 대부분 `Exception` 의 하위 클래스이다.

| 예외              | 의미                                                    |
| :---------------- | :------------------------------------------------------ |
| Exception         | 코드 실행 중 발생하는 일반적인 오류의 부모 클래스       |
| KeyboardInterrupt | 사용자가 Ctrl + C로 프로그램을 중단할 때 발생           |
| SystemExit        | exit() 또는 sys.exit()로 프로그램 종료를 요청할 때 발생 |

`KeyboardInterrupt` 오 `SystemExit` 는 일반적인 오류라기보다 프로그램을 중단하거나 종료하기 위한 신호에 가깝다. 그래서 보통은 `BaseException` 이 아니라 `Exception` 을 잡는다. 

```python
try:
  raise KeyboardInterrupt
except Exception:
  print("Exception 잡힘")
except BaseException:
  print("BaseException 잡힘")
```

출력 결과 :

```tex
BaseException 잡힘
```

`except:`  처럼 예외 타입을 생략하면 `BaseException` 계열까지 잡을 수 있어 위험하다. 사용자의 강제 종료 신호까지 막아버릴 수 있기 때문이다.



## 3. 예외 처리 기본 구조

예외 처리는 `try`, `except` , `else` , `finally` 를 사용한다.

```tex
try:
	예외가 발생할 가능성이 있는 코드
except 예외타입:
	해당 예외가 발생했을 때 실행할 코드
else:
	예외가 발생하지 않을 때 실행할 코드
finally:	
	예외 발생 여부와 관계없이 항상 실행할 코드
```

가장 기본적인 형태는 `try-except` 이다.

```python
try:
    print(10 / 3)
    print(5 / 0)
    print(4 / 2)
except Exception:
    print("예외 발생")

print("프로그램을 종료한다.")
```

출력 결과 :

```tex
3.3333333333333335
예외 발생
프로그램을 종료한다.
```

`try` 블록에서 예외가 발생하면 그 즉시 `except` 블록으로 이동한다. 따라서 `print(4 / 2)` 는 실행되지 않는다.

특정 예외만 처리할 수도 있다.

```python
try:
    print(10 / 3)
    print(5 / 0)
    print(4 / 2)
except ZeroDivisionError:
    print("0으로 나눌 수 없음")

print("프로그램을 종료한다.")
```

출력 결과 :

```tex
3.3333333333333335
0으로 나눌 수 없음
프로그램을 종료한다.
```



## 4. 여러 예외 처리하기

상황에 따라 발생할 수 있는 예외가 다르다면 `except` 를 여러개 사용할 수 있다.

```python
try:
  data = [10, 20, 30, 40, 50]
  print(data[0])
  print(data[5])
  print(data[1])
except IndexError:
  print("인덱스 오류")

print("프로그램을 종료한다.")
```

출력 결과 :

```tex
10
인덱스 오류
프로그램을 종료한다.
```

여러 예외를 나누어 처리하면 오류 원인에 맞는 메시지를 제공할 수 있다.

```python
try:
    data = [10, 20, 30, 40, 50]
    print(5 / 0)
except IndexError:
    print("인덱스 오류")
except ValueError:
    print("입력 오류")
except ZeroDivisionError:
    print("0으로 나눌 수 없음")
except Exception:
    print("예외 발생")
else:
    print("에러가 발생하지 않은 정상적인 프로그램")
finally:
    print("에러에 관계없이 무조건 실행되는 문장")

print("프로그램을 종료한다.")
```

출력 결과 :

```tex
0으로 나눌 수 있다.
에러에 관계없이 무조건 실행되는 문장
프로그램을 종료한다.
```

`except` 는 구체적인 예외부터 작성하는 것이 좋다. `Exception` 을 가장 위에 쓰면 대부분의 예외가 먼저 잡혀서 아래의 구체적인 `except` 블록은 실행되지 않는다.



### 4.1 `else` 와 `finally` 

`else` 는 `try` 블록에서 예외가 발생하지 않았을 때만 실행된다. `finally` 는 예외 발생 여부와 관계없이 항상 실행된다.

```python 
try:
    number = int("10")
except ValueError:
    print("숫자로 변환할 수 없음")
else:
    print("변환 성공:", number)
finally:
    print("변환 시도 종료")
```

출력 결과 :

```tex
변환 성공: 10
변환 시도 종료
```

`finally` 는 파일 닫기, DB 연결 해제, 임시 리소스 정리처럼 반드시 실행되어야 하는 작업에 사용한다.



## 5. 예외 객체 활용하기

`except 예외타입 as 변수` 형태를 사용하면 발생한 예외 객체를 변수로 받을 수 있다.

```python
try:
    int("abc")
except Exception as e:
    print("에러 메시지:", e)
    print("에러 타입:", type(e))
    print("args:", e.args)
```

출력 결과 :

```tex
에러 메시지: invalid literal for int() with base 10: 'abc'
에러 타입: <class 'ValueError'>
args: ("invalid literal for int() with base 10: 'abc'",)
```

예외 객체에는 오류 메시지, 타입, 추가 정보가 들어있다.

```tex
Exception 객체
├── args        → 에러 메시지나 전달된 값
├── __str__()   → 사용자용 문자열 표현
├── __repr__()  → 개발자용 표현
├── __class__   → 예외 타입
└── traceback   → 에러 발생 위치 정보
```

`as e` 를 사용하는 이유는 발생한 예외 객체의 정보를 활용하기 위해서이다.



## 6. `raise` 로 예외 발생시키기

`raise` 는 의도적으로 예외를 발생시키는 키워드이다. 잘못된 입력이나 비정상적인 상태를 명확히 알릴 때 사용한다.

```python
try:
    raise Exception("예외가 발생했어요")
except Exception as e:
    print(e)
```

출력 결과 :

```tex
예외가 발생했어요.
```



### 6.1 조건에 따라 예외 발생시키기

```python
def validate_even(number):
    if number % 2 == 1:
        raise ValueError("홀수를 입력했어요")
    print(number)


try:
    validate_even(3)
except ValueError as e:
    print("예외가 발생:", e)
```

출력 결과 :

```tex
예외가 발생: 홀수를 입력했어요
```

이처럼 함수 내부에서 문제를 발견하면 `raise` 로 예외를 발생기키고, 함수를 호출한 쪽에서 처리하게 만들 수 있다.



### 6.2 현재 예외 다시 전달하기

`except` 블록 안에서 `raise` 만 사용하면 현재 처리 중인 예외를 다시 바깥으로 전달한다.

```python
def parse_number(text):
    try:
        return int(text)
    except ValueError:
        print("숫자 변환 실패")
        raise


try:
    parse_number("abc")
except ValueError as e:
    print("호출한 쪽에서 다시 처리:", e)
```

출력 결과 : 

```tex
숫자 변환 실패
호출한 쪽에서 다시 처리: invalid literal for int() with base 10: 'abc'
```



## 7. 예외 전파

예외는 현재 함수에서 처리되지 않으면 호출한 함수 쪽으로 전달된다. 이를 예외 전파라고 한다.

```python
def func1():
    func2()


def func2():
    func3()


def func3():
    print("%d" % "문자열")


try:
    func1()
except TypeError:
    print("타입이 올바르지 않다.")
```

출력 결과 :

```python
타입이 올바르지 않다. 
```

`func3()` 에서 발생한 `TypeError` 는 `func2()`, `func1()` 을 거쳐 최종적으로 바깥의 `try-except` 에서 처리된다.

함수 내부에서 직접 처리할 수도 있다.

```python
def func1():
    func2()


def func2():
    func3()


def func3():
    try:
        print("%d" % "문자열")
    except TypeError:
        print("타입이 올바르지 않다.")


func1()
```

출력 결과 :

```tex
타입이 올바르지 않다.
```

어느 위치에서 예외를 처리할지는 프로그램 구조에 따라 달라진다. 보통 예외를 의미 있게 처리할 수 있는 위치에서 잡는 것이 좋다.



## 8. 좋은 예외 처리 습관

예외 처리는 단순히 오류를 숨기는 문법이 아니다. 프로그램이 실패할 수 있는 상황을 명확히 표현하고, 복구 가능한 오류를 적잘히 처리하기 위한 도구이다.



### 8.1 너무 넓게 잡지 않기

```python
try:
    result = 10 / 0
except Exception:
    print("문제가 발생했다.")
```

위 코드는 동작은 하지만 어떤 문제가 발생했는지 알기 어렵다. 가능하면 구체적인 예외를 잡는 것이 좋다. 

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("0으로 나눌 수 없다.")
```



### 8.2 예외를 조용히 무시하지 않기

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    pass
```

`pass` 로 예외를 무시하면 문제가 발생했는지 알기 어렵다. 정말 무시해도 되는 상황이 아니라면 로그를 남기거나 사용자에게 안내하는 것이 좋다.



### 8.3 입력 검증과 예외 처리를 함께 사용하기

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("b는 0이 될 수 없다.")
    return a / b


try:
    print(divide(10, 0))
except ZeroDivisionError as e:
    print(e)
```



## 9. 마무리

예외 처리는 프로그램이 예상치 못한 상황에서도 무너지지 않도록 도와주는 중요한 문법이다.

| 문법    | 역할                                            |
| :------ | :---------------------------------------------- |
| try     | 예외가 발생할 가능성이 있는 코드를 감싼다.      |
| except  | 특정 예외가 발생했을 때 실행할 코드를 작성한다. |
| else    | 예외가 발생하지 않았을 때 실행된다.             |
| finally | 예외 발생 여부와 관계없이 항상 실행된다.        |
| raise   | 의도적으로 예외를 발생시키거나 다시 전달한다.   |
| as e    | 발생한 예외 객체를 변수로 받아 정보를 활용한다. |

좋은 예외 처리는 오류를 숨기는 것이 아니라, 오류가 발생했을 때 프로그램이 어떤 방식으로 대응할지 명확하게 정하는 것이다.



# 매직 메서드와 제너레이터 정리

매직 메서드(magic method) 는  파이썬 특정 문법이나 연산이 실행될 때 자동으로 호출되는 특별한 메서드이다. `__len__`, `__str__`, `__getitem__ ` 처럼 이름의 앞뒤에 밑줄 두 개가 붙어 있어 dunder method 라고도 부른다.

매직 메서드를 클래스에 구현하면 `len(obj)` , `print(obj)` , `obj[0]` , `obj + other` , `with obj:` 같은 파이썬의 기본 문법과 사용자 정의 객체를 자연스럽게 연결할 수 있다.



## 1. 매직 메서드란?

매직 메서드는 개발자가 직접 호출하기보다 파이썬 문법에 의해 자동으로 호출되는 메서드이다.

| 문법               | 호출되는 매직 메서드              |
| :----------------- | :-------------------------------- |
| print(obj)         | `obj.__str__()`                   |
| repr(obj)          | `obj.__repr__()`                  |
| len(obj)           | `obj.__len__()`                   |
| obj[index]         | `obj.__getitem__(index)`          |
| obj[index] = value | `obj.__setitem__(index, value)`   |
| del obj[index]     | `obj.__delitem__(index)`          |
| obj()              | `obj.__call__()`                  |
| for item in obj    | `obj.__iter__(), obj.__next__()`  |
| with obj:          | `obj.__enter__(), obj.__exit__()` |
| obj1 + obj2        | `obj1.__add__(obj2)`              |

매직 메서드는 파이썬 문법을 사용자 정의 클래스와 연결하는 약속이다.



## 2. 객체 출력

객체를 출력할 때 가장 자주 사용하는 매직 메서드는 `__str__()` 과 `__repr__()`이다.

### 2.1 `__str__()` : 사용자에게 보여줄 문자열

`__str__()` 은 객체를 사람이 읽기 쉬운 문자열로 표현할 때 사용한다. `print(obj)`또는 `str(obj)` 를 호출하면 자동으로 실행된다. 

```python
class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} {self.quantity}개"


apple = Fruit("사과", 10)

print(apple)
print(str(apple))
```

출력 결과 :

```tex
사과 10개
사과 10개
```

`__str()__` 을 정의하지 않으면 객체를 출력했을 때 기본적으로 클래스 이름과 메모리 주소 형태가 출력된다.



### 2.2 `__repr__()` : 개발자를 위한 공식 표현

`__repr__()` 은 객첼ㄹ 개발자 관점에서 명확하게 표현하는 문자열을 반환한다. `repr(obj)` 를 호출할 때 실행되며, 가능하다면 객체를 다시 생성할 수 있는 형태의 문자열을 반환하는 것이 권장된다.

```python
class Fruit:
  def __init__(self, name, quantity):
    self.name = name
    self.quantity = quantity
    
    def __str__(self):
      return f"{self.name} {self.quantity}개"
    
    def __repr__(self):
      return f"Fruit'{self.name}', quantity={self.quantity})"
    
apple = Fruit("사과", 10)

print(str(apple))
print(repr(apple))
```

출력 결과 : 

```tex
사과 10개
Fruit(name='사과', quantity=10)
```

일반적으로 `__str__()` 은 사용자 친화적인 출력, `__repr__()` 은 디ㅓ깅에 유용한 출력을 담당한다.



## 3. 반복 가능한 객체와 제너레이터

반복 가능한 객체를 이해하려면 이터러블(iterable), 이터레이터(iterator), **제너레이터(generator)**를 구분해야 한다.

| 개념       | 설명                                                         |
| :--------- | :----------------------------------------------------------- |
| 이터러블   | iter()를 적용할 수 있는 객체이다. 예: 리스트, 튜플, 문자열   |
| 이터레이터 | __iter__()와 __next__()를 모두 구현해 값을 하나씩 꺼내는 객체이다. |
| 제너레이터 | yield를 사용해 간단히 만드는 이터레이터이다.                 |

### 3.1 `__iter__()` 와 `__next__()` 로 이터레이터 만들기

`for` 문은 내부적으로 `iter()` 를 호출해 이터레이터를 얻고, 반복할 때마다 `next()` 를 호출한다.

```python
class Counter:
    def __init__(self, max_count):
        self.max_count = max_count
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.max_count:
            self.current += 1
            return self.current
        raise StopIteration


counter = Counter(3)

for num in counter:
    print(num)

```

출력 결과 :

```tex
1
2
3
```

`__next__()` 는 다음 값을 반환하고, 더 이상 반환할 값이 없으면 `StopIteration` 예외를 발생시켜 반복을 종료한다.



### 3.2 제너레이터 함수

제너레이터는 `yield` 키워드를 사용해 값을 한 번에 하나씩 생성하는 함수이다. 일반 함수처럼 보이지만 `yield` 를 만다면 값을 반환하고 실행 상태를 유지한다. 다음 호출 시 이전 위치에서 이어서 실행된다.

```python
def counter(max_count):
  current = 0
 	while courrent < max_count:
    current += 1
    yield current
 
for num in counter(3)
	print(num)
```

출력 결과 :

```tex
1
2
3
```

`yield` 의 핵심은 다음과 같다. 

| 역할                 | 설명                                        |
| :------------------- | :------------------------------------------ |
| 값을 반환한다        | yield 값의 값을 호출한 쪽에 전달한다.       |
| 함수 상태를 저장한다 | 지역 변수와 실행 위치를 기억한다.           |
| 이어서 실행한다      | 다음 next() 호출 때 멈춘 위치부터 실행한다. |

제너레이터는 자동으로 `__iter__()`와` __next__()`를 제공하므로 직접 이터레이터 클래스를 만들지 않아도 된다.

### 3.3 제너레이터를 직접 `next()` 로 호출하기

```python
def counter(max_count):
  current = 0
  while current < max_count:
    current += 1
    yield current
    
gen = counter(2)

print(next(gen))
print(next(gen))
```

출력 결과 :

```tex
1
2
```

제너레이터는 모든 데이터를 한 번에 만들지 않고 필요할 때 하나씩 생성하므로 메모리 효율이 좋다.



## 4. 인덱싱과 아이템 조작

사용자 정의 객체도 `__getitem__()`, `__setitem__()` , `__delitem__()` 을 구현하면 리스트나 딕셔너리처럼 사용할 수 있다. 

| 문법               | 호출되는 메서드                   |
| :----------------- | :-------------------------------- |
| obj[index]         | `__getitem__(self, index)`        |
| obj[index] = value | `__setitem__(self, index, value)` |
| del obj[index]     | `__delitem__(self, index)`        |

```python
class MyList:
  def __init__(self):
    self.data = []
    
  def __getitem__(self, index):
    return self.data[index]
  
  def __setitem__(self, index, value):
    self.data[index] = value
  
  def __delitem__(self, index):
    del self.data[index]
    
ml = MyList()
ml.data = [10, 20, 30]

print(ml[0])

ml[1] = 99
print(ml.data)

del m1[0]
print(ml.data)
```

출력 결과 :

```tex
10
[10, 99, 30]
[99, 30]
```

이렇게 구현하면 `MyList` 객체가 내부적으로 리스트를 감싸고 있어도 외부에서는 `ml[0]` 처럼 자연스럽게 사용할 수 있다.



### 4.1 슬라이싱도 처리할 수 있다.

`obj[1:3]` 처럼 슬라이싱 하면 `__getitem__()` 의 `index` 에 `slice` 객체가 전달된다.

```python
class MyList:
  def __init__(self, data):
    self.data = data
  
  def __getitem__(self,index):
    return self.data[index]
  
ml = MyList([10, 20, 30, 40])

print(ml[1])
print(ml[1:3])
```

출력 결과 :

```tex
20
[20, 30]
```



## 5. 객체를 함수처럼 사용하기

`__call__()`을 구현하면 객체를 함수처럼 호출할 수 있다. 

```python
class Multiplier:
  def __init__(self, n):
    self.n = n
  
  def __call__(self, x):
    return x * self.n
  
m = Multiplier(3)

print(m(10))
```

 출력 결과 :

```
30
```

`m(10)` 은 내부적으로 `m.__call__(10)`을 호출한다. 객체가 상태를 가지고 있으면서 함수처럼 동작해야 할 때 유용한다.



## 6. 객체의 길이와 참/거짓 판단

### 6.1 `__len__()` 

`__len__()` 은 객체의 길이를 정의한다. `len(obj)` 를 호출할 때 자동으로 실행된다 

```python
class Basket:
  def __init__(self):
    self.items = []
  
  def __len__(self):
    return len(self.items)
  
basket = Basket()
basket.items = ["사과", "바나나", "오렌지"]

print(len(basket))
```

출력 결과 :

```tex
3
```



### 6.2 `__bool__()`

`__bool__()` 은 객체가 조건문에서 참인지 거지인지 판단할 때 호출된다. 

```python
class Basket:
  def __init__(self, items):
    self.items = items
    
  def __bool__(self):
    return len(self.items) > 0
  
empty_basket = Basket([])
fruit_basket = Basket(["사괴"])

print(bool(empty_basket))
print(bool(fruit_basket))
```

출력 결과 :

```tex
False
True
```



## 7. 연산자 오버로딩

연산자 오버로딩은 `+`, `==`, `<` 같은 연산자를 사용자 정의 객체에 맞게 동작하도록 만드는 것이다.



### 7.1 `__add__()` 

`__add__()` 는 `obj1 + obj2` 가 실행될 때 호출된다. 

```python
class Basket:
  def __init__(self, items):
    self.items = items
  
  def __add__(self, other):
    return Basket(self.items + other.items)
  
  def __repr__(self):
    print f"Basket({self.items})"
  
basket1 = Basket(["사과", "바나나"])
basket2 = Basket(["오렌지"])

result = basket1 + basket2
print(result)
```

출력 결과 :

```tex
Basket(['사과', '바나나', '오렌지'])
```

### 7.2 `__eq__()` 

`__eq__()`는 `obj1 == obj2` 가 실행될 때 호출된다.

```python
class Fruit: 
  def __init__(self, name, quantity):
    self.name = name
    self.quantity = quantity
    
  def __eq__(self, other):
    return self.name == other.name and self.quantity == other.quantity
  
apple1 = Fruit("사과", 10)
apple2 = Fruit("사과", 10)
apple3 = Fruit("사과", 5)

print(apple1==apple2)
print(apple2==apple3)
```

출력 결과 : 

```tex
True
False
```

비교 대상이 같은 타입인지 확인하려면 다음처럼 방어 코드를 넣을 수 있다. 

```python
class Fruit:
  def __init__(self, name, quantity):
    self.name = name
    self.quantity = quantity
    
  def __eq__(self, other):
    if not isinstance(other, Fruit):
      return NotImplemented
    else:
      return self.name==other.name and self.quantity==other.quantity

apple = Fruit("사과", 10)

print(apple == "사과")    
```

출력 결과 :

```tex
False
```

`NotImplemented` 는 "이 비교는 내가 처리할 수 없다."는 의미이다. 파이썬은 반대쪽 객체의 비교 메서드를 시도하거나 적잘한 기본 결과를 사용한다.



## 8. `with` 문과 컨텍스트 매니저 

`with` 문은 파일, 네티워크 연결, DB 연결처럼 사용 후 반드시 정리해야 하는 자원을 안전하게 관리하기 위한 문법이다. 

| 메서드      | 호출 시점             |
| :---------- | :-------------------- |
| __enter__() | with 블록에 진입할 때 |
| __exit__()  | with 블록이 끝날 때   |



### 8.1 기본 컨텍스트 매니저

```python
class MyResource:
  def __init__(self):
    print("자원 열기")
    return self
 
  def __exit__(self, exc_type, exc_value, traceback):
    print("자원 정리")

with MyResource() as resurce:
  print("자원 사용 중")
```

출력 결과 :

```tex
자원 열기 
자원 사용 중
자원 정리
```

`__enter__()` 에서 반환한 값은 `as` 뒤의 변수에 들어간다. `__exit__()` 은 예외 발생 여부와 관계없이 항상 호출된다.

### 8.2 예외가 발생해도 `__exit__()` 은 실행된다.

```python
class MyResource: 
  def __enter__(self):
    print("자원 열기")
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    print("자원 정리")
    print("예외 타입", exc_type)
    
    
try:
  with MyResource():
  	print("작업 중")
  	1 / 0
except ZeroDivisionError:
  print("바깥에서 예외 처리")
```

출력 결과 :

```tex
자원 열기
작업 중
자원 정리
예외 타입 : <class 'ZeroDivisionError'>
바깥에서 예외 처리
```

`__exit__()`은 예외 정보를 인자로 받는다.

| 매개변수  | 의미                |
| :-------- | :------------------ |
| exc_type  | 발생한 예외 타입    |
| exc_value | 발생한 예외 객체    |
| traceback | 예외 발생 위치 정보 |



### 8.3 `__exit__()` 의 반환값

`__exit__()` 이 `True` 를 반환하면 예외가 바깥으로 전파되지 않는다. 이를 예외 억제라고 한다.

```python
class IgnoreError:
  def __enter__(self):
    print("시작")
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    print("종료")
    return True
  
  
with IgnoreError():
  print("작업 중")
  1 / 0
 
print("프로그램 계속 실행")
```

출력 결과 :

```tex 
시작
작업 중
종료
프로그램 계속 실행
```

예외를 무조건 억제하면 문제를 숨길 수 있으므로, 명확한 의도가 있을때만 `True` 를 반환해야한다.



## 9. 마무리

매직 메서드는 파이썬의 문법과 사용자 정의 객체를 연결하는 핵심 기능이다. 

| 목적             | 매직 메서드                                       |
| :--------------- | :------------------------------------------------ |
| 객체 문자열 표현 | `__str__()`, `__repr__()`                         |
| 반복 처리        | `__iter__()`, `__next__()`                        |
| 인덱싱           | `__getitem__()`, `__setitem__()`, `__delitem__()` |
| 함수처럼 호출    | `__call__()`                                      |
| 길이와 참/거짓   | `__len__()`, `__bool__()`                         |
| 연산자           | `__add__()`, `__eq__()`                           |
| 컨텍스트 관리    | `__enter__()`, `__exit__()`                       |

매직 메서드를 잘 활용하면 사용자 정의 객체도 파이썬의 기본 자료형처럼 자연스럽게 사용할 수 있다. 다만 모든 기능을 매직 메서드로 해결하려 하기보다, 파이썬 문법과 자연스럽게 연결될 때 사용하는 것이 좋다.