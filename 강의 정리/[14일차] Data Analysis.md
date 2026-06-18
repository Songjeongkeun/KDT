# [14일차] Data Analysis

## 1. View란?

View는 `SELECT` 문을 저장해두고 테이블처럼 사용할 수 있게 만든 데이터베이스 객체이다.

```text
원본 테이블
    ↓ SELECT 실행
View
    ↓
사용자에게 필요한 결과만 제공
```

View는 실제 데이터를 별도로 저장하는 일반 테이블이 아니다.  
View를 조회하면 저장된 `SELECT` 문을 바탕으로 원본 테이블의 데이터를 보여준다.

```sql
CREATE VIEW 뷰이름 AS
SELECT 컬럼
FROM 테이블
WHERE 조건;
```

---

## 2. View를 사용하는 이유

### 2.1 복잡한 SQL 단순화

JOIN, 함수, 조건식이 포함된 복잡한 SQL을 View에 저장하면 이후에는 간단한 이름으로 조회할 수 있다.

```sql
SELECT *
FROM member_order;
```

### 2.2 재사용

자주 사용하는 조회문을 매번 다시 작성하지 않아도 된다.

### 2.3 가독성

긴 SQL에 의미 있는 View 이름을 붙이면 코드의 목적을 이해하기 쉬워진다.

```text
member_order → 회원별 주문 정보
member_address → 회원 주소 정보
vip_member → 우수 회원 정보
```

### 2.4 보안

원본 테이블의 모든 컬럼을 공개하지 않고, 필요한 컬럼만 View로 제공할 수 있다.

예를 들어 `member` 테이블에 비밀번호나 민감정보가 있더라도 View에서는 공개하지 않을 수 있다.

```sql
CREATE VIEW public_member AS
SELECT userid, name, email
FROM member;
```

---

## 3. 일반 테이블과 View 비교

| 구분           | 일반 테이블            | View                             |
| -------------- | ---------------------- | -------------------------------- |
| 데이터 저장    | 데이터를 직접 저장한다 | 일반적으로 조회문만 저장한다     |
| 조회 방법      | `SELECT` 사용          | 테이블과 동일하게 `SELECT` 사용  |
| 목적           | 실제 데이터 관리       | 조회 단순화, 재사용, 보안        |
| 원본 변경 반영 | 테이블 자체가 원본이다 | 원본 테이블 변경 결과가 반영된다 |
| 정의 확인      | `SHOW CREATE TABLE`    | `SHOW CREATE VIEW`               |

---

## 4. 기본 View 생성

포인트가 100 이상인 회원을 조회하는 View를 만들어보자.

```sql
CREATE VIEW vip_member AS
SELECT userid, name, point
FROM member
WHERE point >= 100;
```

`vip_member` View에는 다음 조회문이 저장된다.

```sql
SELECT userid, name, point
FROM member
WHERE point >= 100;
```

View를 테이블처럼 조회할 수 있다.

```sql
SELECT *
FROM vip_member;
```

출력 예시:

```text
+----------+--------+-------+
| userid   | name   | point |
+----------+--------+-------+
| apple    | 김사과 |   150 |
| banana   | 반하나 |   250 |
| orange   | 오렌지 |   150 |
+----------+--------+-------+
```

---

## 5. View에 추가 조건 사용하기

View를 조회할 때 다시 `WHERE`, `ORDER BY`, `LIMIT` 등을 사용할 수 있다.

```sql
SELECT *
FROM vip_member
WHERE point >= 150;
```

포인트가 높은 회원부터 정렬할 수도 있다.

```sql
SELECT *
FROM vip_member
ORDER BY point DESC;
```

상위 3명만 조회하는 예시는 다음과 같다.

```sql
SELECT *
FROM vip_member
ORDER BY point DESC
LIMIT 3;
```

동작 흐름은 다음처럼 이해할 수 있다.

```text
member 테이블
    ↓ point >= 100
vip_member View
    ↓ point >= 150
최종 조회 결과
```

---

## 6. 문자열을 결합한 View

회원 주소가 여러 컬럼으로 나뉘어 있다고 가정해보자.

```text
address1: 기본 주소
address2: 상세 주소
address3: 참고 주소
```

`CONCAT()`을 사용하면 여러 주소 컬럼을 하나로 합쳐서 보여줄 수 있다.

```sql
CREATE VIEW member_address AS
SELECT
    userid,
    name,
    CONCAT(address1, ' ', address2, ' ', address3) AS address
FROM member;
```

조회:

```sql
SELECT *
FROM member_address;
```

출력 예시:

```text
+----------+--------+------------------------------+
| userid   | name   | address                      |
+----------+--------+------------------------------+
| apple    | 김사과 	 | 서울 서초구 양재동 111-11   		  |
| banana   | 반하나 	 | 서울 강남구 역삼동 222-22   	 	  |
+----------+--------+------------------------------+
```

### NULL이 포함된 주소 처리

MySQL의 `CONCAT()`은 전달된 값 중 하나라도 `NULL`이면 전체 결과가 `NULL`이 된다.

주소에 `NULL`이 있을 수 있다면 `CONCAT_WS()`가 더 편리하다.

```sql
CREATE OR REPLACE VIEW member_address AS
SELECT
    userid,
    name,
    CONCAT_WS(' ', address1, address2, address3) AS address
FROM member;
```

`CONCAT_WS()`는 구분자를 첫 번째 인자로 받고 `NULL` 값을 건너뛴다.

---

## 7. View 수정

기존 View의 조회문을 변경할 때 `CREATE OR REPLACE VIEW`를 사용할 수 있다.

기존 `vip_member`에 이메일 컬럼을 추가해보자.

```sql
CREATE OR REPLACE VIEW vip_member AS
SELECT userid, name, point, email
FROM member
WHERE point >= 100;
```

확인:

```sql
SELECT *
FROM vip_member;
```

`OR REPLACE`를 사용하면 같은 이름의 View가 있을 때 기존 정의를 새로운 정의로 교체한다.

---

## 8. View 구조 확인

View가 어떤 `SELECT` 문으로 만들어졌는지 확인하려면 `SHOW CREATE VIEW`를 사용한다.

```sql
SHOW CREATE VIEW vip_member;
```

간단한 컬럼 구조는 `DESC`로 확인할 수 있다.

```sql
DESC vip_member;
```

주의할 점은 View를 삭제하기 전에 구조를 확인해야 한다는 것이다.

```sql
SHOW CREATE VIEW vip_member;
DROP VIEW vip_member;
```

삭제한 뒤 `SHOW CREATE VIEW`를 실행하면 View가 존재하지 않는다는 오류가 발생한다.

---

## 9. View 목록 확인

현재 데이터베이스의 View 목록은 다음과 같이 확인한다.

```sql
SHOW FULL TABLES
WHERE TABLE_TYPE = 'VIEW';
```

`information_schema`를 이용하는 방법도 있다.

```sql
SELECT TABLE_NAME
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = DATABASE();
```

---

## 10. View 삭제

View를 삭제할 때는 `DROP VIEW`를 사용한다.

```sql
DROP VIEW vip_member;
```

View가 존재하지 않을 때 발생하는 오류를 피하려면 `IF EXISTS`를 사용할 수 있다.

```sql
DROP VIEW IF EXISTS vip_member;
```

View를 삭제해도 원본 테이블과 원본 데이터는 삭제되지 않는다.

```text
vip_member View 삭제
        ↓
member 테이블은 그대로 유지
```

---

## 11. JOIN 결과를 View로 만들기

View에는 단일 테이블뿐 아니라 JOIN을 포함한 조회문도 저장할 수 있다.

회원 테이블과 주문 테이블이 다음 관계를 가진다고 가정한다.

```text
member
├── idx
├── userid
└── name

orders
├── order_id
├── member_idx
├── product_name
├── price
└── order_date
```

`orders.member_idx`는 `member.idx`를 참조한다.

일반 JOIN 조회:

```sql
SELECT
    m.userid,
    m.name,
    o.product_name,
    o.price,
    o.order_date
FROM member AS m
INNER JOIN orders AS o
    ON m.idx = o.member_idx;
```

이 조회문을 `member_order` View로 만든다.

```sql
CREATE VIEW member_order AS
SELECT
    m.userid,
    m.name,
    o.product_name,
    o.price,
    o.order_date
FROM member AS m
INNER JOIN orders AS o
    ON m.idx = o.member_idx;
```

이후에는 복잡한 JOIN을 다시 작성하지 않고 다음처럼 조회할 수 있다.

```sql
SELECT *
FROM member_order;
```

출력 예시:

```text
+----------+--------+--------------+-------+------------+
| userid   | name   | product_name | price | order_date |
+----------+--------+--------------+-------+------------+
| apple    | 김사과 | 노트북       | 1500000 | 2026-06-09 |
| banana   | 반하나 | 키보드       |  120000 | 2026-06-09 |
+----------+--------+--------------+-------+------------+
```

---

## 12. JOIN View에 조건 추가

특정 회원의 주문만 조회할 수 있다.

```sql
SELECT *
FROM member_order
WHERE userid = 'apple';
```

가격이 10만 원 이상인 주문을 조회할 수도 있다.

```sql
SELECT *
FROM member_order
WHERE price >= 100000
ORDER BY price DESC;
```

주문일 기준으로 조회하는 예시는 다음과 같다.

```sql
SELECT *
FROM member_order
WHERE order_date >= '2026-06-01'
ORDER BY order_date DESC;
```

---

## 13. View를 이용한 보안

`member` 테이블에는 다음처럼 외부에 노출하면 안 되는 정보가 포함될 수 있다.

```text
userpw
주민등록번호
상세주소
내부 관리 데이터
```

안전한 컬럼만 포함한 View를 만들 수 있다.

```sql
CREATE VIEW member_public AS
SELECT userid, name, email
FROM member;
```

특정 DB 사용자에게 원본 테이블 권한은 주지 않고 View 조회 권한만 부여할 수도 있다.

```sql
GRANT SELECT
ON ai.member_public
TO 'viewer'@'localhost';
```

```text
viewer 사용자
    ↓ 조회 가능
member_public View
    ↓
userid, name, email만 공개
```

View는 컬럼 노출 범위를 줄이는 데 도움이 되지만, 이것만으로 모든 보안 문제가 해결되는 것은 아니다.  
사용자 권한, 비밀번호 관리, 애플리케이션 인증도 함께 구성해야 한다.

---

## 14. 로그인 쿼리와 보안

회원 로그인 여부를 확인하는 기본 SQL은 다음과 같다.

```sql
SELECT idx, userid, name
FROM member
WHERE userid = 'example_user'
  AND userpw = 'example_password';
```

하지만 실제 애플리케이션에서는 입력값을 문자열로 SQL에 직접 연결하면 안 된다.

Python과 `mysqlclient`를 사용한다면 매개변수 바인딩을 사용한다.

```python
sql = """
    SELECT idx, userid, name
    FROM member
    WHERE userid = %s
      AND userpw = %s
"""

cur.execute(sql, (userid, userpw))
member = cur.fetchone()
```

또한 실제 서비스에서는 비밀번호를 평문으로 저장하거나 SQL에서 평문 그대로 비교하지 않는다.

```text
회원가입:
비밀번호 → 안전한 해시 함수 → 해시 결과 저장

로그인:
입력 비밀번호 → 저장된 해시와 검증
```

View는 로그인용 민감정보를 공개하는 용도로 사용하면 안 된다.

---

## 15. View를 통해 데이터를 수정할 수 있을까?

일부 단순한 View는 `INSERT`, `UPDATE`, `DELETE`가 가능하다.

예를 들어 단일 테이블을 기반으로 하고 집계나 그룹화가 없는 View는 수정 가능한 경우가 있다.

```sql
CREATE VIEW member_point AS
SELECT idx, userid, point
FROM member;
```

```sql
UPDATE member_point
SET point = 200
WHERE idx = 1;
```

이 경우 원본 `member` 테이블의 데이터가 변경될 수 있다.

하지만 다음 요소가 포함된 View는 수정이 제한될 수 있다.

- `GROUP BY`
- 집계함수
- `DISTINCT`
- `UNION`
- 복잡한 JOIN
- 계산된 컬럼

View는 기본적으로 조회 목적으로 사용하는 편이 이해하기 쉽고 안전하다.

---

## 16. WITH CHECK OPTION

수정 가능한 View를 통해 View의 조건을 벗어나는 데이터가 만들어지는 것을 막으려면 `WITH CHECK OPTION`을 사용할 수 있다.

```sql
CREATE OR REPLACE VIEW vip_member AS
SELECT idx, userid, name, point
FROM member
WHERE point >= 100
WITH CHECK OPTION;
```

다음 수정은 View 조건을 만족한다.

```sql
UPDATE vip_member
SET point = 200
WHERE idx = 1;
```

하지만 포인트를 100 미만으로 변경하면 View 조건을 벗어나므로 오류가 발생할 수 있다.

```sql
UPDATE vip_member
SET point = 50
WHERE idx = 1;
```

---

## 17. View 사용 시 주의점

### 성능이 자동으로 빨라지는 것은 아니다

일반 View는 조회 결과를 미리 저장하지 않는다.  
View를 조회할 때 원본 SQL이 실행되므로 복잡한 JOIN이나 함수가 포함되어 있으면 비용이 발생한다.

```text
View 생성 = 성능 최적화
```

위 공식이 항상 성립하는 것은 아니다.

### 원본 컬럼 변경의 영향

View가 참조하는 원본 컬럼을 삭제하거나 이름을 변경하면 View가 정상적으로 동작하지 않을 수 있다.

### View 중첩

View가 다른 View를 참조하도록 여러 단계로 중첩하면 실제 실행 SQL을 이해하기 어려워질 수 있다.

### ORDER BY 보장

View 정의 안에 정렬이 있더라도 최종 출력 순서를 확실하게 보장하려면 View를 조회할 때 `ORDER BY`를 명시하는 것이 좋다.

```sql
SELECT *
FROM vip_member
ORDER BY point DESC;
```

---

## 18. View 실행 순서 예시

오늘 학습한 내용을 순서대로 실행하면 다음과 같다.

```sql
USE ai;

-- 1. VIP 회원 View 생성
CREATE VIEW vip_member AS
SELECT userid, name, point
FROM member
WHERE point >= 100;

-- 2. View 조회
SELECT *
FROM vip_member;

-- 3. 추가 조건 조회
SELECT *
FROM vip_member
WHERE point >= 150;

-- 4. 주소 View 생성
CREATE VIEW member_address AS
SELECT
    userid,
    name,
    CONCAT_WS(' ', address1, address2, address3) AS address
FROM member;

-- 5. 주소 View 조회
SELECT *
FROM member_address;

-- 6. VIP View 수정
CREATE OR REPLACE VIEW vip_member AS
SELECT userid, name, point, email
FROM member
WHERE point >= 100;

-- 7. View 정의 확인
SHOW CREATE VIEW vip_member;

-- 8. View 목록 확인
SHOW FULL TABLES
WHERE TABLE_TYPE = 'VIEW';

-- 9. View 삭제
DROP VIEW IF EXISTS vip_member;
```

---

## 19. 핵심 정리

| 명령어                   | 설명                           |
| ------------------------ | ------------------------------ |
| `CREATE VIEW`            | 새로운 View 생성               |
| `CREATE OR REPLACE VIEW` | 기존 View 생성 또는 수정       |
| `SELECT ... FROM view`   | View 조회                      |
| `SHOW CREATE VIEW`       | View 정의 확인                 |
| `SHOW FULL TABLES`       | View 목록 확인                 |
| `DROP VIEW`              | View 삭제                      |
| `WITH CHECK OPTION`      | View 조건을 벗어나는 변경 제한 |

View의 핵심은 다음과 같이 정리할 수 있다.

```text
복잡한 SELECT 문을 저장한다.
        ↓
테이블처럼 간단하게 재사용한다.
        ↓
필요한 컬럼만 공개해 가독성과 보안을 높인다.
```

View는 데이터를 직접 저장하는 일반 테이블이 아니라 원본 테이블을 바라보는 가상의 테이블이다.  
잘 활용하면 반복되는 SQL을 줄이고 데이터 접근 구조를 더 명확하게 만들 수 있다.