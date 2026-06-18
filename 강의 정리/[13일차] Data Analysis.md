# [13일차] Data Analysis

이번 시간에는 MySQL에서 데이터를 더 유연하게 조회하고 관리하기 위한 내용을 학습했다.

핵심 내용은 다음과 같다.

- 서브쿼리
- `UNION`
- 테이블 복사
- 사용자 계정과 권한
- MySQL 내장 함수

---

## 1. 서브쿼리

서브쿼리(Sub Query)는 SQL문 안에 포함되는 또 다른 `SELECT`문이다.

즉, 하나의 쿼리 결과를 다른 쿼리의 조건이나 임시 테이블처럼 사용할 수 있다.

기본 형식:

```sql
SELECT 컬럼명
FROM 테이블명
WHERE 컬럼명 = (
    SELECT 컬럼명
    FROM 테이블명
    WHERE 조건
);
```

예시:

```sql
-- 김사과보다 포인트가 많은 회원 조회
SELECT *
FROM member
WHERE point > (
    SELECT point
    FROM member
    WHERE name = '김사과'
);
```

안쪽 쿼리에서 `김사과`의 포인트를 먼저 구하고, 바깥쪽 쿼리에서 그 포인트보다 큰 회원을 조회한다.

---

## 2. 단일 행 서브쿼리

단일 행 서브쿼리는 결과가 하나의 값으로 나오는 서브쿼리이다.

`MAX()`, `MIN()`, `AVG()` 같은 집계 함수와 자주 사용한다.

```sql
-- 포인트가 가장 높은 회원 조회
SELECT *
FROM member
WHERE point = (
    SELECT MAX(point)
    FROM member
);
```

`SELECT MAX(point) FROM member`의 결과는 하나의 값이다.  
바깥 쿼리는 그 값과 같은 `point`를 가진 회원을 조회한다.

---

## 3. 다중 행 서브쿼리

다중 행 서브쿼리는 결과가 여러 개 나오는 서브쿼리이다.

결과가 여러 개이므로 `IN`, `ANY`, `ALL` 같은 연산자와 함께 사용한다.

```sql
-- 포인트가 150 이상인 회원 조회
SELECT *
FROM member
WHERE userid IN (
    SELECT userid
    FROM member
    WHERE point >= 150
);
```

### 주요 연산자

| 연산자 | 의미 |
| --- | --- |
| `IN` | 결과 목록 중 하나와 일치하면 참 |
| `ANY` | 결과 목록 중 하나라도 조건을 만족하면 참 |
| `ALL` | 결과 목록의 모든 값이 조건을 만족해야 참 |

---

## 4. FROM절 서브쿼리

`FROM`절에 들어가는 서브쿼리는 조회 결과를 임시 테이블처럼 사용한다.

```sql
SELECT name, point
FROM (
    SELECT name, point
    FROM member
    WHERE point >= 150
) AS high_point_member;
```

`FROM`절 서브쿼리는 반드시 별칭을 붙여야 한다.

여기서는 `high_point_member`라는 이름의 임시 테이블처럼 사용했다.

---

## 5. SELECT절 서브쿼리

`SELECT`절에 서브쿼리를 사용하면 각 행의 결과와 함께 별도 계산 결과를 출력할 수 있다.

```sql
-- 각 회원의 포인트와 전체 평균 포인트를 함께 조회
SELECT
    name,
    point,
    (SELECT AVG(point) FROM member) AS avg_point
FROM member;
```

각 회원의 `point`와 전체 회원의 평균 포인트가 함께 출력된다.

---

## 6. EXISTS

`EXISTS`는 서브쿼리 결과가 존재하는지 확인할 때 사용한다.

```sql
-- 주문 내역이 있는 회원 조회
SELECT *
FROM member m
WHERE EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.member_idx = m.idx
);
```

`orders` 테이블에 해당 회원의 주문 내역이 하나라도 있으면 조회된다.

`SELECT 1`은 실제 데이터를 가져오기 위한 목적이 아니라, 존재 여부만 확인하기 위한 관례적인 표현이다.

---

## 7. 주문 테이블

회원과 주문 데이터를 연결하기 위해 `orders` 테이블을 생성했다.

```sql
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    member_idx INT NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    price INT NOT NULL,
    order_date DATETIME DEFAULT NOW(),
    FOREIGN KEY (member_idx) REFERENCES member(idx)
);
```

### 컬럼 설명

| 컬럼명 | 설명 |
| --- | --- |
| `order_id` | 주문 고유 번호 |
| `member_idx` | 주문한 회원 번호 |
| `product_name` | 상품명 |
| `price` | 가격 |
| `order_date` | 주문일 |

`member_idx`는 `member` 테이블의 `idx`를 참조한다.  
즉, 주문 데이터와 회원 데이터를 연결하는 역할을 한다.

---

## 8. 주문 여부 조회

주문한 회원:

```sql
SELECT *
FROM member
WHERE idx IN (
    SELECT member_idx
    FROM orders
);
```

주문하지 않은 회원:

```sql
SELECT *
FROM member
WHERE idx NOT IN (
    SELECT member_idx
    FROM orders
);
```

`IN`은 목록에 포함된 데이터를 찾고, `NOT IN`은 목록에 포함되지 않은 데이터를 찾는다.

---

## 9. 가장 비싼 상품을 주문한 회원

```sql
SELECT *
FROM member
WHERE idx = (
    SELECT member_idx
    FROM orders
    WHERE price = (
        SELECT MAX(price)
        FROM orders
    )
);
```

실행 흐름:

1. `orders`에서 가장 비싼 가격을 찾는다.
2. 그 가격의 주문을 한 회원 번호를 찾는다.
3. 해당 회원 번호를 가진 회원 정보를 조회한다.

같은 결과를 `JOIN`으로도 조회할 수 있다.

```sql
SELECT m.name, o.product_name
FROM member m
INNER JOIN orders o
ON m.idx = o.member_idx
WHERE o.price = (
    SELECT MAX(price)
    FROM orders
);
```

---

## 10. 테이블 복사

기존 테이블의 데이터를 다른 테이블로 복사할 수 있다.

```sql
INSERT INTO orders_copy
SELECT *
FROM orders;
```

단, 이 방식은 두 테이블의 컬럼 구조가 같을 때 사용하기 좋다.

조회 결과로 새 테이블을 만들 수도 있다.

```sql
CREATE TABLE orders_copy_copy
AS
SELECT *
FROM orders;
```

주의할 점:

- 데이터는 복사된다.
- 기본키, 외래키, 인덱스 같은 제약조건은 그대로 복사되지 않을 수 있다.

---

## 11. UNION

`UNION`은 여러 `SELECT` 결과를 위아래로 합치는 기능이다.

```sql
SELECT name, address1
FROM member
WHERE address1 LIKE '서울%'

UNION

SELECT name, address1
FROM member
WHERE address1 LIKE '부산%';
```

서울 회원과 부산 회원의 조회 결과를 하나로 합친다.

### UNION 사용 조건

- 각 `SELECT`의 컬럼 개수가 같아야 한다.
- 각 컬럼의 데이터 타입이 호환되어야 한다.
- 컬럼명은 보통 첫 번째 `SELECT`의 컬럼명을 따른다.

---

## 12. UNION과 UNION ALL

`UNION`은 중복 데이터를 제거한다.

```sql
SELECT eng, kor, lev
FROM voca

UNION

SELECT eng, kor, lev
FROM voca_new;
```

`UNION ALL`은 중복 데이터를 제거하지 않는다.

```sql
SELECT eng, kor, lev
FROM voca

UNION ALL

SELECT eng, kor, lev
FROM voca_new;
```

| 구분 | 중복 제거 | 특징 |
| --- | --- | --- |
| `UNION` | 제거함 | 결과가 깔끔함 |
| `UNION ALL` | 제거하지 않음 | 더 빠를 수 있음 |

---

## 13. 사용자 계정

사용자 계정은 데이터베이스에 접속할 수 있는 로그인 계정이다.

`root` 계정은 모든 권한을 가진 관리자 계정이므로 실제 프로젝트에서는 필요한 권한만 가진 계정을 따로 만들어 사용하는 것이 좋다.

기본 형식:

```sql
CREATE USER '계정명'@'접속위치' IDENTIFIED BY '비밀번호';
```

예시:

```sql
CREATE USER 'apple'@'localhost' IDENTIFIED BY '1111';
```

### 접속 위치

| 예시 | 의미 |
| --- | --- |
| `'apple'@'localhost'` | 같은 컴퓨터에서만 접속 가능 |
| `'apple'@'%'` | 어디서든 접속 가능 |
| `'apple'@'192.168.0.%'` | 특정 내부망에서 접속 가능 |
| `'apple'@'192.168.0.10'` | 특정 IP에서만 접속 가능 |

---

## 14. 권한 부여

사용자에게 권한을 부여할 때는 `GRANT`를 사용한다.

```sql
GRANT ALL
ON ai.*
TO 'apple'@'localhost';
```

`apple` 계정에게 `ai` 데이터베이스의 모든 테이블에 대한 권한을 부여한다.

조회 권한만 부여할 수도 있다.

```sql
CREATE USER 'banana'@'localhost' IDENTIFIED BY '2222';

GRANT SELECT
ON ai.*
TO 'banana'@'localhost';
```

### 권한 범위

| 표현 | 의미 |
| --- | --- |
| `ai.*` | `ai` 데이터베이스의 모든 테이블 |
| `*.*` | 모든 데이터베이스의 모든 테이블 |

### 주요 권한

| 권한 | 의미 |
| --- | --- |
| `SELECT` | 조회 |
| `INSERT` | 삽입 |
| `UPDATE` | 수정 |
| `DELETE` | 삭제 |
| `CREATE` | 생성 |
| `DROP` | 삭제 |
| `ALTER` | 구조 변경 |
| `ALL` | 일반적인 모든 권한 |

---

## 15. 권한 확인, 회수, 계정 삭제

권한 확인:

```sql
SHOW GRANTS FOR 'apple'@'localhost';
```

권한 회수:

```sql
REVOKE DELETE
ON ai.*
FROM 'orange'@'localhost';
```

비밀번호 변경:

```sql
ALTER USER 'banana'@'localhost' IDENTIFIED BY '1004';
```

사용자 삭제:

```sql
DROP USER 'banana'@'localhost';
```

계정과 권한은 보안과 직접 연결되므로, 필요한 사용자에게 필요한 권한만 부여하는 것이 좋다.

---

## 16. MySQL 함수

MySQL 함수는 조회 결과를 바로 가공할 때 사용한다.

오늘 배운 함수는 크게 다음과 같이 나눌 수 있다.

| 종류 | 함수 |
| --- | --- |
| 문자열 함수 | `CONCAT`, `LEFT`, `RIGHT`, `SUBSTRING`, `REPLACE`, `UPPER` |
| 수학 함수 | `ABS`, `ROUND`, `CEIL`, `FLOOR`, `MOD`, `RAND`, `TRUNCATE` |
| 날짜 함수 | `NOW`, `CURDATE`, `CURTIME`, `DATE_FORMAT`, `DATEDIFF`, `ADDDATE` |
| 조건 함수 | `IF`, `IFNULL`, `NULLIF`, `CASE WHEN` |
| 형변환 함수 | `CAST`, `CONVERT` |
| 집계 함수 | `COUNT`, `AVG`, `SUM`, `MAX`, `MIN` |

---

## 17. 문자열 함수

```sql
-- 문자열 연결
SELECT CONCAT(address1, ' ', address2, ' ', address3) AS 주소
FROM member;

-- 왼쪽 3글자 추출
SELECT userid, LEFT(userid, 3) AS 아이디앞부분
FROM member;

-- 전화번호에서 '-' 제거
SELECT hp, REPLACE(hp, '-', '') AS 번호
FROM member;

-- 이메일 대문자 변환
SELECT email, UPPER(email) AS 대문자
FROM member;
```

자주 사용하는 문자열 함수:

| 함수 | 의미 |
| --- | --- |
| `CONCAT()` | 문자열 연결 |
| `LEFT()` | 왼쪽 일부 추출 |
| `RIGHT()` | 오른쪽 일부 추출 |
| `SUBSTRING()` | 문자열 일부 추출 |
| `CHAR_LENGTH()` | 문자 개수 |
| `LENGTH()` | 바이트 수 |
| `TRIM()` | 공백 제거 |
| `REPLACE()` | 문자열 치환 |
| `LOWER()` | 소문자 변환 |
| `UPPER()` | 대문자 변환 |

---

## 18. 수학 함수

```sql
SELECT ABS(-100);
SELECT ROUND(3.141592, 2);
SELECT CEIL(3.9);
SELECT FLOOR(3.9);
SELECT MOD(10, 3);
SELECT TRUNCATE(3.141592, 2);
```

랜덤 회원 1명 조회:

```sql
SELECT *
FROM member
ORDER BY RAND()
LIMIT 1;
```

---

## 19. 날짜 함수

```sql
-- 현재 날짜와 시간
SELECT NOW();

-- 현재 날짜
SELECT CURDATE();

-- 현재 시간
SELECT CURTIME();

-- 날짜 형식 변경
SELECT DATE_FORMAT(NOW(), '%Y/%m/%d');

-- 날짜 차이 계산
SELECT DATEDIFF(NOW(), regdate)
FROM member;

-- 현재 날짜에서 30일 더하기
SELECT ADDDATE(NOW(), 30);
```

`DATE_FORMAT()`에서 자주 사용하는 형식:

| 포맷 | 의미 |
| --- | --- |
| `%Y` | 4자리 연도 |
| `%m` | 2자리 월 |
| `%d` | 2자리 일 |
| `%H` | 시 |
| `%i` | 분 |
| `%s` | 초 |

---

## 20. 조건 함수

```sql
-- 조건이 하나일 때
SELECT userid, IF(point >= 100, 'VIP', '일반') AS 등급
FROM member;

-- NULL 값 처리
SELECT userid, IFNULL(regdate, '가입일 없음') AS 가입일
FROM member;

-- 두 값이 같으면 NULL 반환
SELECT NULLIF(10, 10);
```

조건이 여러 개일 때는 `CASE WHEN`을 사용한다.

```sql
SELECT userid,
CASE
    WHEN point >= 200 THEN 'VIP'
    WHEN point >= 100 THEN 'GOLD'
    ELSE 'NORMAL'
END AS 등급
FROM member;
```

---

## 21. 형변환 함수

```sql
-- 문자열을 날짜 타입으로 변환
SELECT CAST('2026-06-08' AS DATETIME);

-- 문자열을 정수 타입으로 변환
SELECT CONVERT('-123', SIGNED);
SELECT CONVERT('-123', UNSIGNED);
```

`SIGNED`는 음수를 허용하는 정수형이고, `UNSIGNED`는 음수를 허용하지 않는 정수형이다.

---

## 22. 집계 함수

집계 함수는 여러 행의 값을 하나로 요약할 때 사용한다.

```sql
SELECT COUNT(idx) FROM member;
SELECT AVG(point) FROM member;
SELECT SUM(point) FROM member;
SELECT MAX(point) FROM member;
SELECT MIN(point) FROM member;
```

| 함수 | 의미 |
| --- | --- |
| `COUNT()` | 개수 |
| `AVG()` | 평균 |
| `SUM()` | 합계 |
| `MAX()` | 최댓값 |
| `MIN()` | 최솟값 |

---

## 23. 정리

오늘 배운 내용은 데이터를 더 정교하게 조회하고 관리하기 위한 기능들이다.

서브쿼리를 사용하면 기준값을 직접 입력하지 않고 데이터에서 동적으로 가져올 수 있다.  
`UNION`은 여러 조회 결과를 하나로 합칠 때 사용한다.  
사용자 계정과 권한 관리는 데이터베이스 보안의 기본이다.  
MySQL 함수는 문자열, 숫자, 날짜 데이터를 SQL 단계에서 바로 가공할 수 있게 해준다.

특히 데이터 분석에서는 SQL에서 필요한 전처리를 먼저 수행하면 Python이나 Excel로 데이터를 가져온 뒤의 작업이 훨씬 깔끔해진다.