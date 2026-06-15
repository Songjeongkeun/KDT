/*
	문자열 함수, 수학 함수, 날짜 함수, 조건 함수, 형변환 함수, 집계 함수
*/

-- 문자열 함수
-- concat()
-- 문자열을 이어 붙이는 함수
select concat('안녕하세요', 'MySQL');
use ai;
select concat(address1, ' ', address2, ' ',  address3) as 주소 from member;
-- left(), right()
-- 문자열의 왼쪽/오른쪽 일부를 가져옴
select left('ABCDEFGHIJ', 3); 
select right('ABCDEFGHIJ', 4);
select userid, left(userid, 3) as '아이디 앞부분' from member;
-- substring()
-- 문자열의 일부를 추출
select substring('ABCDEFGHIJ', 3, 4); -- 3번째 문자부터 4글자 추출하기
select ssn1, substring(ssn1, 1, 2) as 출생년도 from member;
-- char_length(), length()
-- 문자 개수, 바이트 수
select char_length('가나다');
select length('가나다'); -- 한글 3byte
-- trim(), ltrim(), rtrim()
-- 공백 제거
select trim('     mysql     ');
-- replace()
-- 문자열 치환
select replace('010-1111-1111', '-', '');
select hp, replace(hp, '-', '') as 번호 from member;
-- lower(), upper()
-- 소문자, 대문자 변환
select upper('mysql');
select email, upper(email) as '대문자' from member;
-- 수학 함수
-- abs()
-- 절댓값
select abs(-100);
-- round()
-- 반올림
select round(3.141592, 2);
-- ceil(), floor()
-- 올림, 내림
select ceil(3.9); 
select floor(3.9);
-- mod()
-- 나머지
select mod(10, 3);
-- rand()
-- 랜덤값 생성(0~1사이의 실수)
select rand();
select * from member order by rand() limit 1;
-- truncate()
-- 버림
select truncate(3.141592, 2);

-- 날짜 함수
-- now()
-- 현재 날짜 + 시간
select now();
-- curdate(), curtime()
select curdate();
select curtime();
-- 운영체제의 시간을 가져옴
-- date_format()
-- 날짜 포멧 변경
select date_format(now(), '%Y년 %m월 %d일 %H시 %i분 %s초');
-- datediff()
-- 날짜 차이 계산
select datediff('2026-12-17', now());
-- adddate()
-- 날짜 더하기
select adddate(now(), 30);
-- dayofweek()
-- 요일 숫자 반환
select dayofweek(now()); -- 1: 일요일, 2: 월요일
-- month(), year(), day()
select year(now());
select month(now());
select day(now());

-- 조건 함수
-- if()
-- 조건 처리
select userid, if(point >= 100, 'VIP', '일반') from member;
-- if null()
-- null 인지 확인, null 처리
select userid, ifnull(regdate, '가입일 없음') from member;
-- nullif()
-- 두 값이 같으면 null 반환
select nullif(10, 10);
-- case when
-- 여러 조건 처리
select userid,
case
	when point >= 200 then 'VIP'
    when point >= 100 then 'GOLD'
    else 'NORMAL'
end as 등급 from member;

-- 형변환 함수
-- cast()
-- 자료형 변경
select cast('2026-06-08' as datetime);

-- convert()
-- 형변환
select convert('-123', signed);
select convert('-123', unsigned);

-- 집계 함수
-- count()
-- 행 개수
select count(idx) from member;
-- avg()
-- 평균
select avg(point) from member;
-- sum()
-- 합계
select sum(point) from member;
-- max(), min()
-- 최댓값, 최솟값
select max(point) from member;
select min(point) from member;

-- 1. userid 앞 3글자만 출력하세요.
select left(userid, 3) from member;
-- 2. 전화번호의 '-'를 제거하세요.
select replace(hp, '-', '') as 번호 from member;
-- 3. 현재 날짜를 yyyy/mm/dd 형식으로 출력하세요.
select date_format(now(), '%Y/%m/%d');
-- 4. point 평균을 구하세요.
select avg(point) from member;
-- 5. point가 가장 높은 회원을 조회하세요.
select userid from member where point = (select max(point) from member);
-- 6. userid를 모두 대문자로 출력하세요.
select upper(userid) from member;
-- 7. 회원 등급을 case when으로 나누세요.
select userid,
case
	when point >= 200 then 'VIP'
    when point >= 100 then 'GOLD'
    else 'NORMAL'
end as 등급 from member;
-- 8. 랜덤 회원 1명을 조회하세요.
select * from member order by rand() limit 1;
-- 9. 이메일 길이를 출력하세요.
select char_length(email) from member;
-- 10. 가입일 기준 오늘까지 며칠 지났는지 출력하세요.
select datediff(now(), regdate) from member;