# MySQL을 활용한 Python 단어장 프로그램

Python과 MySQL을 연결해 단어를 등록·조회·검색·수정·삭제하는 콘솔 단어장 프로그램을 구현한다.

수업에서 작성한 코드는 다음 네 클래스로 구성되어 있다.

```text
Word
    단어 데이터와 값 검증

WordsDAO
    MySQL 연결과 SQL 실행

WordsService
    단어장의 기능 처리

Menu
    메뉴 출력과 사용자 입력
```

> 아래 코드는 노트북의 구조와 메서드 이름을 최대한 유지했다. 데이터베이스 비밀번호만 `<PASSWORD>`로 변경했다.

---

## 1. mysqlclient 불러오기

```python
import MySQLdb
```

`mysqlclient` 패키지는 Python 코드에서 `MySQLdb`라는 이름으로 사용한다.

```bash
python -m pip install mysqlclient
```

---

## 2. Word 클래스

`Word` 클래스는 영어 단어, 한글 뜻, 레벨을 하나의 객체로 표현한다.

```python
class Word:
    def __init__(self, eng, kor, lev=1):
        self.eng = eng
        self.kor = kor
        self.lev = lev

    def __repr__(self):
        return f"Word(eng='{self.eng}', kor={self.kor}, lev={self.lev})"

    @property
    def eng(self):
        return self.__eng

    @eng.setter
    def eng(self, eng):
        if not eng:
            raise ValueError("영어 단어는 비워둘 수 없습니다")

        self.__eng = eng

    @property
    def kor(self):
        return self.__kor

    @kor.setter
    def kor(self, kor):
        if not kor:
            raise ValueError("뜻을 비워둘 수 없습니다")

        self.__kor = kor

    @property
    def lev(self):
        return self.__lev

    @lev.setter
    def lev(self, lev):
        lev = int(lev)

        if lev < 1:
            raise ValueError("레벨은 1 이상이어야 합니다")

        self.__lev = lev
```

### 생성자

```python
def __init__(self, eng, kor, lev=1):
    self.eng = eng
    self.kor = kor
    self.lev = lev
```

`lev`를 입력하지 않으면 기본값 `1`을 사용한다.

```python
word1 = Word("apple", "사과")
word2 = Word("avocado", "아보카도", 2)
```

### property와 setter

각 속성에 값을 저장할 때 setter가 자동으로 호출된다.

```text
self.eng = eng → eng setter 실행
self.kor = kor → kor setter 실행
self.lev = lev → lev setter 실행
```

영어 단어나 뜻이 비어 있으면 오류를 발생시킨다.

```python
Word("", "사과", 1)
```

```text
ValueError: 영어 단어는 비워둘 수 없습니다
```

레벨은 정수로 변환한 뒤 1 이상인지 확인한다.

```python
Word("apple", "사과", 0)
```

```text
ValueError: 레벨은 1 이상이어야 합니다
```

---

## 3. WordsDAO 클래스

DAO(Data Access Object)는 데이터베이스 접근을 담당하는 객체이다.

```python
class WordsDAO:
    def __init__(self):
        self.db = None

    def connect(self):
        self.db = MySQLdb.connect(
            host='localhost',
            user='apple',
            password='<PASSWORD>',
            db='ai',
            charset='utf8'
        )

    def disconnect(self):
        if self.db:
            self.db.close()

    def insert(self, word):
        self.connect()
        cur = self.db.cursor()

        sql = "insert into voca (eng, kor, lev) values (%s, %s, %s)"
        data = (word.eng, word.kor, word.lev)

        cur.execute(sql, data)
        self.db.commit()
        cur.close()
        self.disconnect()

    def select_all(self):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        sql = "select eng, kor, lev from voca order by eng asc"
        cur.execute(sql)
        rows = cur.fetchall()

        cur.close()
        self.disconnect()

        return rows

    def search_all(self, eng):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        sql = """
        select eng, kor, lev
        from voca
        where eng like concat('%%', %s, '%%')
        """

        cur.execute(sql, (eng,))
        rows = cur.fetchall()

        cur.close()
        self.disconnect()

        return rows

    def search(self, eng):
        self.connect()
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        sql = "select eng, kor, lev from voca where eng=%s"
        cur.execute(sql, (eng,))
        row = cur.fetchone()

        cur.close()
        self.disconnect()

        return row

    def update(self, word):
        self.connect()
        cur = self.db.cursor()

        sql = "update voca set kor=%s, lev=%s where eng =%s"
        data = (word.kor, word.lev, word.eng)
        result = cur.execute(sql, data)

        self.db.commit()
        cur.close()
        self.disconnect()

        return result

    def delete(self, eng):
        self.connect()
        cur = self.db.cursor()

        sql = "delete from voca where eng=%s"
        result = cur.execute(sql, (eng,))

        self.db.commit()
        cur.close()
        self.disconnect()

        return result
```

---

## 4. connect()와 disconnect()

### connect()

```python
def connect(self):
    self.db = MySQLdb.connect(
        host='localhost',
        user='apple',
        password='<PASSWORD>',
        db='ai',
        charset='utf8'
    )
```

MySQL에 연결한 Connection 객체를 `self.db`에 저장한다.

### disconnect()

```python
def disconnect(self):
    if self.db:
        self.db.close()
```

Connection이 존재하면 연결을 닫는다.

연결 테스트:

```python
dao = WordsDAO()
dao.connect()
dao.disconnect()
```

> 실제 프로젝트에서는 비밀번호를 코드에 직접 작성하지 않고 환경변수로 분리하는 것이 안전하다.

---

## 5. 단어 등록: insert()

```python
def insert(self, word):
    self.connect()
    cur = self.db.cursor()

    sql = "insert into voca (eng, kor, lev) values (%s, %s, %s)"
    data = (word.eng, word.kor, word.lev)

    cur.execute(sql, data)
    self.db.commit()
    cur.close()
    self.disconnect()
```

`Word` 객체의 속성을 튜플로 만들어 `INSERT` 문에 전달한다.

```text
Word 객체
    ↓
(eng, kor, lev)
    ↓
INSERT 실행
    ↓
commit()
```

---

## 6. 전체 단어 조회: select_all()

```python
def select_all(self):
    self.connect()
    cur = self.db.cursor(MySQLdb.cursors.DictCursor)

    sql = "select eng, kor, lev from voca order by eng asc"
    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    self.disconnect()

    return rows
```

영어 단어를 기준으로 오름차순 정렬한다.

```sql
order by eng asc
```

DictCursor를 사용하므로 결과는 다음처럼 컬럼명으로 접근할 수 있다.

```python
word['eng']
word['kor']
word['lev']
```

---

## 7. 포함 검색: search_all()

```python
def search_all(self, eng):
    self.connect()
    cur = self.db.cursor(MySQLdb.cursors.DictCursor)

    sql = """
    select eng, kor, lev
    from voca
    where eng like concat('%%', %s, '%%')
    """

    cur.execute(sql, (eng,))
    rows = cur.fetchall()

    cur.close()
    self.disconnect()

    return rows
```

`LIKE`와 `%`를 사용해 입력한 문자열이 포함된 모든 단어를 조회한다.

```text
검색어: app

검색 가능:
apple
application
pineapple
```

Python DB API에서 `%`가 매개변수 표시에 사용되기 때문에 SQL 문자열 안의 `%`를 `%%`로 작성했다.

---

## 8. 정확히 일치하는 단어 검색: search()

```python
def search(self, eng):
    self.connect()
    cur = self.db.cursor(MySQLdb.cursors.DictCursor)

    sql = "select eng, kor, lev from voca where eng=%s"
    cur.execute(sql, (eng,))
    row = cur.fetchone()

    cur.close()
    self.disconnect()

    return row
```

수정과 삭제를 실행하기 전에 단어가 존재하는지 확인할 때 사용한다.

```text
search_all("app") → 문자열을 포함하는 여러 단어
search("apple")   → 정확히 일치하는 단어 하나
```

---

## 9. 단어 수정: update()

```python
def update(self, word):
    self.connect()
    cur = self.db.cursor()

    sql = "update voca set kor=%s, lev=%s where eng =%s"
    data = (word.kor, word.lev, word.eng)
    result = cur.execute(sql, data)

    self.db.commit()
    cur.close()
    self.disconnect()

    return result
```

영어 단어를 기준으로 뜻과 레벨을 수정한다.

`result`에는 영향을 받은 행의 개수가 저장된다.

---

## 10. 단어 삭제: delete()

```python
def delete(self, eng):
    self.connect()
    cur = self.db.cursor()

    sql = "delete from voca where eng=%s"
    result = cur.execute(sql, (eng,))

    self.db.commit()
    cur.close()
    self.disconnect()

    return result
```

값이 하나인 튜플은 반드시 쉼표를 붙인다.

```python
(eng,)
```

---

## 11. WordsService 클래스

Service 클래스는 사용자 입력을 받고 DAO 메서드를 호출한다.

```python
class WordsService:
    def __init__(self):
        self.dao = WordsDAO()

    def insert_word(self):
        eng = input("단어를 입력하세요: ")
        kor = input("뜻을 입력하세요: ")
        lev = input("레벨을 입력하세요: ")

        word = Word(eng, kor, lev)
        self.dao.insert(word)

        print("단어가 등록되었습니다")

    def pirnt_all(self):
        words = self.dao.select_all()

        if not words:
            print("등록된 단어가 없습니다")
            return

        for word in words:
            print(
                f"{word['eng']}, "
                f"뜻:{word['kor']}, "
                f"레벨:{word['lev']}"
            )

    def search_words(self):
        eng = input("검색할 단어를 입력하세요: ")
        words = self.dao.search_all(eng)

        if not words:
            print("찾는 단어가 없습니다")
            return

        for word in words:
            print(
                f"{word['eng']}, "
                f"뜻:{word['kor']}, "
                f"레벨:{word['lev']}"
            )

    def edit_word(self):
        eng = input("수정할 단어를 입력하세요: ")
        word = self.dao.search(eng)

        if not word:
            print("수정할 단어가 없습니다")
            return

        kor = input("새로운 뜻을 입력하세요: ")
        lev = input("새로운 레벨을 입력하세요: ")
        word = Word(eng, kor, lev)
        result = self.dao.update(word)

        if result > 0:
            print("수정되었습니다")
        else:
            print("수정 실패했습니다.")

    def delete_word(self):
        eng = input("삭제할 단어를 입력하세요: ")
        word = self.dao.search(eng)

        if not word:
            print("삭제할 단어가 없습니다")
            return

        result = self.dao.delete(eng)

        if result > 0:
            print("삭제되었습니다")
        else:
            print("삭제 실패했습니다")
```

### 원본 코드의 메서드 이름

노트북에서는 전체 출력 메서드가 다음처럼 작성되어 있다.

```text
def pirnt_all(self):
```

`print`의 철자가 `pirnt`로 작성되었지만 `Menu`에서도 같은 이름으로 호출하므로 현재 코드에서는 동작한다.

```python
self.service.pirnt_all()
```

가독성을 위해 이후에는 `print_all()`로 이름을 수정하는 것이 좋다.

---

## 12. 단어 등록 과정

```python
def insert_word(self):
    eng = input("단어를 입력하세요: ")
    kor = input("뜻을 입력하세요: ")
    lev = input("레벨을 입력하세요: ")

    word = Word(eng, kor, lev)
    self.dao.insert(word)

    print("단어가 등록되었습니다")
```

실행 흐름:

```text
사용자 입력
    ↓
Word 객체 생성
    ↓
setter에서 값 검증
    ↓
WordsDAO.insert()
    ↓
MySQL에 저장
```

---

## 13. 전체 단어 출력 과정

```python
def pirnt_all(self):
    words = self.dao.select_all()

    if not words:
        print("등록된 단어가 없습니다")
        return

    for word in words:
        print(
            f"{word['eng']}, "
            f"뜻:{word['kor']}, "
            f"레벨:{word['lev']}"
        )
```

DAO가 반환한 딕셔너리에서 컬럼명으로 값을 꺼낸다.

---

## 14. 단어 검색 과정

```python
def search_words(self):
    eng = input("검색할 단어를 입력하세요: ")
    words = self.dao.search_all(eng)

    if not words:
        print("찾는 단어가 없습니다")
        return

    for word in words:
        print(
            f"{word['eng']}, "
            f"뜻:{word['kor']}, "
            f"레벨:{word['lev']}"
        )
```

포함 검색이므로 일부 문자열만 입력해도 관련 단어를 모두 조회할 수 있다.

---

## 15. 단어 수정 과정

```python
def edit_word(self):
    eng = input("수정할 단어를 입력하세요: ")
    word = self.dao.search(eng)

    if not word:
        print("수정할 단어가 없습니다")
        return

    kor = input("새로운 뜻을 입력하세요: ")
    lev = input("새로운 레벨을 입력하세요: ")
    word = Word(eng, kor, lev)
    result = self.dao.update(word)

    if result > 0:
        print("수정되었습니다")
    else:
        print("수정 실패했습니다.")
```

먼저 `search()`로 단어의 존재 여부를 확인한 뒤 새로운 `Word` 객체를 만들어 수정한다.

---

## 16. 단어 삭제 과정

```python
def delete_word(self):
    eng = input("삭제할 단어를 입력하세요: ")
    word = self.dao.search(eng)

    if not word:
        print("삭제할 단어가 없습니다")
        return

    result = self.dao.delete(eng)

    if result > 0:
        print("삭제되었습니다")
    else:
        print("삭제 실패했습니다")
```

삭제 전 `search()`를 호출해 단어가 실제로 존재하는지 확인한다.

---

## 17. Menu 클래스

```python
class Menu:
    def __init__(self):
        self.service = WordsService()

    def run(self):
        while True:
            try:
                print()
                print("=====단어장=====")
                print("1. 등록하기")
                print("2. 출력하기")
                print("3. 검색하기")
                print("4. 수정하기")
                print("5. 삭제하기")
                print("6. 종료하기")

                menu = int(input("메뉴를 선택하세요"))

                if menu == 1:
                    print("단어를 등록합니다")
                    self.service.insert_word()
                elif menu == 2:
                    print("단어를 출력합니다")
                    self.service.pirnt_all()
                elif menu == 3:
                    print("단어를 검색합니다")
                    self.service.search_words()
                elif menu == 4:
                    print("단어를 수정합니다")
                    self.service.edit_word()
                elif menu == 5:
                    print("단어를 삭제합니다")
                    self.service.delete_word()
                elif menu == 6:
                    print("프로그램을 종료합니다")
                    break
                else:
                    print("메뉴는 1부터 6까지 입력하세요")
            except Exception as e:
                print("오류 : ", e)
                print("다시 입력하세요")
```

Menu 클래스는 메뉴 번호에 따라 Service 메서드를 호출한다.

```text
1 → insert_word()
2 → pirnt_all()
3 → search_words()
4 → edit_word()
5 → delete_word()
6 → 종료
```

`int(input())`에서 숫자가 아닌 값을 입력하거나 데이터베이스 오류가 발생하면 `except`에서 처리한다.

---

## 18. 프로그램 실행

```python
menu = Menu()
menu.run()
```

실행 예시:

```text
=====단어장=====
1. 등록하기
2. 출력하기
3. 검색하기
4. 수정하기
5. 삭제하기
6. 종료하기
메뉴를 선택하세요: 2

단어를 출력합니다
apple, 뜻:사과, 레벨:1
avocado, 뜻:아보카도, 레벨:2
banana, 뜻:바나나, 레벨:1
melon, 뜻:메로나, 레벨:2
orange, 뜻:오렌지, 레벨:1
```

삭제 실행 예시:

```text
메뉴를 선택하세요: 5
단어를 삭제합니다
삭제할 단어를 입력하세요: melon
삭제되었습니다
```

삭제 후 전체 출력을 실행하면 `melon`이 사라진 것을 확인할 수 있다.

---

## 19. 클래스 간 동작 흐름

단어를 등록할 때 각 클래스는 다음 순서로 동작한다.

```text
Menu
    ↓ insert_word() 호출
WordsService
    ↓ Word 객체 생성
Word
    ↓ 값 검증
WordsDAO
    ↓ INSERT 실행
MySQL voca 테이블
```

전체 단어를 출력할 때는 다음 순서로 동작한다.

```text
Menu
    ↓ pirnt_all() 호출
WordsService
    ↓ select_all() 호출
WordsDAO
    ↓ SELECT 실행
MySQL
    ↓ 조회 결과 반환
WordsService
    ↓ 결과 출력
사용자
```

---

## 20. 원본 코드를 사용할 때 주의할 점

### 예외 발생 시 연결 종료

현재 DAO 코드는 SQL 실행 중 예외가 발생하면 `cur.close()`와 `disconnect()`까지 도달하지 못할 수 있다.

원본 구조를 유지하면서 개선하려면 `try-finally`를 사용할 수 있다.

```python
def insert(self, word):
    self.connect()
    cur = self.db.cursor()

    try:
        sql = "insert into voca (eng, kor, lev) values (%s, %s, %s)"
        data = (word.eng, word.kor, word.lev)
        cur.execute(sql, data)
        self.db.commit()
    except Exception:
        self.db.rollback()
        raise
    finally:
        cur.close()
        self.disconnect()
```

### 너무 넓은 예외 처리

Menu의 `except Exception`은 모든 오류를 한 번에 처리한다. 학습 단계에서는 편리하지만 실제 프로그램에서는 입력 오류와 데이터베이스 오류를 구분하는 것이 좋다.

### 연결 반복

각 DAO 메서드가 실행될 때마다 MySQL 연결을 열고 닫는다. 작은 프로그램에서는 이해하기 쉽지만 요청이 많은 프로그램에서는 Connection Pool을 고려할 수 있다.

### 비밀번호 노출

데이터베이스 비밀번호는 코드나 블로그에 공개하지 않는다. 환경변수나 별도 설정 파일을 사용한다.

---

## 21. 핵심 정리

| 클래스 | 역할 |
| --- | --- |
| `Word` | 단어 데이터를 저장하고 검증 |
| `WordsDAO` | MySQL 연결과 CRUD SQL 실행 |
| `WordsService` | 사용자 입력과 단어장 기능 처리 |
| `Menu` | 메뉴 출력과 기능 선택 |

이 프로젝트에서 사용하는 CRUD 메서드는 다음과 같다.

| 기능 | DAO 메서드 | SQL |
| --- | --- | --- |
| 등록 | `insert()` | `INSERT` |
| 전체 조회 | `select_all()` | `SELECT` |
| 포함 검색 | `search_all()` | `SELECT ... LIKE` |
| 단일 검색 | `search()` | `SELECT ... WHERE` |
| 수정 | `update()` | `UPDATE` |
| 삭제 | `delete()` | `DELETE` |

원본 프로그램은 객체지향 구조와 데이터베이스 CRUD를 함께 연습할 수 있는 예제이다. `Word`, DAO, Service, Menu의 역할을 구분해서 보면 프로그램 전체 흐름을 더 쉽게 이해할 수 있다.
