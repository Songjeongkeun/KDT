/*
	DML (Data Manipulation Language, 데이터 조작어)
	select: 데이터를 조회(검색)
    insert: 데이터를 테이블에 삽입
    update: 데이터를 수정
    delete: 데이터를 삭제
*/
create table voca (
	eng varchar(50) primary key,
    kor varchar(50) not null,
    lev int default 1,
    regdate datetime default now()
);

use ai;
desc voca;


insert into voca values ('apple', '사과', 1, now());
select * from voca;
insert into voca(eng, kor) values ('banana', '바나나');
-- Error Code: 1062. Duplicate entry 'orange' for key 'voca.PRIMARY'
insert into voca values ('orange','오렌지',null,null);
insert into voca (eng, kor) values ('melon','메론');
insert into voca (eng, kor, lev) values ('avocado','아보카도',2);

delete from voca; -- truncate 와 결과는 같지만, truncate 는 복구가 안되지만 delete 는 복구가 된다.
-- Error Code: 1175. You are using safe update mode and you tried to update a table without a WHERE that uses a KEY column.  To disable safe mode, toggle the option in Preferences -> SQL Editor and reconnect.

delete from voca where eng = 'banana'; -- where 절 뒤에 = 는 같다라는 의미, where 절 앞에 = 는 대입

update voca set lev = 1;
update voca set lev = 2 where eng = 'avocado';

desc member; -- schema 보는 법
alter table member add gender varchar(10) not null;
-- 기존 테이블에 데이터 값이 있을 때 조심해서 사용해야 한다.

select * from member;
-- 회원가입
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('apple', '1111', '김사과', '010-1111-1111', 'apple@apple.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
-- insert into member 을 못 쓰는 이유 : auto increment 를 설정한 column 이 있기 때문이다.
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('banana', '2222', '반하나', '010-2222-2222', 'banana@banana.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('orange', '3333', '오렌지', '010-3333-3333', 'orange@orange.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '남자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('melon', '4444', '이메론', '010-4444-4444', 'melon@melon.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '남자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('cherry', '5555', '채리', '010-5555-5555', 'cherry@cherry.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender, regdate) values ('berry', '6666', '배애리', '010-6666-6666', 'berry@berry.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자', null);

-- auto increment 를 준 column 에 primary key 를 줘야한다. (MySQL 특징)
-- 한 table 에 pirmary key 는 한개만 가져야 한다. (MySQL 특징)

-- 150 250 150 150 50 200
update member set point = 0 where idx = 5;
update member set point = point + 50;
update member set point = point + 100 where idx = 2;
update member set point = 100 where idx = 6;
-- update member set point = point + 100 where userid = 'banana', 같은 결과이지만 primary key 로 잡는게 속도가 빨라서 primary key 로 잡아준다.

select * from member;
-- 이런 query 는 실제 개발에서 사용할 때 조심해야 한다.
select userid from member;
select userid, name from member;
select hp, userid, name from member;

select 100;
select 100 + 50;
select 100 + 50 as 덧셈;
select 100 + 50 as '덧셈 연산';
select ''; -- 빈 문자열
select null; -- 데이터가 없음
select 100 + '';
select 100 + null; -- null 과의 연산은 무조건 null 이다.


/*
	산술 연산자 : +, -, *, /, mod(나머지), div(몫)
    비교 연산자 : =, <, >, <=, >=, <>(다르다)
    대입 연산자 : =
    논리 연산자 : and, or, not, xor
    is : 양쪽의 피연사자가 모두 같으면 true, 같지 않으면 false, 데이터가 나오고, 안나오고의 차이다.
	between A and B : A 보다는 크거나 같고, B 보다는 작거나 같으면 true, 아니면 false
    in : 매개변수로 전달된 리스트에 값이 존재하면 true, 아니면 false
    like : 패턴으로 문자열을 검색하여 값이 존재하면 true, 아니면 false
    
*/ 

-- 포인트가 150이상인, 멤버의 아이디, 이름, 포인트를 검색
select userid, name, point from member where point >= 150;

-- 포인트가 150이상이고, 200이하인 멤버의 아이디, 이름, 포인트, 성별을 검색
select userid, name, point, gender from member where point between 150 and 200;

-- 로그인
select userid from member where userid='apple' and userpw='1111'; -- 성공
select userid from member where userid='apple' and userpw='2222'; -- 실패

-- 이름이 김사과, 반하나, 오렌지인 사람의 모든 정보를 검색
select * from member where name = '김사과' or name = '반하나' or name = '오렌지';
select * from member where name in ('김사과', '반하나', '오렌지');

-- regdate 가 null 인 멤버를 검색
select * from member where regdate is null;
select * from member where regdate is not null;

-- 아이디가 a로 시작하는 멤의의 정보를 검색
select * from member where userid like 'a%';
-- 아이디가 a로 끝나는 멤버의 정보를 검색
select * from member where userid like '%a';
-- 아이디가 'a'를 포함하는 멤버의 정보를 검색
select * from member where userid like '%a%';

-- 이메일이 .com 으로 끝나는 멤버의 정보를 검색
select * from member where email like '%.com';

-- 이름이 3자인 멤버를 검색
select * from member where name like '___';

-- 이름이 첫 글자가 '김'씨이며 3자인 멤버를 검색
select * from member where name like '김__'; 

select * from member order by idx; -- 오름차순 asc 생략

select * from member order by idx desc;

-- 멤버를 포인트 순으로 정렬
select * from member order by point desc;

-- 멤버를 포인트 순으로 정렬. 단 포인트가 같으면 가입 최신순으로 정렬
select * from member order by point desc, regdate desc;

-- limit : 일부 로우(레코드를) 검색
-- 사용 방법 : limit 검색할 로우의 개수, limit 시작로우(인덱스) 가져올 로우의 개수
select * from member limit 2; -- 한개만 있을 경우 시작로우(인덱스) 가 0 이 default 이다.

select * from member limit 2, 3;

-- 멤버에서 포인트순으로 내림차순 정렬하고 포인트가 같다면 가입순으로 내림차순 한 뒤 top 3를 검색
select * from member order by point desc, regdate desc limit 3;

/*
	group
    select 그룹을 맺을 컬럼 또는 집계함수 from 테이블 group by 그룹을 맺을 컬럼

*/

select gender from member group by gender;

select gender, count(idx) as 인원수 from member group by gender;
select gender, count(idx) as 인원수 from member group by gender having gender ='여자';
select gender, count(idx) as 인원수 from member where gender = '여자' group by gender;

-- 성별로 그룹을 맺고 인원수가 3명 이상인 성별을 검색
select gender, count(idx) as 인원수 from member group by gender having count(idx) > 3;
select gender, count(idx) as 인원수 from member group by gender having 인원수 > 3; -- 앞에서 변수명을 설정해줬기 때문에 뒤에서 변수명 사용 가능

/*
	멤버 중 포인트가 50이상인 멤버중에서 성별로 그룹을 나눈 뒤,
	각 그룹에 포인트 평균을 구하고 평균의 포인트가 100 이상인 성별을 출력
	(단, 성별이 남자, 여자 모두 출력된다면 포안트가 높은 성별을 우선으로 출력)
*/
select * from member;
select gender, avg(point) as 평균 from member where point >= 50 group by gender having 평균 >= 100 order by gender desc;