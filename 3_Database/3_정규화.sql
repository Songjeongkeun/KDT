/*
	
    정규화(Normalization) 
    - 데이터베이스 테이블을 효율적으로 구조화하는 작업
    - 중복 데이터를 줄이고, 데이터가 꼬이지 않게 테이블을 나누는 과정
    - 데이터 무결성 유지,유지보수 편리성 증가
    
    정규화 단계
    1. 제1정규형(1NF)
		- 하나의 칸에는 하나의 값만 들어가야 함
        ex) MySQL, Python (x)
    2. 제2정규형(2NF)
		- 1NF 를 만족
        - 기본키(Primary Key) 전체에 완전 종속되어야 함
    3. 제3정규형(3NF)
		- 2NF 만족
        - 이행적 종속 제거
	* 이행적 종속 
		학번 -> 학과번호 
        학과번호 -> 학과명
        학번 -> 학과명 : 간접 연결을 이행적 종속이라고 함
*/

-- 학생 student
create table student(
	student_id int primary key,
    student_name varchar(20)
);

-- 교수 professor
create table professor(
	professor_id int primary key,
    professor_name varchar(20),
    professor_phone varchar(20)
);

-- 과목 course
create table course(
	course_id int primary key,
	course_name varchar(50),
    professor_id int,
    foreign key (professor_id) references professor(professor_id)
);

-- drop table enroll; 
-- 수강 enroll
create table enroll(
	student_id int,
    course_id int,
    foreign key (student_id) references student(student_id),
    foreign key (course_id) references course(course_id),
    primary key (student_id)
);

-- 제 4정규화 : 너무 정규화를 하면 속도의 저하를 시키므로, 성능 최적화를 위해서 비 정규화하는 형태라고 한다.

select * from member;

create table profile(
	idx int not null,
    height double,
    weight double,
    mbti varchar(10),
    foreign key(idx) references member(idx)
);

select * from profile;

insert into profile values (1, 160, 50, 'ISTJ');
insert into profile values (3, 170, 70, 'ESTP');
insert into profile values (4, 175, 80, 'ENFJ');
insert into profile values (6, 175, 80, 'ENFJ');
-- insert into profile vlaues(7, 175, 80, 'ENFJ'); 외래키 제약조건 위배

-- idx, ueerid, name, gender, mbti
select member.idx, userid, name, gender, mbti from member inner join profile 
on member.idx = profile.idx;

select m.idx, m.userid, m.name, m.gender, p.mbti from member as m inner join profile as p
on m.idx = p.idx;
-- member as m = member m 

select m.idx, m.userid, m.name, m.gender, p.mbti from member as m left join profile as p
on m.idx = p.idx;

select m.idx, m.userid, m.name, m.gender, p.mbti from member as m right join profile as p
on m.idx = p.idx;

select userid, name, gender, mbti from member cross join profile;