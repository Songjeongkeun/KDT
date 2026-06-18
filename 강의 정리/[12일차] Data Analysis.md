# MySQL DML, 조건 검색, 정규화, JOIN 정리

주요 내용은 `INSERT`, `SELECT`, `UPDATE`, `DELETE` 같은 DML, 조건 검색, 정렬, 그룹화, 정규화, 외래키, JOIN이다.

---

## 1. DML이란?

DML(Data Manipulation Language)은 테이블 안의 데이터를 조작하는 SQL 명령어이다.

| 명령어 | 의미 |
| --- | --- |
| `SELECT` | 데이터를 조회 |
| `INSERT` | 데이터를 추가 |
| `UPDATE` | 데이터를 수정 |
| `DELETE` | 데이터를 삭제 |

DDL이 테이블의 구조를 다룬다면, DML은 테이블 안에 들어 있는 실제 데이터를 다룬다.

```text
DDL: 테이블 만들기, 수정하기, 삭제하기
DML: 데이터 넣기, 조회하기, 수정하기, 삭제하기
```

---

## 2. 단어장 테이블 예시

영어 단어와 한글 뜻을 저장하는 `voca` 테이블을 생성

```sql
CREATE TABLE voca (
    eng VARCHAR(50) PRIMARY KEY,
    kor VARCHAR(50) NOT NULL,
    lev INT DEFAULT 1,
    regdate DATETIME DEFAULT NOW()
);
```

컬럼 구조는 다음과 같다.

| 컬럼명 | 의미 | 제약조건 |
| --- | --- | --- |
| `eng` | 영어 단어 | `PRIMARY KEY` |
| `kor` | 한글 뜻 | `NOT NULL` |
| `lev` | 난이도 | 기본값 `1` |
| `regdate` | 등록일 | 기본값 `NOW()` |

테이블 구조는 `DESC`로 확인한다.

```sql
DESC voca;
```

---

## 3. INSERT: 데이터 삽입

`INSERT`는 테이블에 새로운 데이터를 추가할 때 사용

### 3.1 전체 컬럼에 값 넣기

```sql
INSERT INTO voca VALUES ('apple', '사과', 1, NOW());
```

이 방식은 테이블의 모든 컬럼에 순서대로 값을 넣어야 한다.

```text
eng     kor   lev   regdate
apple   사과   1     현재 시간
```

### 3.2 일부 컬럼만 지정해서 값 넣기

```sql
INSERT INTO voca (eng, kor) VALUES ('banana', '바나나');
```

`lev`와 `regdate`는 값을 직접 넣지 않았지만 기본값이 자동으로 들어간다.

```text
eng      kor    lev   regdate
banana   바나나   1     현재 시간
```

### 3.3 기본값과 NULL 차이

```sql
INSERT INTO voca VALUES ('orange', '오렌지', NULL, NULL);
```

위 쿼리는 `lev`와 `regdate`에 기본값을 넣는 것이 아니라, 직접 `NULL`을 넣는 것이다.

```text
기본값 사용:
컬럼을 생략하면 DEFAULT 값이 들어간다.

NULL 직접 입력:
컬럼에 NULL이라는 값을 직접 넣는다.
```

`NOT NULL`이 걸린 컬럼에는 `NULL`을 넣을 수 없다.

### 3.4 기본키 중복 오류

`eng`는 기본키이므로 같은 영어 단어를 중복 저장할 수 없다.

```sql
INSERT INTO voca (eng, kor) VALUES ('orange', '오렌지');

INSERT INTO voca (eng, kor) VALUES ('orange', '오렌지');
```

오류 예시:

```text
Error Code: 1062. Duplicate entry 'orange' for key 'voca.PRIMARY'
```

기본키는 중복을 허용하지 않기 때문에 같은 `eng` 값을 다시 넣으면 오류가 발생한다.

---

## 4. DELETE: 데이터 삭제

`DELETE`는 테이블의 데이터를 삭제할 때 사용한다.

```sql
DELETE FROM voca WHERE eng = 'banana';
```

위 쿼리는 `eng`가 `'banana'`인 행만 삭제한다.

```text
WHERE 조건에 맞는 데이터만 삭제된다.
```

### 4.1 WHERE 없이 DELETE를 사용할 때 주의

```sql
DELETE FROM voca;
```

위 쿼리는 `voca` 테이블의 모든 데이터를 삭제한다.  
실무에서는 매우 위험한 쿼리이므로 반드시 조심해야 한다.

`DELETE`와 `TRUNCATE`의 차이는 다음과 같다.

| 구분 | DELETE | TRUNCATE |
| --- | --- | --- |
| 대상 | 조건에 맞는 행 또는 전체 행 | 전체 행 |
| `WHERE` 사용 | 가능 | 불가능 |
| 테이블 구조 | 유지 | 유지 |
| 복구 가능성 | 트랜잭션 상황에 따라 가능 | 일반적으로 어렵다 |
| 실행 속도 | 상대적으로 느림 | 상대적으로 빠름 |

**MySQL Workbench**에서는 **Safe Update Mode** 때문에 다음과 같은 오류가 발생할 수 있다.

```text
Error Code: 1175.
You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column.
```

이 오류는 조건 없이 전체 데이터를 수정하거나 삭제하는 실수를 막기 위한 안전장치이다.

---

## 5. UPDATE: 데이터 수정

`UPDATE`는 기존 데이터를 수정할 때 사용한다.

```sql
UPDATE voca SET lev = 2 WHERE eng = 'avocado';
```

위 쿼리는 `eng`가 `'avocado'`인 단어의 난이도를 `2`로 바꾼다.

### 5.1 WHERE 없이 UPDATE를 사용할 때 주의

```sql
UPDATE voca SET lev = 1;
```

위 쿼리는 모든 단어의 `lev`를 `1`로 바꾼다.  
전체 데이터를 수정하는 쿼리이므로 실행 전 반드시 확인해야 한다.

회원 포인트를 증가시키는 예시는 다음과 같다.

```sql
UPDATE member SET point = point + 50;
```

모든 회원의 포인트를 `50`씩 증가시킨다.

특정 회원만 수정하려면 `WHERE`를 사용한다.

```sql
UPDATE member SET point = point + 100 WHERE idx = 2;
```

기본키인 `idx`를 조건으로 사용하면 특정 행을 빠르고 정확하게 찾을 수 있다.

---

## 6. SELECT: 데이터 조회

`SELECT`는 테이블의 데이터를 조회할 때 사용한다.

```sql
SELECT * FROM member;
```

`*`는 모든 컬럼을 의미한다.

특정 컬럼만 조회할 수도 있다.

```sql
SELECT userid FROM member;
SELECT userid, name FROM member;
SELECT hp, userid, name FROM member;
```

컬럼 순서는 `SELECT`에 작성한 순서대로 출력된다.

---

## 7. SELECT에서 계산과 별칭 사용

`SELECT`는 테이블 조회뿐 아니라 계산 결과도 출력할 수 있다.

```sql
SELECT 100;
SELECT 100 + 50;
SELECT 100 + 50 AS 덧셈;
SELECT 100 + 50 AS '덧셈 연산';
```

출력 결과 :

```tex
100 | 100 + 50	| 덧셈	| 덧셈 연산
100 | 150				| 150	 | 150
```

`AS`는 출력 컬럼의 이름을 바꿀 때 사용한다.

### 7.1 빈 문자열과 NULL

```sql
SELECT '';
SELECT NULL;
SELECT 100 + '';
SELECT 100 + NULL;
```

의미는 다음과 같다.

| 표현 | 의미 |
| --- | --- |
| `''` | 빈 문자열 |
| `NULL` | 값이 없음 |
| `100 + ''` | MySQL에서 빈 문자열을 숫자 `0`처럼 처리할 수 있음 |
| `100 + NULL` | 결과는 `NULL` |

`NULL`은 값이 없다는 뜻이므로, `NULL`과의 연산 결과는 대부분 `NULL`이 된다.

---

## 8. WHERE 조건 검색

`WHERE`는 조건에 맞는 행만 조회할 때 사용한다.

```sql
SELECT userid, name, point 
FROM member 
WHERE point >= 150;
```

위 쿼리는 포인트가 `150` 이상인 회원만 조회한다.

---

## 9. SQL 연산자

SQL에서 자주 사용하는 연산자는 다음과 같다.

| 종류 | 연산자 | 의미 |
| --- | --- | --- |
| 산술 연산자 | `+`, `-`, `*`, `/`, `MOD`, `DIV` | 계산 |
| 비교 연산자 | `=`, `<`, `>`, `<=`, `>=`, `<>` | 값 비교 |
| 논리 연산자 | `AND`, `OR`, `NOT`, `XOR` | 조건 연결 |
| 범위 조건 | `BETWEEN A AND B` | A 이상 B 이하 |
| 목록 조건 | `IN` | 목록 중 하나와 일치 |
| NULL 비교 | `IS NULL`, `IS NOT NULL` | NULL 여부 확인 |
| 패턴 검색 | `LIKE` | 문자열 패턴 검색 |

---

## 10. BETWEEN

`BETWEEN A AND B`는 A 이상 B 이하의 값을 찾을 때 사용한다.

```sql
SELECT userid, name, point, gender
FROM member
WHERE point BETWEEN 150 AND 200;
```

위 쿼리는 포인트가 `150` 이상 `200` 이하인 회원을 조회한다.

```text
point >= 150 AND point <= 200
```

위 조건과 같은 의미이다.

---

## 11. AND와 OR

로그인처럼 여러 조건을 동시에 만족해야 하는 경우 `AND`를 사용한다.

```sql
SELECT userid
FROM member
WHERE userid = 'apple'
  AND userpw = '1111';
```

아이디와 비밀번호가 모두 맞아야 결과가 나온다.

여러 조건 중 하나만 만족해도 되는 경우 `OR`를 사용한다.

```sql
SELECT *
FROM member
WHERE name = '김사과'
   OR name = '반하나'
   OR name = '오렌지';
```

---

## 12. IN

`IN`은 여러 값 중 하나와 일치하는 데이터를 찾을 때 사용한다.

```sql
SELECT *
FROM member
WHERE name IN ('김사과', '반하나', '오렌지');
```

아래 쿼리와 같은 의미이다.

```sql
SELECT *
FROM member
WHERE name = '김사과'
   OR name = '반하나'
   OR name = '오렌지';
```

`OR`가 여러 번 반복될 때 `IN`을 사용하면 코드가 더 깔끔해진다.

---

## 13. NULL 검색

`NULL`은 일반적인 `=` 연산자로 비교하지 않는다. `NULL` 은 `is` 연산자를 사용하여 판별한다.

```sql
SELECT *
FROM member
WHERE regdate IS NULL;
```

`regdate`가 `NULL`인 회원을 조회한다.

```sql
SELECT *
FROM member
WHERE regdate IS NOT NULL;
```

`regdate`가 `NULL`이 아닌 회원을 조회한다.

```text
NULL 비교는 = NULL이 아니라 IS NULL을 사용한다.
```

---

## 14. LIKE 패턴 검색

`LIKE`는 문자열 패턴을 이용해 데이터를 검색할 때 사용한다.

| 패턴 | 의미 |
| --- | --- |
| `%` | 글자 수 제한 없이 아무 문자열 |
| `_` | 정확히 한 글자 |

### 14.1 특정 문자로 시작

```sql
SELECT *
FROM member
WHERE userid LIKE 'a%';
```

`userid`가 `a`로 시작하는 회원을 찾는다.

### 14.2 특정 문자로 끝남

```sql
SELECT *
FROM member
WHERE userid LIKE '%a';
```

`userid`가 `a`로 끝나는 회원을 찾는다.

### 14.3 특정 문자를 포함

```sql
SELECT *
FROM member
WHERE userid LIKE '%a%';
```

`userid`에 `a`가 포함된 회원을 찾는다.

### 14.4 이메일이 `.com`으로 끝남

```sql
SELECT *
FROM member
WHERE email LIKE '%.com';
```

### 14.5 이름이 정확히 3글자

```sql
SELECT *
FROM member
WHERE name LIKE '___';
```

`_`는 한 글자를 의미하므로, `_` 3개는 정확히 3글자를 뜻한다.

### 14.6 김씨이며 이름이 3글자

```sql
SELECT *
FROM member
WHERE name LIKE '김__';
```

첫 글자는 `김`이고 뒤에 정확히 두 글자가 오는 이름을 검색한다.

---

## 15. ORDER BY 정렬

`ORDER BY`는 조회 결과를 정렬할 때 사용한다.

```sql
SELECT *
FROM member
ORDER BY idx;
```

기본 정렬은 오름차순이다. `ASC`가 생략된 형태이다.

```sql
SELECT *
FROM member
ORDER BY idx ASC;
```

내림차순 정렬은 `DESC`를 사용한다.

```sql
SELECT *
FROM member
ORDER BY idx DESC;
```

포인트가 높은 회원부터 보고 싶다면 다음처럼 작성한다.

```sql
SELECT *
FROM member
ORDER BY point DESC;
```

포인트가 같을 때 가입일이 최신인 회원을 먼저 보려면 정렬 조건을 여러 개 작성한다.

```sql
SELECT *
FROM member
ORDER BY point DESC, regdate DESC;
```

---

## 16. LIMIT

`LIMIT`은 조회 결과 중 일부 행만 가져올 때 사용한다.

```sql
SELECT *
FROM member
LIMIT 2;
```

위 쿼리는 처음부터 2개의 행만 조회한다.

특정 위치부터 원하는 개수만큼 가져올 수도 있다.

```sql
SELECT *
FROM member
LIMIT 2, 3;
```

의미는 다음과 같다.

```text
2번 인덱스부터 3개 가져오기
```

SQL의 시작 위치는 보통 `0`부터 생각하면 된다.

포인트 기준 상위 3명을 조회하는 예시는 다음과 같다.

```sql
SELECT *
FROM member
ORDER BY point DESC, regdate DESC
LIMIT 3;
```

---

## 17. GROUP BY

`GROUP BY`는 같은 값을 가진 행들을 그룹으로 묶을 때 사용한다.

성별로 회원을 묶는 예시는 다음과 같다.

```sql
SELECT gender
FROM member
GROUP BY gender;
```

성별마다 몇 명인지 구하려면 `COUNT()`를 함께 사용한다.

```sql
SELECT gender, COUNT(idx) AS 인원수
FROM member
GROUP BY gender;
```

출력 예시:

```text
gender   인원수
여자       4
남자       2
```

---

## 18. WHERE와 HAVING 차이

`WHERE`는 그룹을 만들기 전에 행을 필터링한다.  
`HAVING`은 그룹을 만든 후 그룹 결과를 필터링한다.

```sql
SELECT gender, COUNT(idx) AS 인원수
FROM member
WHERE gender = '여자'
GROUP BY gender;
```

위 쿼리는 먼저 여자 회원만 남긴 뒤, 성별로 그룹을 묶는다.

```sql
SELECT gender, COUNT(idx) AS 인원수
FROM member
GROUP BY gender
HAVING gender = '여자';
```

위 쿼리는 성별로 그룹을 만든 뒤, `gender`가 `'여자'`인 그룹만 남긴다.

인원수가 3명 이상인 성별을 찾는 예시는 다음과 같다.

```sql
SELECT gender, COUNT(idx) AS 인원수
FROM member
GROUP BY gender
HAVING 인원수 > 3;
```

집계함수 결과를 조건으로 사용할 때는 `WHERE`가 아니라 `HAVING`을 사용한다.

---

## 19. 집계 함수

집계 함수는 데이터베이스에서 그룹 단위로 데이터를 집계하고 통계적인 값을 계산하기 위해 사용되는 함수이다. 집계 함수는 여러 개의 행을 하나의 결과로 반환하며, 이를 통해 데이터의 합계, 평균, 개수, 최댓값, 최솟값 등을 계산할 수 있다. 집계 함수는 `SELECT` 문장의 `SELECT` 절이나 `HAVING` 절에서 사용된다.

### 19.1 `SUM()` 

`SUM()` 은 숫자 데이터의 합계를 계산한다. 주로 숫자형 열에서 사용되며, `NULL` 값을 제외하고 합계를 계산한다.

```sql
SELECT SUM(sales) AS total_sales 
FROM orders;
```

지정된 열의 모든 갑을 합산하여 결과를 반환

### 19.2 `AVG()`

`AVG()` 는 숫자 데이터의 평균을 계산한다. 숫자형 열에서 사용되며, `NULL`값을 제외하고 평균을 계산한다.

```sql
SELECT AVG(price) AS average_price
FROM products;
```

지정된 열의 평균 값을 계산하여 결과 반환

### 19.3 `COUNT()`

`COUNT()` 는 행의 개수를 계산한다. 열이나 테이블에서 사용될 수 있으며, `NULL` 값을 포함한 모든 행의 개수를 반환한다.

```sql
SELECT COUNT(*) AS total_orders
FROM orders;
```

지정된 열의 행 수를 계산하여 결과를 반환

### 19.4 `MAX()`

`MAX()` 는 숫자나 문자열 데이터의 최댓값을 반환한다. 숫자형 열이나 문자열 열에서 사용될 수 있으며, `NULL` 값을 제외한 최댓값을 반환한다.

```sql
SELECT MAX(quantity) AS max_quantity
FROM products; 
```

지정된 열의 최댓값을 찾아 결과를 반환

### 19.5 `MIN()`

`MIN()` 은 숫자나 문자열 데이터의 최솟값을 반환한다. 숫자형 열이나 문자열 열에서 사용될 수 있으며, `NULL` 값을 제외한 최솟값을 반환한다.

```sql
SELECT MIN(price) AS min_price
FROM products;
```

지정된 열의 최솟값을 찾아 결과 반환

### 19.6 `GROUP_CONCAT()`

`GROUP_CONCAT()` 는 문자열 데이터를 그룹화하여 하나의 문자열로 결합한다. 그룹 내에서 문자열을 결합하고, 구분자를 지정하여 결과를 반환한다.

```sql
SELECT department, GROUP_CONCAT(employee_name) AS employees
FROM employees
GROUP BY department;
```

그룹 내의 특정 열 값을 구분자로 결합하여 하나의 문자열로 반환

### 19.7 `DISTINCT()` 

`DISTINCT()` 는 중복된 값을 제거한 후 유일한 값을 반환한다. 주로 집계 함수와 함께 사용되어 그룹화된 데이터에서 중복을 제거한 결과를 얻을 수 있다.

```sql
SELECT DISTINCT department
FROM employees;
```

중복된 값을 제거하고 유일한 값만 반환

---

## 20. 정규화란?

정규화(Normalization)는 데이터베이스 테이블을 효율적으로 구조화하는 작업이다.

정규화를 하는 이유는 다음과 같다.

- 중복 데이터를 줄인다.
- 데이터가 서로 꼬이는 문제를 줄인다.
- 데이터 무결성을 유지한다.
- 유지보수를 편하게 만든다.

예를 들어 학생, 과목, 교수 정보가 하나의 테이블에 모두 섞여 있으면 같은 교수 정보가 여러 번 반복될 수 있다.

```text
학생명   과목명      교수명   교수전화번호
김사과   Python     이교수   010-1111-1111
반하나   Python     이교수   010-1111-1111
오렌지   Database   박교수   010-2222-2222
```

`Python` 과목을 듣는 학생이 많아질수록 `이교수`의 정보가 계속 반복된다.  
교수 전화번호가 바뀌면 여러 행을 모두 수정해야 하므로 실수 가능성이 커진다.

이런 문제를 줄이기 위해 테이블을 역할별로 나누는 것이 정규화이다.

### 20.1 제1정규형(1NF)

제1정규형은 하나의 칸에 하나의 값만 들어가야 한다는 규칙이다.

잘못된 예시는 다음과 같다.

| student_id | student_name | skills |
| ---- | :-- | :-- |
| 1 | 김사과 | MySQL, Python |

`skills` 컬럼에 `MySQL, Python`처럼 여러 값이 들어가 있으므로 1NF를 만족하지 않는다.

수정하면 다음과 같다.

| student_id | student_name | skill |
| :--- | :-- | --- |
| 1 | 김사과 | MySQL |
| 1 | 김사과 | Python |

하나의 칸에는 하나의 값만 들어간다.

### 20.2 제2정규형(2NF)

제2정규형은 다음 조건을 만족해야 한다.

1. 제1정규형을 만족한다.
2. 기본키 전체에 완전 종속되어야 한다.

특히 복합 기본키를 사용할 때 중요하다.

예를 들어 수강 테이블의 기본키가 `(student_id, course_id)`라고 하자.

| student_id | course_id | student_name | course_name |
| :--- | :--- | :-- | :-- |
| 1 | 101 | 김사과 | Python |
| 1 | 102 | 김사과 | Database |

여기서 `student_name`은 `student_id`에만 의존한다.  
`course_name`은 `course_id`에만 의존한다.  
즉, 복합키 전체가 아니라 일부에만 의존하므로 2NF를 만족하지 않는다.

이를 해결하려면 테이블을 나눈다.

```text
student(student_id, student_name)
course(course_id, course_name)
enroll(student_id, course_id)
```

### 20.3 제3정규형(3NF)

제3정규형은 다음 조건을 만족해야 한다.

1. 제2정규형을 만족한다.
2. 이행적 종속을 제거한다.

이행적 종속은 A가 B를 결정하고, B가 C를 결정해서, 결과적으로 A가 C를 간접적으로 결정하는 관계이다.

```text
학번 -> 학과번호
학과번호 -> 학과명
학번 -> 학과명
```

`학번`으로 `학과명`을 직접 저장하면 학과명 변경 시 여러 학생 데이터를 수정해야 한다.

따라서 학과 정보를 별도 테이블로 분리한다.

```text
student(student_id, student_name, department_id)
department(department_id, department_name)
```

정규화의 핵심은 “중복되는 정보는 따로 빼고, 필요한 곳에서는 키로 연결한다”는 것이다.

### 20.4 정규화된 테이블 예시

학생, 교수, 과목, 수강 정보를 테이블로 나누면 다음과 같다.

**학생 테이블**

```sql
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(20)
);
```

**교수 테이블**

```sql
CREATE TABLE professor (
    professor_id INT PRIMARY KEY,
    professor_name VARCHAR(20),
    professor_phone VARCHAR(20)
);
```

**과목 테이블**

```sql
CREATE TABLE course (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50),
    professor_id INT,
    FOREIGN KEY (professor_id) REFERENCES professor(professor_id)
);
```

`course` 테이블은 `professor_id`를 통해 `professor` 테이블과 연결된다.

**수강 테이블**

```sql
CREATE TABLE enroll (
    student_id INT,
    course_id INT,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    PRIMARY KEY (student_id)
);
```

수강 테이블은 학생과 과목을 연결하는 중간 테이블이다.

`PRIMARY KEY (student_id)`를 사용하면 한 학생이 한 과목만 수강할 수 있는 구조가 된다.



## 21. 외래키 제약조건

외래키(Foreign Key)는 다른 테이블의 기본키를 참조하는 키이다.

```sql
FOREIGN KEY (idx) REFERENCES member(idx)
```

프로필 테이블 예시는 다음과 같다.

```sql
CREATE TABLE profile (
    idx INT NOT NULL,
    height DOUBLE,
    weight DOUBLE,
    mbti VARCHAR(10),
    FOREIGN KEY (idx) REFERENCES member(idx)
);
```

`profile.idx`는 `member.idx`를 참조한다.  
즉, `member`에 존재하는 회원만 `profile`에 추가할 수 있다.

```sql
INSERT INTO profile
VALUES (1, 160, 50, 'ISTJ');

INSERT INTO profile
VALUES (3, 170, 70, 'ESTP');
```

하지만 `member` 테이블에 `idx = 7`인 회원이 없다면 다음 쿼리는 실패한다.

```sql
INSERT INTO profile
VALUES (7, 175, 80, 'ENFJ');
```

오류 의미:

```text
외래키 제약조건 위배
member 테이블에 없는 idx는 profile에 넣을 수 없다.
```

외래키는 테이블 사이의 관계가 잘못되는 것을 막아준다.

---

## 22. JOIN이란?

JOIN은 두 개 이상의 테이블을 연결해서 조회하는 SQL 문법이다.

정규화를 하면 테이블이 여러 개로 나뉘기 때문에, 필요한 데이터를 한 번에 보기 위해 JOIN을 사용한다.

예를 들어 회원 기본 정보는 `member` 테이블에 있고, 키, 몸무게, MBTI는 `profile` 테이블에 있다고 하자.

```text
member 테이블
idx, userid, name, gender

profile 테이블
idx, height, weight, mbti
```

두 테이블은 `idx`로 연결된다.

### 22.1 INNER JOIN

`INNER JOIN`은 두 테이블에 모두 연결되는 데이터만 조회한다.

```sql
SELECT member.idx, userid, name, gender, mbti
FROM member
INNER JOIN profile
ON member.idx = profile.idx;
```

테이블 이름이 길면 별칭을 사용할 수 있다.

```sql
SELECT m.idx, m.userid, m.name, m.gender, p.mbti
FROM member AS m
INNER JOIN profile AS p
ON m.idx = p.idx;
```

`member AS m`은 `member` 테이블을 `m`이라는 이름으로 줄여 쓰겠다는 의미이다.  
`AS`는 생략할 수 있다.

```sql
SELECT m.idx, m.userid, m.name, m.gender, p.mbti
FROM member m
INNER JOIN profile p
ON m.idx = p.idx;
```

INNER JOIN 결과는 다음처럼 이해할 수 있다.

```text
member에도 있고 profile에도 있는 idx만 출력
```

출력 예시:

```text
idx   userid   name    gender   mbti
1     apple    김사과   여자      ISTJ
3     orange   오렌지   남자      ESTP
4     melon    이메론   남자      ENFJ
6     berry    배애리   여자      ENFJ
```

### 22.2 LEFT JOIN

`LEFT JOIN`은 왼쪽 테이블의 데이터는 모두 보여주고, 오른쪽 테이블에 연결되는 데이터가 있으면 함께 보여준다.

```sql
SELECT m.idx, m.userid, m.name, m.gender, p.mbti
FROM member AS m
LEFT JOIN profile AS p
ON m.idx = p.idx;
```

`member`를 기준으로 모든 회원을 보여준다.  
프로필이 없는 회원은 `mbti`가 `NULL`로 나온다.

```text
member는 모두 출력
profile에 없으면 profile 컬럼은 NULL
```

출력 예시:

```text
idx   userid   name    gender   mbti
1     apple    김사과   여자      ISTJ
2     banana   반하나   여자      NULL
3     orange   오렌지   남자      ESTP
4     melon    이메론   남자      ENFJ
5     cherry   채리     여자      NULL
6     berry    배애리   여자      ENFJ
```

### 22.3 RIGHT JOIN

`RIGHT JOIN`은 오른쪽 테이블의 데이터는 모두 보여주고, 왼쪽 테이블에 연결되는 데이터가 있으면 함께 보여준다.

```sql
SELECT m.idx, m.userid, m.name, m.gender, p.mbti
FROM member AS m
RIGHT JOIN profile AS p
ON m.idx = p.idx;
```

출력 예시:

```tex
idx   userid   name    gender   mbti
1     apple    김사과   여자      ISTJ
3     orange   오렌지   남자      ESTP
4     melon    이메론   남자      ENFJ
6     berry    배애리   여자      ENFJ
```

```text
profile은 모두 출력
member에 연결되는 데이터가 있으면 member 정보도 함께 출력
```

현재 예시에서는 외래키 때문에 `profile.idx`는 반드시 `member.idx`에 존재해야 한다.  
그래서 `RIGHT JOIN` 결과가 `INNER JOIN`과 비슷하게 보일 수 있다.

### 22.4 CROSS JOIN

`CROSS JOIN`은 두 테이블의 모든 조합을 만든다.

```sql
SELECT userid, name, gender, mbti
FROM member
CROSS JOIN profile;
```

만약 `member`가 6행이고 `profile`이 4행이라면 결과는 다음과 같다.

```text
6 * 4 = 24행
```

`CROSS JOIN`은 모든 조합을 만들기 때문에 결과 행 수가 매우 커질 수 있다.  
실무에서는 꼭 필요한 경우가 아니라면 조심해서 사용해야 한다.

### 22.5 JOIN 종류 비교

| JOIN 종류 | 기준 | 결과 |
| --- | --- | --- |
| `INNER JOIN` | 양쪽 테이블 모두 | 서로 연결되는 데이터만 출력 |
| `LEFT JOIN` | 왼쪽 테이블 | 왼쪽은 모두 출력, 오른쪽 없으면 `NULL` |
| `RIGHT JOIN` | 오른쪽 테이블 | 오른쪽은 모두 출력, 왼쪽 없으면 `NULL` |
| `CROSS JOIN` | 모든 조합 | 두 테이블 행의 모든 조합 출력 |

그림처럼 생각하면 다음과 같다.

```text
INNER JOIN
member ∩ profile

LEFT JOIN
member 전체 + 연결되는 profile

RIGHT JOIN
연결되는 member + profile 전체

CROSS JOIN
member의 모든 행 × profile의 모든 행
```

---

## 23. 정규화와 JOIN의 관계

정규화를 하면 중복 데이터가 줄어들지만, 데이터가 여러 테이블로 나뉜다.  
따라서 여러 테이블의 정보를 함께 조회하려면 JOIN이 필요하다.

```text
정규화 전:
한 테이블에 모든 정보가 들어 있음
조회는 쉽지만 중복이 많음

정규화 후:
여러 테이블로 나누어 저장
중복은 줄지만 JOIN이 필요함
```

정규화와 JOIN은 서로 반대되는 개념이 아니라 함께 사용되는 개념이다.

- 정규화는 데이터를 잘 나누는 작업이다.
- JOIN은 나누어진 데이터를 다시 연결해서 조회하는 작업이다.

---

## 24. 과도한 정규화와 비정규화

정규화를 많이 하면 데이터 중복은 줄어들지만, 조회할 때 JOIN이 많아질 수 있다.  
JOIN이 너무 많아지면 조회 성능이 떨어질 수 있다.

이때 성능 최적화를 위해 일부러 데이터를 합쳐 저장하는 경우가 있다.  
이를 비정규화(Denormalization)라고 한다.

```text
정규화:
중복을 줄이고 데이터 무결성을 높인다.

비정규화:
조회 성능을 위해 일부 중복을 허용한다.
```

실무에서는 무조건 정규화를 많이 하는 것이 답은 아니다.  
데이터 무결성과 조회 성능 사이에서 균형을 잡아야 한다.

---

## 25. 오늘 내용 핵심 요약

| 개념 | 핵심 |
| --- | --- |
| `INSERT` | 테이블에 데이터를 추가한다 |
| `SELECT` | 데이터를 조회한다 |
| `UPDATE` | 기존 데이터를 수정한다 |
| `DELETE` | 데이터를 삭제한다 |
| `WHERE` | 조건에 맞는 행만 필터링한다 |
| `LIKE` | 문자열 패턴 검색에 사용한다 |
| `ORDER BY` | 결과를 정렬한다 |
| `LIMIT` | 일부 행만 가져온다 |
| `GROUP BY` | 같은 값끼리 그룹화한다 |
| `HAVING` | 그룹화 결과를 조건으로 필터링한다 |
| 정규화 | 중복을 줄이고 테이블을 역할별로 나눈다 |
| 외래키 | 다른 테이블의 기본키를 참조한다 |
| JOIN | 나뉜 테이블을 연결해서 조회한다 |

오늘 배운 내용의 큰 흐름은 다음과 같다.

```text
1. DML로 데이터를 조작한다.
2. WHERE, LIKE, ORDER BY, LIMIT으로 원하는 데이터를 조회한다.
3. GROUP BY와 HAVING으로 데이터를 집계한다.
4. 정규화로 테이블을 나눈다.
5. 외래키로 테이블 관계를 만든다.
6. JOIN으로 나뉜 테이블을 다시 연결해 조회한다.
```
