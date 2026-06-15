use ai;

select * from member;

-- insert into member (userid, userpw, name, hp, email, ssn1, ssn2, zipcode, address1, address2, address3, gender) values ('apple', '1111', '테스--', '010-1111-1111', 'apple@apple.com', '001011', '4011111', '12345', '서울 서초구', '양재동', '111-11', '여자');
-- Error Code: 1142. INSERT command denied to user 'banana'@'localhost' for table 'member'
-- insert 권한 없음

