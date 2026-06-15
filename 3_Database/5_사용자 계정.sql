/*
	사용자 계정
    - 데이터베이스에 접속할 수 있는 로그인 계정
    - root 계정은 모든 권한을 가진 계정이기 때문에 실제 사용시 위험할 수 있음
    - 프로젝트별로 계정을 따로 만들고, 필요한 권한만 부여하는 것이 일반적 
*/

-- create user '계정명'@'접속위치' identified by '비밀번호';
-- localhost : 같은 컴퓨터(내 컴퓨터)에서만 접속 외부에서는 접속 X
-- 'apple'@'%' : 어디서든 접속 가능
-- 'apple'@'192.168.0.%' : 192.168.0. 으로 시작하는 내부망에서만 접속 가능
-- 'apple'@'192.168.0.10' : 특정 ip 에서만 접속이 가능하다.

create user 'apple'@'localhost' identified by '1111';

-- grnat 권한종류 on 데이터베이스명.테이블명 새 '계정명'@'접속위치';
-- 권한종류
-- all : 모든 일반 권한. select, insert, update, delete, create, drop, alter, index 
-- ai.* : ai 데이터베이스 안의 모든 테이블
-- *.* : 모든 데이터베이스 안의 모든 테이블 이란 의미
grant all on ai.* to 'apple'@'localhost';

show grants for 'apple'@'localhost';

create user 'banana'@'localhost' identified by '2222';
grant select on ai.* to 'banana'@'localhost';

create user 'orange'@'localhost' identified by '3333';
grant select on ai.* to 'orange'@'localhost';
-- 권한 회수
revoke delete on ai.* from 'orange'@'localhost';

-- 사용자 비밀번호 변경
alter user 'banana'@'localhost' identified by '1004';

-- 사용자 삭제
drop user 'banana'@'localhost';

create database testdb;
use testdb;
create table member(
	idx int auto_increment primary key,
    userid varchar(20) unique not null,
    userpw varchar(20) not null,
    name varchar(20) not null,
    hp varchar(20) not null,
    email varchar(50) not null,
    ssn1 char(6) not null,
    ssn2 char(7) not null,
    zipcode varchar(5),
    address1 varchar(100),
    address2 varchar(100),
    address3 varchar(100),
    regdate datetime default now(),
    point int default 1000
);

select * from member;
alter table member add gender varchar(10) not null;
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('apple', '1111', '김사과', '010-1111-1111', 'apple@apple.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
-- insert into member 을 못 쓰는 이유 : auto increment 를 설정한 column 이 있기 때문이다.
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('banana', '2222', '반하나', '010-2222-2222', 'banana@banana.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('orange', '3333', '오렌지', '010-3333-3333', 'orange@orange.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '남자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('melon', '4444', '이메론', '010-4444-4444', 'melon@melon.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '남자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('cherry', '5555', '채리', '010-5555-5555', 'cherry@cherry.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender, regdate) values ('berry', '6666', '배애리', '010-6666-6666', 'berry@berry.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자', null);

create user 'user1'@'192.168.162.34' identified by '1111';
-- Error Code: 1396. Operation CREATE USER failed for 'user1'@'192.168.162.34' (User account already exists)
create user 'user2'@'192.168.12.4' identified by '1111';

grant select, update, insert on testdb.* to 'user1'@'192.168.162.34';
grant select, update, insert on testdb.* to 'user2'@'192.168.12.4'; 
