# Study Task Manager 정답 예시

## 파일 구조

```text
study_task_manager_solution/
├── main.py
├── menu.py
├── study_service.py
├── study_dao.py
├── models.py
├── db.py
├── schema.sql
└── README.md
```

## 실행 준비

1. MySQL에서 `schema.sql`을 실행한다.
2. `db.py`의 MySQL 계정 정보를 본인 환경에 맞게 수정한다.
3. 필요한 패키지를 설치한다.

```bash
pip install mysql-connector-python
```

## 실행

```bash
python main.py
```

## 주요 기능

- 과목 등록, 목록 조회, 삭제
- 과제 등록, 전체 조회, 조건별 조회, 검색
- 과제 수정, 완료 처리, 삭제
- 전체 과제, 완료 과제, 대기 과제 요약

