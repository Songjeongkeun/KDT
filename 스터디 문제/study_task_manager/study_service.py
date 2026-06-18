from datetime import datetime

from models import Subject, Task, StudyPlan, StudyLog, TaskMemo
from study_dao import StudyDAO


class StudyService:
    def __init__(self):
        self.dao = StudyDAO()

    def print_subject(self, subjects):
        if not subjects:
            print("등록된 과목이 없습니다.")
            return
        print("==== 과목 목록 ====")
        for subject in subjects:
            description = subject["description"] or "---"
            print(
                f"{subject['subject_id']},"
                f"{subject['subject_name']} - {description}"
            )

    def add_subject(self):
        subject_name = input("과목명을 입력하세요: ")
        description = input("간단한 설명을 입력하세요: ")
        subject = Subject(subject_name=subject_name, description=description)
        result = self.dao.add_subject(subject)
        if result > 0:
            print("과목이 등록되었습니다.")
        else:
            print("과목 등록에 실패했습니다.")

    def show_subject(self):
        subjects = self.dao.get_subjects()
        self.print_subject(subjects)

    def delete_subject(self):
        subject_id = int(input("삭제하실 과목 번호를 입력하세요: "))
        subject = self.dao.get_subject_by_id(subject_id)

        if not subject:
            print("삭제할 과목이 없습니다.")
            return

        counts = self.dao.count_subject_links(subject_id)
        if counts["task_count"] > 0 or counts["plan_count"] > 0 or counts["log_count"] > 0:
            print("연결된 과제, 학습 계획, 학습 기록이 있는 과목은 삭제할 수 없습니다.")
            return

        result = self.dao.delete_subject(subject_id)

        if result > 0:
            print("과목이 삭제되었습니다.")
        else:
            print('과목 삭제에 실패했습니다.')

    def add_task(self):
        subjects = self.dao.get_subjects()

        if not subjects:
            print("과제를 등록하려면 먼저 과목을 등록해야 합니다.")
            return

        for subject in subjects:
            self.print_subject(subject)

        subject_id = int(input("과목 번호를 입력하세요: "))
        subject = self.dao.get_subject_by_id(subject_id)

        if not subject:
            print("존재하지 않는 과목입니다.")
            return

        title = input("과제 제목을 입력하세요: ")
        content = input("과제 내용을 입력하세요(생략 가능): ")
        priority = input("우선순위를 입력하세요(낮음/보통/높음): ").strip()
        due_date = input("마감일을 입력하세요(YYYY-MM-DD, 생략 가능): ").strip()

        if priority not in ["낮음", "보통", "높음"]:
            print("우선순위는 낮음, 보통, 높음 중에서 입력하세요")
            return

        if due_date:
            datetime.strptime(due_date, "%Y-%m-%d")
        else:
            due_date = None

        task = Task(subject_id, title, content, priority, due_date)
        result = self.dao.add_task(task)
        if result > 0: 
            print("과제가 등록되었습니다.")
        else:
            print("과제 등록에 실패했습니다.")
            
    def show_all_tasks(self):
        tasks = self.dao.get_tasks()

        if not tasks:
            print("조회된 과제가 없습니다")
            return

        for task in tasks:
            self.print_task(task)
            
    def filter_tasks(self):
        subject_text = input("과목 번호를 입력하세요. (생략 가능): )").strip()
        priority = input("우선순위를 입력하세요.(낮음 / 보통 / 높음, 생략가능) ").strip()
        status = input("상태를 입력하세요. (대기 / 완료, 생략 가능)").strip()
        
        subject_id = int(subject_text) if subject_text else None
        
        if priority and priority not in ["낮음", "보통", "높음"]:
            print("잘못된 우선순위입니다.")
            return
        
        if status and status not in ["대기", "완료"]:
            print("잘못된 상태입니다.")
            return
        
        priority = priority or None
        status = status or None
        tasks = self.dao.filter_tasks(subject_id, priority, status)