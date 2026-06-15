# Python과 MySQL 연동하기

Python에서 MySQL 데이터베이스에 접속하고 데이터를 조회·삽입·수정·삭제하는 과정을 정리한다.

이번 실습에서는 `mysqlclient` 라이브러리를 사용한다. 설치하는 패키지 이름은 `mysqlclient`이지만, Python 코드에서는 `MySQLdb`라는 이름으로 불러온다.

> 아래 코드는 수업에서 작성한 코드를 최대한 유지했다. 실제 비밀번호만 `<PASSWORD>`로 변경했다.

---

## 1. mysqlclient

`mysqlclient`는 Python에서 MySQL 데이터베이스와 상호작용할 때 사용하는 라이브러리이다.

```bash
python -m pip install mysqlclient
```

설치 후 다음과 같이 불러온다.

```python
import MySQLdb
```

Python에서 MySQL을 사용할 때 `PyMySQL`, `mysqlclient` 등을 많이 사용한다. 두 라이브러리의 사용법은 비슷하지만, `mysqlclient`는 C 기반으로 구현되어 빠른 성능을 제공한다.

---

## 2. MySQL 접속

`MySQLdb.connect()`를 사용해 데이터베이스에 접속한다.

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

db
```

출력 예시:

```text
<_mysql.connection open to 'localhost' at 0x...>
```

매개변수의 의미는 다음과 같다.

| 매개변수 | 설명 |
| --- | --- |
| `host` | MySQL 서버 주소 |
| `user` | MySQL 사용자명 |
| `password` | MySQL 비밀번호 |
| `db` | 사용할 데이터베이스 |

한글 데이터를 안정적으로 처리하려면 `charset`을 추가할 수 있다.

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai',
    charset='utf8mb4'
)
```

실제 프로젝트에서는 비밀번호를 코드에 직접 작성하지 않고 환경변수나 설정 파일로 분리해야 한다.

---

## 3. Cursor 생성

Cursor는 SQL 문을 실행하고 결과를 가져오는 작업 객체이다.

```python
cur = db.cursor()
cur.execute("select * from member")
```

출력 예시:

```text
7
```

`execute()`가 반환하는 숫자는 조회되거나 영향을 받은 행의 개수이다.

```text
Connection
    └── Cursor
          ├── SQL 실행
          └── 결과 조회
```

하나의 Connection에서도 필요에 따라 Cursor를 생성할 수 있다. Cursor 사용이 끝나면 `close()`로 닫아야 한다.

---

## 4. SQL 결과 가져오기

Cursor로 `SELECT` 문을 실행한 뒤 fetch 메서드로 결과를 가져온다.

| 메서드 | 설명 |
| --- | --- |
| `fetchall()` | 남아 있는 모든 행을 가져온다 |
| `fetchone()` | 다음 행 하나를 가져온다 |
| `fetchmany(size)` | 지정한 개수만큼 가져온다 |

### 4.1 fetchall()

```python
data = cur.fetchall()
data
```

출력 결과는 여러 튜플을 담은 튜플 형태이다.

```text
(
    (1, 'apple', '1111', '김사과', ...),
    (2, 'banana', '2222', '반하나', ...),
    ...
)
```

`fetchall()`은 모든 결과를 한 번에 가져오므로 데이터가 매우 많으면 메모리 사용량이 커질 수 있다.

### Cursor의 결과는 소비된다

같은 Cursor에서 다시 `fetchall()`을 실행하면 빈 튜플이 반환된다.

```python
data = cur.fetchall()
data
```

출력:

```text
()
```

첫 번째 `fetchall()` 호출에서 모든 결과를 이미 가져왔기 때문이다. 다시 조회하려면 `execute()`를 다시 호출해야 한다.

```python
cur.execute("select * from member")
data = cur.fetchall()
```

### 4.2 fetchone()

필요한 컬럼만 조회한다.

```python
cur.execute("select userid, name, gender from member")
```

첫 번째 행:

```python
row = cur.fetchone()
row
```

```text
('apple', '김사과', '여자')
```

다시 호출하면 다음 행을 가져온다.

```python
row = cur.fetchone()
row
```

```text
('banana', '반하나', '여자')
```

```python
row = cur.fetchone()
row
```

```text
('orange', '오렌지', '남자')
```

`fetchone()`은 호출할 때마다 Cursor 위치가 다음 행으로 이동한다.

---

## 5. fetchone()으로 전체 결과 순회

```python
sql = "select userid, name, gender, hp from member"
cur.execute(sql)
```

반복문을 사용해 한 행씩 가져올 수 있다.

```python
while True:
    row = cur.fetchone()

    if row:
        print(row)
    else:
        break
```

출력 예시:

```text
('apple', '김사과', '여자', '010-1111-1111')
('banana', '반하나', '여자', '010-2222-2222')
('orange', '오렌지', '남자', '010-3333-3333')
```

> 노트북의 실행 결과가 `banana`부터 시작했다면, 같은 Cursor에서 이전에 한 행을 이미 가져온 상태였기 때문이다. SQL을 다시 실행하면 첫 번째 행부터 가져온다.

---

## 6. 딕셔너리 형태로 결과 반환

기본 Cursor는 결과를 튜플로 반환한다. `DictCursor`를 사용하면 컬럼명을 key로 가진 딕셔너리 형태로 결과를 받을 수 있다.

```python
cur = db.cursor(MySQLdb.cursors.DictCursor)
cur.execute(sql)

result = cur.fetchall()
result
```

출력 예시:

```text
(
    {
        'userid': 'apple',
        'name': '김사과',
        'gender': '여자',
        'hp': '010-1111-1111'
    },
    {
        'userid': 'banana',
        'name': '반하나',
        'gender': '여자',
        'hp': '010-2222-2222'
    }
)
```

컬럼명으로 값에 접근할 수 있다.

```python
cur.execute(sql)

while True:
    row = cur.fetchone()

    if row:
        print(
            f"아이디:{row['userid']}, "
            f"이름:{row['name']}, "
            f"성별:{row['gender']}, "
            f"전화번호:{row['hp']}"
        )
    else:
        break
```

출력 예시:

```text
아이디:apple, 이름:김사과, 성별:여자, 전화번호:010-1111-1111
아이디:banana, 이름:반하나, 성별:여자, 전화번호:010-2222-2222
```

튜플의 인덱스를 사용하는 것보다 데이터의 의미를 파악하기 쉽다.

---

## 7. Cursor와 Connection 닫기

데이터베이스 작업이 끝나면 Cursor와 Connection을 닫는다.

```python
cur.close()
db.close()
```

종료 순서는 일반적으로 다음과 같다.

```text
SQL 작업 완료
    ↓
Cursor 닫기
    ↓
Connection 닫기
```

---

# 데이터 삽입하기

## 8. 데이터베이스 연결

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()
```

---

## 9. execute()로 한 행 삽입

```python
sql = """
insert into member (
    userid, userpw, name, hp,
    email, gender, ssn1, ssn2
)
values (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = (
    'mango',
    '8888',
    '마앙고',
    '010-8888-8888',
    'mango@mango.com',
    '남자',
    '000000',
    '0000000'
)

cur.execute(sql, data)
db.commit()
```

SQL 안에 값을 직접 연결하지 않고 `%s` 자리에 데이터를 별도로 전달한다.

```python
cur.execute(sql, data)
```

이 방식은 SQL Injection을 방지하고 문자열 따옴표 처리를 안전하게 해준다.

`INSERT`, `UPDATE`, `DELETE`처럼 데이터를 변경하는 SQL을 실행한 뒤에는 `commit()`이 필요하다.

---

## 10. executemany()로 여러 행 삽입

```python
sql = """
insert into member (
    userid, userpw, name, hp,
    email, gender, ssn1, ssn2
)
values (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = [
    (
        'pear',
        '9999',
        '배철수',
        '010-9999-9999',
        'pear@pear.com',
        '남자',
        '000000',
        '0000000'
    ),
    (
        'peach',
        '0000',
        '복숭아',
        '010-0000-0000',
        'peach@peach.com',
        '남자',
        '000000',
        '0000000'
    )
]

cur.executemany(sql, data)
db.commit()
```

`executemany()`는 하나의 SQL에 여러 데이터 묶음을 적용할 때 사용한다.

```text
execute()     → 데이터 한 건 처리
executemany() → 데이터 여러 건 처리
```

작업 후 연결을 종료한다.

```python
cur.close()
db.close()
```

---

# 회원가입 프로그램

## 11. 공백으로 회원정보 입력받기

```python
sql = """
insert into member (
    userid, userpw, name, hp, email,
    ssn1, ssn2, zipcode,
    address1, address2, address3, gender
)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()

print("회원가입 프로그램")

while True:
    data = tuple(input("회원 정보를 입력하세요 :").split())
    cur.execute(sql, data)
    db.commit()

    cmd = input("회원가입을 추가로 하시겠습니까? (Y/N)")

    if cmd == "N":
        print("회원가입 프로그램을 종료하겠습니다")
        break
    else:
        continue

cur.close()
db.close()
```

이 방식은 코드가 짧지만 주소처럼 공백이 들어가는 값을 정확하게 구분하기 어렵다. 또한 정확히 12개 값을 입력하지 않으면 오류가 발생한다.

---

## 12. 항목별로 회원정보 입력받기

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()

while True:
    try:
        userid = input('아이디를 입력하세요: ')
        userpw = input('비밀번호를 입력하세요: ')
        name = input('이름을 입력하세요: ')
        hp = input('전화번호를 입력하세요: ')
        email = input('이메일을 입력하세요: ')
        ssn1 = input('주민등록번호 앞자리를 입력하세요: ')
        ssn2 = input('주민등록번호 뒷자리를 입력하세요: ')
        zipcode = input('우편번호를 입력하세요: ')
        address1 = input('주소를 입력하세요: ')
        address2 = input('상세주소를 입력하세요: ')
        address3 = input('참고사항 입력하세요: ')
        gender = input('성별을 입력하세요(남자 또는 여자): ')

        sql = """
        insert into member (
            userid, userpw, name, hp, email,
            gender, ssn1, ssn2, zipcode,
            address1, address2, address3
        )
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            userid, userpw, name, hp, email,
            gender, ssn1, ssn2, zipcode,
            address1, address2, address3
        )

        cur.execute(sql, data)
        db.commit()
        print('가입되었습니다!')

        yn = input('추가로 가입하시겠습니까? (y/n): ')

        if yn.lower() == 'n':
            print('프로그램을 종료합니다')
            break
    except Exception as e:
        print('다시 입력하세요')

cur.close()
db.close()
```

원본 구조를 유지했지만 실무에서는 다음처럼 오류 내용을 함께 확인하고 `rollback()`을 호출하는 것이 좋다.

```text
except Exception as e:
    db.rollback()
    print('다시 입력하세요:', e)
```

> 주민등록번호와 비밀번호는 매우 민감한 정보이다. 실제 서비스에서는 평문으로 저장해서는 안 되며, 수집 범위와 암호화 정책도 검토해야 한다.

---

# 로그인 프로그램

## 13. 아이디와 비밀번호 확인

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()

sql = "select userid, name from member"
cur.execute(sql)

userid = input("아이디를 입력하세요.")
userpw = input("비밀번호를 입력하세요.")

sql = "select idx from member where userid=%s and userpw=%s"
data = (userid, userpw)
result = cur.execute(sql, data)

if result > 0:
    print("로그인에 성공했습니다")
else:
    print("아이디 또는 비밀번호를 확인하세요.")

cur.close()
db.close()
```

`execute()`가 반환한 행의 개수가 1 이상이면 아이디와 비밀번호가 일치하는 회원이 있다는 뜻이다.

### 문자열 결합 방식의 문제

노트북에는 SQL 문자열 연결을 비교하는 코드도 포함되어 있다.

```python
sql = "select idx from member where userid=%s and userpw=%s"

sql = (
    "select idx from member where userid'"
    + userid
    + "' and userpw'"
    + userpw
    + "'"
)
```

두 번째 방식은 SQL 문법도 정확하지 않고 SQL Injection에 취약하다. 첫 번째처럼 매개변수 바인딩을 사용해야 한다.

```python
cur.execute(sql, (userid, userpw))
```

---

# 회원정보 수정

## 14. UPDATE 실행

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()

while True:
    try:
        userid = input('변경할 아이디를 입력하세요: ')
        name = input('이름을 입력하세요: ')
        hp = input('전화번호를 입력하세요: ')
        email = input('이메일을 입력하세요: ')
        ssn1 = input('주민등록번호 앞자리를 입력하세요: ')
        ssn2 = input('주민등록번호 뒷자리를 입력하세요: ')
        zipcode = input('우편번호를 입력하세요: ')
        address1 = input('주소를 입력하세요: ')
        address2 = input('상세주소를 입력하세요: ')
        address3 = input('참고사항 입력하세요: ')
        gender = input('성별을 입력하세요(남자 또는 여자): ')

        sql = """
        update member
        set name=%s,
            hp=%s,
            email=%s,
            ssn1=%s,
            ssn2=%s,
            zipcode=%s,
            address1=%s,
            address2=%s,
            address3=%s,
            gender=%s
        where userid=%s
        """

        data = (
            name, hp, email, ssn1, ssn2,
            zipcode, address1, address2,
            address3, gender, userid
        )

        result = cur.execute(sql, data)
        db.commit()

        if result > 0:
            print('변경되었습니다')
        else:
            print('오류')

        yn = input('추가로 변경하시겠습니까? (y/n): ')

        if yn.lower() == 'n':
            print('프로그램을 종료합니다')
            break
    except Exception as e:
        print('다시 입력하세요')

cur.close()
db.close()
```

`UPDATE`의 `execute()` 결과는 변경의 영향을 받은 행의 개수이다.

```text
result > 0 → 변경된 회원이 있음
result == 0 → 조건에 맞는 회원이 없거나 값이 동일함
```

---

# 회원 탈퇴

## 15. DELETE 실행

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()

while True:
    try:
        userid = input('삭제할 아이디를 입력하세요: ')
        sql = "delete from member where userid = %s"
        data = (userid,)
        result = cur.execute(sql, data)
        db.commit()

        if result > 0:
            print("아이디가 삭제되었습니다")
        else:
            print("오류")

        yn = input('추가로 삭제하시겠습니까? (y/n): ')

        if yn.lower() == 'n':
            print('프로그램을 종료합니다')
            break
    except Exception as e:
        print('다시 입력하세요')

cur.close()
db.close()
```

값이 한 개인 튜플은 쉼표가 필요하다.

```python
data = (userid,)
```

쉼표가 없으면 튜플이 아니라 단순한 문자열이 된다.

간단한 회원 탈퇴 코드는 다음과 같다.

```python
db = MySQLdb.connect(
    host='localhost',
    user='root',
    password='<PASSWORD>',
    db='ai'
)

cur = db.cursor()

userid = input('탈퇴할 아이디를 입력하세요: ')
sql = 'delete from member where userid=%s'
result = cur.execute(sql, (userid,))
db.commit()

if result > 0:
    print('탈퇴되었습니다')
else:
    print('오류')

cur.close()
db.close()
```

---

## 16. CRUD 흐름 정리

| 기능 | SQL | Python 메서드 |
| --- | --- | --- |
| 조회 | `SELECT` | `execute()` + fetch 메서드 |
| 삽입 | `INSERT` | `execute()` 또는 `executemany()` |
| 수정 | `UPDATE` | `execute()` + `commit()` |
| 삭제 | `DELETE` | `execute()` + `commit()` |

전체 흐름은 다음과 같다.

```text
MySQL 연결
    ↓
Cursor 생성
    ↓
SQL과 데이터 준비
    ↓
execute() 실행
    ↓
SELECT: fetch로 결과 조회
DML: commit으로 변경 확정
    ↓
Cursor와 Connection 종료
```

---

## 17. 실습 코드에서 기억할 점

1. `fetchall()`이나 `fetchone()`을 호출하면 Cursor의 결과가 소비된다.
2. SQL과 사용자 입력값을 문자열로 직접 결합하지 않는다.
3. SQL의 값은 `%s`와 `execute(sql, data)`로 전달한다.
4. 데이터 변경 후에는 `commit()`이 필요하다.
5. 오류가 발생하면 `rollback()`을 고려한다.
6. Cursor와 Connection은 작업 후 닫는다.
7. 비밀번호와 주민등록번호 같은 민감정보는 코드나 블로그에 공개하지 않는다.
8. 실제 서비스에서는 비밀번호를 안전한 방식으로 해싱해야 한다.

`mysqlclient`를 사용하면 Python 코드에서 SQL을 직접 실행할 수 있다. 핵심은 연결, Cursor, 결과 조회, 트랜잭션, 자원 종료의 흐름을 정확히 이해하는 것이다.
