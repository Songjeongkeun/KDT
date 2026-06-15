-- 데이터 베이스 확인하기
show databases;

-- 데이터 베이스 생성하기
create database ai;
/* 
	테이블
    - 데이터를 행과 열로 스키마(테이블의 형태)에 따라 저장할 수 있는 구조
    create table 테이블명(
		컬럼명1 데이터타입1 제약조건1,
        컬럼명2 데이터타입2 제약조건2,
        컬럼명3 데이터타입3 제약조건3,
        ...)
	데이터 타입
    - 정수: int, bigint
    - 실수: float, double, decimal(소수점 자리수를 고정할 수 있다)
    - 문자형: char, varchar(최대 65535byte), text, binary, varbinaty(글자 이외의 것들을 저장할 때 사)
    - 날짜형: date, time, datetime, timestamp(1970-1-1-00:00 시작해서, 1ms 만큼 증가하는 숫자값, 날짜의 덧셈뺄셈을 구하기 위해 사용)
    
    제약 조건
    - 데이터의 무결성을 지키기 위해 데이터를 입력받을 때 실행되는 검사 규칙
    - not null: null 값을 허용하지 않음
    - unique: 중복값을 허용하지 않음. null 값은 허용
    - default: null 값을 삽입할 때 기본이 되는 값을 설정
    - primary key
		1. null 값을 허용하지 않음
        2. 중복값을 허용하지 않음
        3. 인덱싱 설정
        4. 기본키로 설정. 참조(외래)키와 쌍으로 연결
	- foreign key : 기본키와 쌍으로 연결
    - auto_increment: 데이터를 직접 삽입하지 못함. 자동 증가되는 숫자를 삽입.
    
	스키마
    - 데이터베이스의 구조와 제약조건에 관한 명세를 기술한 집합
*/ 

-- 데이터베이스 선택하기
use ai;

-- 테이블 만들기
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

-- 테이블 확인하기
desc member;

-- 테이블 삭제하기
drop table member;

-- 컬럼 삭제하기
alter table member drop point;

-- 컬럼 추가하기
alter table member add point int default 1000;

-- 컬럼 수정하기
alter table member modify column point int default 100;

/*
	DDL(Database Definition Language, 데이터 정의어)
    create: 데이터베이스, 테이블, 뷰 등을 생성
    alter: 기존 객체(테이블, 뷰 등)의 구조를 변경
    drop: 객체(데이터베이스, 테이블, 뷰, 인덱스 등)를 완전히 삭제
    truncate: 테이블의 모든 데이터를 삭제하지만, 구조는 남김(롤백 불가)
*/