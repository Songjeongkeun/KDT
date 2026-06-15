/*
	서브쿼리(Sub Query)
	- 서브쿼리는 SQL문 안에 들어가는 또 다른 SELECT 문
    * select ... from where 컬럼  = (select ... );
    * 김사과보다 포인트가 많은 회원을 검색
    select point from member where name = '김사과';
    select * from member where point > 150;
    = select * from member where point > (select point from member where name = '김사과');
*/
use ai;
-- 1. 단일 행 서브쿼리
-- 결과가 하나의 값만 나오는 서브쿼리
-- 포인트가 가장 높은 회원을 검색
select * from member where point = (select max(point) from member);

-- 2. 다중 행 서브쿼리
-- 결과가 여러개 나오는 서브쿼리
-- in, any, all 을 사용
-- 포인트가 200 이상인 userid 목록에 포함된 회원을 검색
select * from member where userid in (select userid from member where point >= 150);

-- 3. from 절 서브쿼리
-- 서브쿼리 결과를 임시 테이블처럼 사용하는 방식
select name, point from (select name, point from member where point >= 150) as high_point_member;

-- 4. select 절 서브쿼리
-- 조회 결과에 서브쿼리 결과를 함께 보여주는 방식
-- 각 회원의 포인트와 전체 평균 포인트를 함께 검색
select name, point, (select avg(point) from member) as avg_point from member;

-- 5 exists 서브쿼리
-- 존재 여부를 확인할 때 사용
-- 주문 내역이 있는 회원을 검색
select * from member m where exists (select 1 from orders o where o.member_idx = m.idx);

create table orders (
    order_id int auto_increment primary key,
    member_idx int not null,
    product_name varchar(100) not null,
    price int not null,
    order_date datetime default now(),
    foreign key (member_idx) references member(idx)
);

insert into orders(member_idx, product_name, price)
values
(1, '키보드', 50000),
(1, '마우스', 30000),
(2, '모니터', 250000),
(2, '노트북 거치대', 40000),
(3, 'USB', 15000),
(4, '노트북', 1200000),
(4, '헤드셋', 90000);

select * from orders;
select * from member;

-- 1. 주문한 적이 있는 회원들만 조회
select * from member where idx in (select member_idx from orders);

-- 2. 주문한 적이 없는 회원들만 조회
select * from member where idx not in (select member_idx from orders);

-- 3. 가장 비싼 상품을 주문한 회원 조회
select * from member where idx =(select member_idx from orders where price = (select max(price) from orders));

-- 가장 비싼 상품을 주문한 회원의 이름과 상품명을 조회
select m.name, o.product_name from member m inner join orders o on m.idx = o.member_idx where o.price = (select max(price) from orders);


create table orders_copy (
    order_id int auto_increment primary key,
    member_idx int not null,
    product_name varchar(100) not null,
    price int not null,
    order_date datetime default now(),
    foreign key (member_idx) references member(idx)
);

select * from orders_copy;
select * from orders; 
insert into orders_copy(select * from orders);
-- 테이블 형태가 같을 때 사용 가능하다.

create table orders_copy_copy(select * from orders);
select * from orders_copy_copy;

/*
	UNION
    - 여러 개의 select 결과를 하나로 합쳐주는 기능
    - 조회 결과를 위아래로 이어 붙이는 기능
    
*/

select * from member;

-- 서울 회원 + 부산 회원 합치기
select name, address1 from member where address1 like '서울%';
select name, address1 from member where address1 like '부산%';

select name, address1 from member where address1 like '서울%'
union
select name, address1 from member where address1 like '부산%';

select * from voca;

create table voca_new (
	eng varchar(50) primary key,
    kor varchar(50) not null,
    lev int default 1,
    regdate datetime default now()
);

insert into voca_new values('pineapple', '파인애플', 2, now());
insert into voca_new values('papaya', '파파야', 2, now());
insert into voca_new values('blueberry', '블루베리', 1, now());
select * from voca_new;
select eng, kor, lev from voca union select eng, kor, lev from voca_new;
insert into voca_new values('apple', '사과', 1, now());
-- union은 중복데이터를 삭제
select eng, kor, lev from voca union select eng, kor, lev from voca_new;
-- regdate가 다르기 때문에 중복데이터가 아님
select eng, kor, lev, regdate from voca union select eng, kor, lev, regdate from voca_new;

-- union all: 중복 데이터를 제거하지 않음
select eng, kor, lev from voca union all select eng, kor, lev from voca_new;
