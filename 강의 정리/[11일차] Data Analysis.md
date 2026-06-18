# [11일차] Data Analysis

## 1. 데이터베이스 확인하기

현재 MySQL 서버에 존재하는 데이터베이스 목록을 확인할 때 사용한다.

```sql
-- 현재 서버에 존재하는 데이터베이스 목록 확인
SHOW DATABASES;
```

출력 예시:

```text
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

## 2. 데이터베이스 생성하기

새로운 데이터베이스를 만들 때는 `CREATE DATABASE`를 사용한다.

```sql
-- ai라는 이름의 데이터베이스 생성
CREATE DATABASE ai;
```

주의:

- 이미 같은 이름의 데이터베이스가 있으면 오류가 발생할 수 있다.
- 실무에서는 보통 다음처럼 작성하기도 한다.

```sql
-- ai 데이터베이스가 없을 때만 생성
CREATE DATABASE IF NOT EXISTS ai;
```

## 3. 데이터베이스 선택하기

테이블을 만들거나 데이터를 조작하려면 먼저 사용할 데이터베이스를 선택해야 한다.

```sql
-- ai 데이터베이스 사용
USE ai;
```

이후 실행하는 `CREATE TABLE`, `INSERT`, `SELECT` 등의 명령은 기본적으로 `ai` 데이터베이스 안에서 실행된다.

## 4. 테이블이란?

테이블은 데이터를 행과 열로 저장하는 구조이다.

엑셀 표처럼 생각하면 이해하기 쉽다.

| 용어 | 의미 |
| --- | --- |
| 테이블 | 데이터를 저장하는 표 |
| 행, Row, Record | 실제 데이터 한 줄 |
| 열, Column, Field | 데이터의 항목 |
| 스키마 | 테이블의 구조와 제약조건 |

예를 들어 회원 정보를 저장하는 `member` 테이블은 다음과 같은 구조를 가질 수 있다.

| idx | userid | userpw | name | hp | email |
| ---: | --- | --- | --- | --- | --- |
| 1 | apple | 1234 | 김사과 | 010-1111-1111 | apple@example.com |
| 2 | banana | 1234 | 반하나 | 010-2222-2222 | banana@example.com |

## 5. 테이블 생성 기본 형식

테이블은 `CREATE TABLE` 명령어로 만든다.

기본 형식:

```sql
CREATE TABLE 테이블명 (
    컬럼명1 데이터타입 제약조건,
    컬럼명2 데이터타입 제약조건,
    컬럼명3 데이터타입 제약조건
);
```

예시:

```sql
CREATE TABLE member (
    idx INT AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(20) UNIQUE NOT NULL,
    userpw VARCHAR(20) NOT NULL
);
```

위 예시는 `member`라는 테이블을 만들고, `idx`, `userid`, `userpw` 컬럼을 생성한다.

## 6. 스키마란?

스키마는 데이터베이스나 테이블의 구조와 제약조건을 정의한 명세이다.

쉽게 말해, 테이블이 어떤 모양으로 데이터를 저장할지 정해놓은 설계도이다.

스키마에 포함되는 내용:

- 테이블 이름
- 컬럼 이름
- 컬럼 데이터 타입
- 제약조건
- 기본키
- 외래키
- 기본값

## 7. 데이터 타입

데이터 타입은 컬럼에 어떤 종류의 값을 저장할지 정하는 규칙이다.

## 7.1 정수형

정수 데이터를 저장할 때 사용한다.

| 타입 | 설명 |
| --- | --- |
| `INT` | 일반적인 정수 |
| `BIGINT` | 더 큰 범위의 정수 |

예시:

```sql
point INT DEFAULT 1000
```

설명:

- `point` 컬럼은 정수를 저장한다.
- 값을 입력하지 않으면 기본값으로 `1000`이 들어간다.

## 7.2 실수형

소수점이 있는 숫자를 저장할 때 사용한다.

| 타입 | 설명 |
| --- | --- |
| `FLOAT` | 실수 |
| `DOUBLE` | 더 정밀한 실수 |
| `DECIMAL` | 정확한 소수 계산에 사용 |

예시:

```sql
price DECIMAL(10, 2)
```

설명:

- 전체 10자리 숫자까지 저장할 수 있다.
- 소수점 아래는 2자리까지 저장한다.
- 돈, 가격, 정산 데이터에는 `FLOAT`보다 `DECIMAL`이 더 적합하다.

## 7.3 문자형

문자 데이터를 저장할 때 사용한다.

| 타입 | 설명 |
| --- | --- |
| `CHAR(n)` | 고정 길이 문자열 |
| `VARCHAR(n)` | 가변 길이 문자열 |
| `TEXT` | 긴 문자열 |
| `BINARY` | 고정 길이 바이너리 데이터 |
| `VARBINARY` | 가변 길이 바이너리 데이터 |

예시:

```sql
userid VARCHAR(20) UNIQUE NOT NULL
ssn1 CHAR(6) NOT NULL
```

설명:

- `userid`는 최대 20글자까지 저장할 수 있다.
- `ssn1`은 주민등록번호 앞자리처럼 길이가 정해진 값에 적합하다.
- `CHAR`는 고정 길이, `VARCHAR`는 가변 길이다.

## 7.4 날짜형

날짜와 시간을 저장할 때 사용한다.

| 타입 | 설명 |
| --- | --- |
| `DATE` | 날짜 |
| `TIME` | 시간 |
| `DATETIME` | 날짜와 시간 |
| `TIMESTAMP` | 시간 흐름 기준의 날짜/시간 |

예시:

```sql
regdate DATETIME DEFAULT NOW()
```

설명:

- `regdate`는 회원 가입일 같은 날짜와 시간을 저장한다.
- 값을 직접 넣지 않으면 현재 날짜와 시간이 기본값으로 저장된다.

## 8. 제약조건

제약조건은 데이터의 무결성을 지키기 위해 데이터를 입력하거나 수정할 때 검사하는 규칙이다.

무결성이란 데이터가 정확하고 일관된 상태를 유지하는 것을 의미한다.

## 8.1 `NOT NULL`

`NULL` 값을 허용하지 않는다.

```sql
name VARCHAR(20) NOT NULL
```

설명:

- `name` 컬럼에는 반드시 값이 들어가야 한다.
- 비워두면 오류가 발생한다.

## 8.2 `UNIQUE`

중복 값을 허용하지 않는다.

```sql
userid VARCHAR(20) UNIQUE NOT NULL
```

설명:

- 같은 아이디를 가진 회원이 여러 명 생기지 않도록 막는다.
- `UNIQUE`는 중복은 막지만, 일반적으로 `NULL`은 허용될 수 있다.
- 반드시 값이 있어야 한다면 `NOT NULL`도 함께 사용한다.

## 8.3 `DEFAULT`

값을 입력하지 않았을 때 기본으로 들어갈 값을 설정한다.

```sql
point INT DEFAULT 1000
```

설명:

- `point` 값을 직접 넣지 않으면 자동으로 `1000`이 들어간다.

## 8.4 `PRIMARY KEY`

테이블에서 각 행을 구분하는 대표 컬럼이다.

```sql
idx INT AUTO_INCREMENT PRIMARY KEY
```

특징:

1. `NULL` 값을 허용하지 않는다.
2. 중복 값을 허용하지 않는다.
3. 자동으로 인덱스가 설정된다.
4. 다른 테이블에서 참조할 수 있다.

설명:

- `idx`는 회원 한 명을 구분하기 위한 고유 번호이다.
- 이름이나 아이디보다 숫자 고유번호를 기본키로 자주 사용한다.

## 8.5 `FOREIGN KEY`

다른 테이블의 기본키를 참조하는 키이다.

기본 형식:

```sql
FOREIGN KEY (컬럼명) REFERENCES 참조테이블명(참조컬럼명)
```

예시:

```sql
FOREIGN KEY (member_idx) REFERENCES member(idx)
```

설명:

- 주문 테이블에서 어떤 회원의 주문인지 연결할 때 사용할 수 있다.
- `FOREIGN KEY`는 테이블 간 관계를 만들 때 중요하다.

## 8.6 `AUTO_INCREMENT`

숫자 값을 자동으로 증가시킨다.

```sql
idx INT AUTO_INCREMENT PRIMARY KEY
```

설명:

- 데이터를 추가할 때 `idx` 값을 직접 넣지 않아도 자동으로 1, 2, 3처럼 증가한다.
- 보통 기본키 컬럼에 많이 사용한다.

## 9. 회원 테이블 만들기

아래 SQL은 회원 정보를 저장하는 `member` 테이블을 생성한다.

```sql
CREATE TABLE member (
    idx INT AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(20) UNIQUE NOT NULL,
    userpw VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    hp VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    ssn1 CHAR(6) NOT NULL,
    ssn2 CHAR(7) NOT NULL,
    zipcode VARCHAR(5),
    address1 VARCHAR(100),
    address2 VARCHAR(100),
    address3 VARCHAR(100),
    regdate DATETIME DEFAULT NOW(),
    point INT DEFAULT 1000
);
```

## 9.1 컬럼별 설명

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
| --- | --- | --- | --- |
| `idx` | `INT` | `AUTO_INCREMENT`, `PRIMARY KEY` | 회원 고유 번호 |
| `userid` | `VARCHAR(20)` | `UNIQUE`, `NOT NULL` | 회원 아이디 |
| `userpw` | `VARCHAR(20)` | `NOT NULL` | 비밀번호 |
| `name` | `VARCHAR(20)` | `NOT NULL` | 이름 |
| `hp` | `VARCHAR(20)` | `NOT NULL` | 휴대폰 번호 |
| `email` | `VARCHAR(50)` | `NOT NULL` | 이메일 |
| `ssn1` | `CHAR(6)` | `NOT NULL` | 주민등록번호 앞자리 |
| `ssn2` | `CHAR(7)` | `NOT NULL` | 주민등록번호 뒷자리 |
| `zipcode` | `VARCHAR(5)` | 없음 | 우편번호 |
| `address1` | `VARCHAR(100)` | 없음 | 주소 |
| `address2` | `VARCHAR(100)` | 없음 | 상세주소 |
| `address3` | `VARCHAR(100)` | 없음 | 참고주소 |
| `regdate` | `DATETIME` | `DEFAULT NOW()` | 가입일 |
| `point` | `INT` | `DEFAULT 1000` | 기본 포인트 |

## 10. 테이블 구조 확인하기

테이블이 어떤 컬럼과 타입으로 구성되어 있는지 확인할 때 `DESC`를 사용한다.

```sql
-- member 테이블 구조 확인
DESC member;
```

출력 예시:

```text
+----------+--------------+------+-----+-------------------+----------------+
| Field    | Type         | Null | Key | Default           | Extra          |
+----------+--------------+------+-----+-------------------+----------------+
| idx      | int          | NO   | PRI | NULL              | auto_increment |
| userid   | varchar(20)  | NO   | UNI | NULL              |                |
| userpw   | varchar(20)  | NO   |     | NULL              |                |
| name     | varchar(20)  | NO   |     | NULL              |                |
| point    | int          | YES  |     | 1000              |                |
+----------+--------------+------+-----+-------------------+----------------+
```

## 11. 테이블 삭제하기

테이블 자체를 완전히 삭제할 때는 `DROP TABLE`을 사용한다.

```sql
-- member 테이블 삭제
DROP TABLE member;
```

주의:

- 테이블 구조와 데이터가 모두 삭제된다.
- 복구하기 어렵기 때문에 신중하게 사용해야 한다.

## 12. 컬럼 삭제하기

기존 테이블에서 특정 컬럼을 삭제할 때는 `ALTER TABLE ... DROP`을 사용한다.

```sql
-- member 테이블에서 point 컬럼 삭제
ALTER TABLE member DROP point;
```

설명:

- `member` 테이블 구조에서 `point` 컬럼이 제거된다.
- 해당 컬럼에 저장되어 있던 데이터도 함께 사라진다.

## 13. 컬럼 추가하기

기존 테이블에 새 컬럼을 추가할 때는 `ALTER TABLE ... ADD`를 사용한다.

```sql
-- member 테이블에 point 컬럼 추가
ALTER TABLE member ADD point INT DEFAULT 1000;
```

설명:

- `point`라는 정수형 컬럼을 추가한다.
- 값을 입력하지 않으면 기본값으로 `1000`이 들어간다.

## 14. 컬럼 수정하기

기존 컬럼의 데이터 타입이나 기본값을 수정할 때는 `ALTER TABLE ... MODIFY COLUMN`을 사용한다.

```sql
-- point 컬럼의 기본값을 100으로 수정
ALTER TABLE member MODIFY COLUMN point INT DEFAULT 100;
```

설명:

- `point` 컬럼의 구조를 수정한다.
- 기존 기본값 `1000`을 `100`으로 바꾼다.

## 15. DDL

DDL은 `Database Definition Language`의 약자로, 데이터베이스 객체의 구조를 정의하는 명령어이다.

즉, 데이터베이스나 테이블을 만들고, 수정하고, 삭제할 때 사용한다.

| 명령어 | 의미 | 예시 |
| --- | --- | --- |
| `CREATE` | 데이터베이스, 테이블, 뷰 등을 생성 | `CREATE TABLE member (...);` |
| `ALTER` | 기존 객체의 구조 변경 | `ALTER TABLE member ADD point INT;` |
| `DROP` | 객체를 완전히 삭제 | `DROP TABLE member;` |
| `TRUNCATE` | 테이블의 모든 데이터 삭제, 구조는 유지 | `TRUNCATE TABLE member;` |

## 15.1 `TRUNCATE` 주의점

```sql
TRUNCATE TABLE member;
```

설명:

- 테이블 안의 모든 데이터를 삭제한다.
- 테이블 구조는 남는다.
- 일반적으로 롤백이 어렵기 때문에 신중하게 사용해야 한다.

## 16. DML

DML은 `Data Manipulation Language`의 약자로, 테이블 안의 데이터를 조작하는 명령어이다.

| 명령어 | 의미 | 예시 |
| --- | --- | --- |
| `SELECT` | 데이터 조회 | `SELECT * FROM member;` |
| `INSERT` | 데이터 삽입 | `INSERT INTO member (...) VALUES (...);` |
| `UPDATE` | 데이터 수정 | `UPDATE member SET point = 2000 WHERE idx = 1;` |
| `DELETE` | 데이터 삭제 | `DELETE FROM member WHERE idx = 1;` |

## 17. 단어장 테이블 만들기

영어 단어와 한글 뜻을 저장하는 `voca` 테이블을 만든다.

```sql
CREATE TABLE voca (
    eng VARCHAR(50) PRIMARY KEY,
    kor VARCHAR(50) NOT NULL,
    lev INT DEFAULT 1,
    regdate DATETIME DEFAULT NOW()
);
```

## 17.1 컬럼별 설명

| 컬럼명 | 데이터 타입 | 제약조건 | 설명 |
| --- | --- | --- | --- |
| `eng` | `VARCHAR(50)` | `PRIMARY KEY` | 영어 단어 |
| `kor` | `VARCHAR(50)` | `NOT NULL` | 한글 뜻 |
| `lev` | `INT` | `DEFAULT 1` | 단어 난이도 |
| `regdate` | `DATETIME` | `DEFAULT NOW()` | 등록일 |

## 17.2 구조 해석

```sql
eng VARCHAR(50) PRIMARY KEY
```

설명:

- 영어 단어를 기본키로 사용한다.
- 같은 영어 단어가 중복 저장될 수 없다.
- `PRIMARY KEY`이므로 `NULL`도 허용되지 않는다.

```sql
kor VARCHAR(50) NOT NULL
```

설명:

- 한글 뜻은 반드시 입력해야 한다.

```sql
lev INT DEFAULT 1
```

설명:

- 난이도를 저장한다.
- 값을 입력하지 않으면 기본값으로 `1`이 들어간다.

```sql
regdate DATETIME DEFAULT NOW()
```

설명:

- 단어를 등록한 날짜와 시간을 저장한다.
- 값을 직접 넣지 않으면 현재 시간이 자동 저장된다.

## 18. 전체 실행 흐름

처음부터 테이블을 만드는 흐름은 다음과 같다.

```sql
-- 1. 데이터베이스 목록 확인
SHOW DATABASES;

-- 2. 데이터베이스 생성
CREATE DATABASE ai;

-- 3. 사용할 데이터베이스 선택
USE ai;

-- 4. 테이블 생성
CREATE TABLE member (
    idx INT AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(20) UNIQUE NOT NULL,
    userpw VARCHAR(20) NOT NULL,
    name VARCHAR(20) NOT NULL,
    hp VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    ssn1 CHAR(6) NOT NULL,
    ssn2 CHAR(7) NOT NULL,
    zipcode VARCHAR(5),
    address1 VARCHAR(100),
    address2 VARCHAR(100),
    address3 VARCHAR(100),
    regdate DATETIME DEFAULT NOW(),
    point INT DEFAULT 1000
);

-- 5. 테이블 구조 확인
DESC member;
```

## 19. 핵심 요약

- 데이터베이스 목록 확인: `SHOW DATABASES;`
- 데이터베이스 생성: `CREATE DATABASE 데이터베이스명;`
- 데이터베이스 선택: `USE 데이터베이스명;`
- 테이블 생성: `CREATE TABLE 테이블명 (...);`
- 테이블 구조 확인: `DESC 테이블명;`
- 테이블 삭제: `DROP TABLE 테이블명;`
- 컬럼 추가: `ALTER TABLE 테이블명 ADD 컬럼명 데이터타입;`
- 컬럼 삭제: `ALTER TABLE 테이블명 DROP 컬럼명;`
- 컬럼 수정: `ALTER TABLE 테이블명 MODIFY COLUMN 컬럼명 데이터타입;`

## 20. DDL과 DML 차이

| 구분 | 목적 | 대표 명령어 |
| --- | --- | --- |
| DDL | 구조 정의 | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| DML | 데이터 조작 | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |

쉽게 말하면:

- DDL은 테이블의 모양을 다루는 명령어이다.
- DML은 테이블 안의 데이터를 다루는 명령어이다.

## 21. 실습할 때 주의할 점

1. `CREATE DATABASE` 후에는 반드시 `USE 데이터베이스명;`을 실행한다.
2. `DROP TABLE`은 테이블과 데이터를 모두 삭제하므로 조심한다.
3. 기본키는 중복과 `NULL`을 허용하지 않는다.
4. `AUTO_INCREMENT`는 보통 숫자 기본키와 함께 사용한다.
5. `VARCHAR`는 길이가 변하는 문자열에 사용한다.
6. `CHAR`는 주민등록번호 앞자리처럼 길이가 고정된 값에 사용한다.
7. `DEFAULT NOW()`를 사용하면 현재 시간이 자동으로 들어간다.
8. `ALTER TABLE`은 기존 테이블 구조를 바꿀 때 사용한다.