# 함수별 실행 예제

> `main.py` 실행 후 메인 메뉴와 하위 메뉴를 선택하면서 각 기능을 실행하는 예제입니다.

---

## 1. 프로그램 실행

```bash
python3 main.py
```

실행 후 다음과 같은 메인 메뉴가 출력된다.

```text
===== Study Task Manager =====
1. 과목 관리
2. 과제 관리
3. 학습 계획 관리
4. 학습 기록 관리
5. 과제 메모 관리
6. 요약 정보
0. 종료
메뉴를 선택하세요:
```

---

## 2. 과목 관리 함수

### 2.1 과목 등록

사용 함수:

```python
StudyService.add_subject()
StudyDAO.add_subject(subject)
```

실행 예제:

```text
메뉴를 선택하세요: 1

----- 과목 관리 -----
1. 과목 등록
2. 과목 전체 출력
3. 과목 삭제
0. 이전 메뉴

하위 메뉴를 선택하세요: 1

[과목 등록]
과목명: Python
설명: 파이썬 기초 문법 학습
과목이 등록되었습니다.
```

### 2.2 과목 전체 출력

사용 함수:

```python
StudyService.show_subjects()
StudyDAO.get_subjects()
```

실행 예제:

```text
메뉴를 선택하세요: 1
하위 메뉴를 선택하세요: 2

[과목 목록]
1. Python - 파이썬 기초 문법 학습
2. MySQL - 데이터베이스 기초
```

### 2.3 과목 삭제

사용 함수:

```python
StudyService.delete_subject()
StudyDAO.delete_subject(subject_id)
```

실행 예제:

```text
메뉴를 선택하세요: 1
하위 메뉴를 선택하세요: 3

[과목 삭제]

[과목 목록]
2. MySQL - 데이터베이스 기초

삭제할 과목 번호: 2
과목이 삭제되었습니다.
```

---

## 3. 과제 관리 함수

### 3.1 과제 등록

사용 함수:

```python
StudyService.add_task()
StudyDAO.add_task(task)
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 1

[과제 등록]

[과목 목록]
1. Python - 파이썬 기초 문법 학습

과목 번호: 1
과제 제목: 클래스 예제 만들기
과제 내용: property를 사용한 클래스 작성
우선순위(낮음/보통/높음): 높음
마감일(YYYY-MM-DD, 생략 가능): 2026-06-20

과제가 등록되었습니다.
```

### 3.2 과제 전체 출력

사용 함수:

```python
StudyService.show_all_tasks()
StudyDAO.get_tasks()
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 2

[과제 목록]
1. [Python] 클래스 예제 만들기 / 우선순위: 높음 / 상태: 대기 / 마감일: 2026-06-20
```

### 3.3 조건별 과제 조회

사용 함수:

```python
StudyService.filter_tasks()
StudyDAO.filter_tasks(subject_id, priority, status)
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 3

[조건별 과제 조회]
입력하지 않은 조건은 전체로 조회합니다.

과목 번호(생략 가능): 1
우선순위(낮음/보통/높음, 생략 가능): 높음
상태(대기/완료, 생략 가능): 대기

[과제 목록]
1. [Python] 클래스 예제 만들기 / 우선순위: 높음 / 상태: 대기 / 마감일: 2026-06-20
```

### 3.4 과제 검색

사용 함수:

```python
StudyService.search_tasks()
StudyDAO.search_tasks(keyword)
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 4

[과제 검색]
검색어: 클래스

[과제 목록]
1. [Python] 클래스 예제 만들기 / 우선순위: 높음 / 상태: 대기 / 마감일: 2026-06-20
```

### 3.5 과제 수정

사용 함수:

```python
StudyService.update_task()
StudyDAO.update_task(task, task_id)
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 5

[과제 수정]

[과제 목록]
1. [Python] 클래스 예제 만들기 / 우선순위: 높음 / 상태: 대기 / 마감일: 2026-06-20

수정할 과제 번호: 1
수정하지 않을 항목은 Enter만 누르세요.
제목(클래스 예제 만들기): 클래스와 DAO 예제 만들기
내용(property를 사용한 클래스 작성):
우선순위(높음): 보통
마감일(2026-06-20):

과제가 수정되었습니다.
```

### 3.6 과제 완료 처리

사용 함수:

```python
StudyService.complete_task()
StudyDAO.complete_task(task_id)
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 6

[과제 완료 처리]

[과제 목록]
1. [Python] 클래스와 DAO 예제 만들기 / 우선순위: 보통 / 상태: 대기 / 마감일: 2026-06-20

완료할 과제 번호: 1
과제가 완료 처리되었습니다.
```

### 3.7 과제 삭제

사용 함수:

```python
StudyService.delete_task()
StudyDAO.delete_task(task_id)
```

실행 예제:

```text
메뉴를 선택하세요: 2
하위 메뉴를 선택하세요: 7

[과제 삭제]

[과제 목록]
1. [Python] 클래스와 DAO 예제 만들기 / 우선순위: 보통 / 상태: 완료 / 마감일: 2026-06-20

삭제할 과제 번호: 1
과제가 삭제되었습니다.
```

---

## 4. 학습 계획 관리 함수

### 4.1 학습 계획 등록

사용 함수:

```python
StudyService.add_plan()
StudyDAO.add_plan(plan)
```

실행 예제:

```text
메뉴를 선택하세요: 3
하위 메뉴를 선택하세요: 1

[학습 계획 등록]

[과목 목록]
1. Python - 파이썬 기초 문법 학습

과목 번호: 1
계획 제목: 클래스 복습
계획 날짜(YYYY-MM-DD): 2026-06-18
시작 시간(HH:MM, 생략 가능): 19:00
종료 시간(HH:MM, 생략 가능): 20:30
메모: models.py 다시 보기

학습 계획이 등록되었습니다.
```

### 4.2 학습 계획 전체 출력

사용 함수:

```python
StudyService.show_plans()
StudyDAO.get_plans()
```

실행 예제:

```text
메뉴를 선택하세요: 3
하위 메뉴를 선택하세요: 2

[학습 계획 목록]
1. [Python] 클래스 복습 / 날짜: 2026-06-18 / 시간: 19:00:00~20:30:00 / 메모: models.py 다시 보기
```

### 4.3 학습 계획 삭제

사용 함수:

```python
StudyService.delete_plan()
StudyDAO.delete_plan(plan_id)
```

실행 예제:

```text
메뉴를 선택하세요: 3
하위 메뉴를 선택하세요: 3

[학습 계획 삭제]

[학습 계획 목록]
1. [Python] 클래스 복습 / 날짜: 2026-06-18 / 시간: 19:00:00~20:30:00 / 메모: models.py 다시 보기

삭제할 계획 번호: 1
학습 계획이 삭제되었습니다.
```

---

## 5. 학습 기록 관리 함수

### 5.1 학습 기록 등록

사용 함수:

```python
StudyService.add_log()
StudyDAO.add_log(log)
```

실행 예제:

```text
메뉴를 선택하세요: 4
하위 메뉴를 선택하세요: 1

[학습 기록 등록]

[과목 목록]
1. Python - 파이썬 기초 문법 학습

과목 번호: 1
학습 날짜(YYYY-MM-DD): 2026-06-18
학습 시간(분): 90
학습 내용: 클래스, property, DAO 구조 복습

학습 기록이 등록되었습니다.
```

### 5.2 학습 기록 전체 출력

사용 함수:

```python
StudyService.show_logs()
StudyDAO.get_logs()
```

실행 예제:

```text
메뉴를 선택하세요: 4
하위 메뉴를 선택하세요: 2

[학습 기록 목록]
1. [Python] 2026-06-18 / 90분 / 클래스, property, DAO 구조 복습
```

### 5.3 학습 기록 삭제

사용 함수:

```python
StudyService.delete_log()
StudyDAO.delete_log(log_id)
```

실행 예제:

```text
메뉴를 선택하세요: 4
하위 메뉴를 선택하세요: 3

[학습 기록 삭제]

[학습 기록 목록]
1. [Python] 2026-06-18 / 90분 / 클래스, property, DAO 구조 복습

삭제할 기록 번호: 1
학습 기록이 삭제되었습니다.
```

---

## 6. 과제 메모 관리 함수

### 6.1 과제 메모 등록

사용 함수:

```python
StudyService.add_memo()
StudyDAO.add_memo(memo)
```

실행 예제:

```text
메뉴를 선택하세요: 5
하위 메뉴를 선택하세요: 1

[과제 메모 등록]

[과제 목록]
1. [Python] 클래스와 DAO 예제 만들기 / 우선순위: 보통 / 상태: 완료 / 마감일: 2026-06-20

과제 번호: 1
메모: 제출 전에 schema.sql 다시 확인하기

과제 메모가 등록되었습니다.
```

### 6.2 과제 메모 조회

사용 함수:

```python
StudyService.show_memos()
StudyDAO.get_memos(task_id)
```

실행 예제:

```text
메뉴를 선택하세요: 5
하위 메뉴를 선택하세요: 2

과제 번호(생략하면 전체 조회):

[과제 메모 목록]
1. [과제 1: 클래스와 DAO 예제 만들기] 제출 전에 schema.sql 다시 확인하기
```

### 6.3 과제 메모 삭제

사용 함수:

```python
StudyService.delete_memo()
StudyDAO.delete_memo(memo_id)
```

실행 예제:

```text
메뉴를 선택하세요: 5
하위 메뉴를 선택하세요: 3

[과제 메모 삭제]

[과제 메모 목록]
1. [과제 1: 클래스와 DAO 예제 만들기] 제출 전에 schema.sql 다시 확인하기

삭제할 메모 번호: 1
과제 메모가 삭제되었습니다.
```

---

## 7. 요약 정보 함수

### 7.1 요약 정보 출력

사용 함수:

```python
StudyService.show_summary()
StudyDAO.get_summary()
```

실행 예제:

```text
메뉴를 선택하세요: 6

[요약 정보]
과목: 1개
전체 과제: 1개
완료 과제: 1개
대기 과제: 0개
학습 계획: 1개
학습 기록: 1개
총 학습 시간: 90분
과제 메모: 1개
```

---

## 8. 입력 오류 예제

### 8.1 우선순위 오류

```text
우선순위(낮음/보통/높음): 매우높음
우선순위는 낮음, 보통, 높음 중에서 입력하세요.
```

### 8.2 날짜 형식 오류

```text
마감일(YYYY-MM-DD, 생략 가능): 2026/06/20
날짜 형식은 YYYY-MM-DD로 입력하세요.
```

### 8.3 시간 형식 오류

```text
시작 시간(HH:MM, 생략 가능): 7시
시간 형식은 HH:MM으로 입력하세요.
```

### 8.4 숫자 입력 오류

```text
메뉴를 선택하세요: abc
입력 오류: invalid literal for int() with base 10: 'abc'
다시 입력하세요
```
