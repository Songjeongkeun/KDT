from datetime import datetime

from models import Subject, StudyLog, StudyPlan, Task, TaskMemo
from study_dao import StudyDAO


class StudyService:
    def __init__(self):
        self.dao = StudyDAO()

    @staticmethod
    def print_subject(subject):
        description = subject["description"] or "-"
        print(
            f"{subject['subject_id']}. "
            f"{subject['subject_name']} - {description}"
        )

    @staticmethod
    def print_task(task):
        due_date = task["due_date"] or "-"
        print(
            f"{task['task_id']}. "
            f"[{task['subject_name']}] "
            f"{task['title']} / "
            f"우선순위: {task['priority']} / "
            f"상태: {task['status']} / "
            f"마감일: {due_date}"
        )

    @staticmethod
    def print_plan(plan):
        start_time = plan["start_time"] or "-"
        end_time = plan["end_time"] or "-"
        memo = plan["memo"] or "-"
        print(
            f"{plan['plan_id']}. "
            f"[{plan['subject_name']}] "
            f"{plan['plan_title']} / "
            f"날짜: {plan['plan_date']} / "
            f"시간: {start_time}~{end_time} / "
            f"메모: {memo}"
        )

    @staticmethod
    def print_log(log):
        print(
            f"{log['log_id']}. "
            f"[{log['subject_name']}] "
            f"{log['study_date']} / "
            f"{log['study_time']}분 / "
            f"{log['content']}"
        )

    @staticmethod
    def print_memo(memo):
        print(
            f"{memo['memo_id']}. "
            f"[과제 {memo['task_id']}: {memo['title']}] "
            f"{memo['memo']}"
        )

    def add_subject(self):
        subject_name = input("과목명을 입력하세요: ")
        description = input("설명을 입력하세요(생략 가능): ")

        subject = Subject(subject_name, description)
        result = self.dao.add_subject(subject)

        if result > 0:
            print("과목이 등록되었습니다")
        else:
            print("과목 등록에 실패했습니다")

    def show_subjects(self):
        subjects = self.dao.get_subjects()

        if not subjects:
            print("등록된 과목이 없습니다")
            return

        for subject in subjects:
            self.print_subject(subject)

    def delete_subject(self):
        subject_id = int(input("삭제할 과목 번호를 입력하세요: "))
        subject = self.dao.get_subject_by_id(subject_id)

        if not subject:
            print("삭제할 과목이 없습니다")
            return

        counts = self.dao.count_subject_links(subject_id)
        if counts["task_count"] > 0 or counts["plan_count"] > 0 or counts["log_count"] > 0:
            print("연결된 과제, 학습 계획, 학습 기록이 있는 과목은 삭제할 수 없습니다")
            return

        result = self.dao.delete_subject(subject_id)

        if result > 0:
            print("과목이 삭제되었습니다")
        else:
            print("과목 삭제에 실패했습니다")

    def add_task(self):
        subjects = self.dao.get_subjects()

        if not subjects:
            print("과제를 등록하려면 먼저 과목을 등록해야 합니다")
            return

        for subject in subjects:
            self.print_subject(subject)

        subject_id = int(input("과목 번호를 입력하세요: "))
        subject = self.dao.get_subject_by_id(subject_id)

        if not subject:
            print("존재하지 않는 과목입니다")
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
            print("과제가 등록되었습니다")
        else:
            print("과제 등록에 실패했습니다")

    def show_all_tasks(self):
        tasks = self.dao.get_tasks()

        if not tasks:
            print("조회된 과제가 없습니다")
            return

        for task in tasks:
            self.print_task(task)

    def filter_tasks(self):
        subject_text = input("과목 번호를 입력하세요(생략 가능): ").strip()
        priority = input("우선순위를 입력하세요(낮음/보통/높음, 생략 가능): ").strip()
        status = input("상태를 입력하세요(대기/완료, 생략 가능): ").strip()

        subject_id = int(subject_text) if subject_text else None

        if priority and priority not in ["낮음", "보통", "높음"]:
            print("잘못된 우선순위입니다")
            return

        if status and status not in ["대기", "완료"]:
            print("잘못된 상태입니다")
            return

        priority = priority or None
        status = status or None
        tasks = self.dao.filter_tasks(subject_id, priority, status)

        if not tasks:
            print("조회된 과제가 없습니다")
            return

        for task in tasks:
            self.print_task(task)

    def search_tasks(self):
        keyword = input("검색할 과제 제목 또는 내용을 입력하세요: ").strip()
        tasks = self.dao.search_tasks(keyword)

        if not tasks:
            print("찾는 과제가 없습니다")
            return

        for task in tasks:
            self.print_task(task)

    def update_task(self):
        task_id = int(input("수정할 과제 번호를 입력하세요: "))
        saved_task = self.dao.get_task_by_id(task_id)

        if not saved_task:
            print("수정할 과제가 없습니다")
            return

        print("새 값을 입력하세요. 입력하지 않으면 기존 값을 유지합니다.")
        title = input(f"제목({saved_task['title']}): ").strip()
        content = input(f"내용({saved_task['content'] or '-'}): ").strip()
        priority = input(f"우선순위({saved_task['priority']}): ").strip()
        due_date = input(f"마감일({saved_task['due_date'] or '-'}): ").strip()

        if priority and priority not in ["낮음", "보통", "높음"]:
            print("잘못된 우선순위입니다")
            return

        if due_date:
            datetime.strptime(due_date, "%Y-%m-%d")

        task = Task(
            saved_task["subject_id"],
            title or saved_task["title"],
            content or saved_task["content"] or "",
            priority or saved_task["priority"],
            due_date or saved_task["due_date"],
        )
        result = self.dao.update_task(task, task_id)

        if result > 0:
            print("과제가 수정되었습니다")
        else:
            print("과제 수정에 실패했습니다")

    def complete_task(self):
        task_id = int(input("완료할 과제 번호를 입력하세요: "))
        task = self.dao.get_task_by_id(task_id)

        if not task:
            print("완료 처리할 과제가 없습니다")
            return

        if task["status"] == "완료":
            print("이미 완료된 과제입니다")
            return

        result = self.dao.complete_task(task_id)

        if result > 0:
            print("과제가 완료 처리되었습니다")
        else:
            print("완료 처리에 실패했습니다")

    def delete_task(self):
        task_id = int(input("삭제할 과제 번호를 입력하세요: "))
        task = self.dao.get_task_by_id(task_id)

        if not task:
            print("삭제할 과제가 없습니다")
            return

        result = self.dao.delete_task(task_id)

        if result > 0:
            print("과제가 삭제되었습니다")
        else:
            print("과제 삭제에 실패했습니다")

    def add_plan(self):
        subjects = self.dao.get_subjects()

        if not subjects:
            print("학습 계획을 등록하려면 먼저 과목을 등록해야 합니다")
            return

        for subject in subjects:
            self.print_subject(subject)

        subject_id = int(input("과목 번호를 입력하세요: "))
        subject = self.dao.get_subject_by_id(subject_id)

        if not subject:
            print("존재하지 않는 과목입니다")
            return

        plan_title = input("계획 제목을 입력하세요: ")
        plan_date = input("계획 날짜를 입력하세요(YYYY-MM-DD): ").strip()
        start_time = input("시작 시간을 입력하세요(HH:MM, 생략 가능): ").strip()
        end_time = input("종료 시간을 입력하세요(HH:MM, 생략 가능): ").strip()
        memo = input("메모를 입력하세요(생략 가능): ")

        datetime.strptime(plan_date, "%Y-%m-%d")

        if start_time:
            datetime.strptime(start_time, "%H:%M")
        else:
            start_time = None

        if end_time:
            datetime.strptime(end_time, "%H:%M")
        else:
            end_time = None

        plan = StudyPlan(subject_id, plan_title, plan_date, start_time, end_time, memo)
        result = self.dao.add_plan(plan)

        if result > 0:
            print("학습 계획이 등록되었습니다")
        else:
            print("학습 계획 등록에 실패했습니다")

    def show_plans(self):
        plans = self.dao.get_plans()

        if not plans:
            print("등록된 학습 계획이 없습니다")
            return

        for plan in plans:
            self.print_plan(plan)

    def delete_plan(self):
        plan_id = int(input("삭제할 계획 번호를 입력하세요: "))
        plan = self.dao.get_plan_by_id(plan_id)

        if not plan:
            print("삭제할 학습 계획이 없습니다")
            return

        result = self.dao.delete_plan(plan_id)

        if result > 0:
            print("학습 계획이 삭제되었습니다")
        else:
            print("학습 계획 삭제에 실패했습니다")

    def add_log(self):
        subjects = self.dao.get_subjects()

        if not subjects:
            print("학습 기록을 등록하려면 먼저 과목을 등록해야 합니다")
            return

        for subject in subjects:
            self.print_subject(subject)

        subject_id = int(input("과목 번호를 입력하세요: "))
        subject = self.dao.get_subject_by_id(subject_id)

        if not subject:
            print("존재하지 않는 과목입니다")
            return

        study_date = input("학습 날짜를 입력하세요(YYYY-MM-DD): ").strip()
        study_time = int(input("학습 시간을 입력하세요(분): ").strip())
        content = input("학습 내용을 입력하세요: ")

        datetime.strptime(study_date, "%Y-%m-%d")

        if study_time < 0:
            print("학습 시간은 0 이상이어야 합니다")
            return

        log = StudyLog(subject_id, study_date, study_time, content)
        result = self.dao.add_log(log)

        if result > 0:
            print("학습 기록이 등록되었습니다")
        else:
            print("학습 기록 등록에 실패했습니다")

    def show_logs(self):
        logs = self.dao.get_logs()

        if not logs:
            print("등록된 학습 기록이 없습니다")
            return

        for log in logs:
            self.print_log(log)

    def delete_log(self):
        log_id = int(input("삭제할 기록 번호를 입력하세요: "))
        log = self.dao.get_log_by_id(log_id)

        if not log:
            print("삭제할 학습 기록이 없습니다")
            return

        result = self.dao.delete_log(log_id)

        if result > 0:
            print("학습 기록이 삭제되었습니다")
        else:
            print("학습 기록 삭제에 실패했습니다")

    def add_memo(self):
        tasks = self.dao.get_tasks()

        if not tasks:
            print("과제 메모를 등록하려면 먼저 과제를 등록해야 합니다")
            return

        for task in tasks:
            self.print_task(task)

        task_id = int(input("과제 번호를 입력하세요: "))
        task = self.dao.get_task_by_id(task_id)

        if not task:
            print("존재하지 않는 과제입니다")
            return

        memo_text = input("메모를 입력하세요: ")
        memo = TaskMemo(task_id, memo_text)
        result = self.dao.add_memo(memo)

        if result > 0:
            print("과제 메모가 등록되었습니다")
        else:
            print("과제 메모 등록에 실패했습니다")

    def show_memos(self):
        task_text = input("과제 번호를 입력하세요(생략하면 전체 조회): ").strip()
        task_id = int(task_text) if task_text else None
        memos = self.dao.get_memos(task_id)

        if not memos:
            print("등록된 과제 메모가 없습니다")
            return

        for memo in memos:
            self.print_memo(memo)

    def delete_memo(self):
        memo_id = int(input("삭제할 메모 번호를 입력하세요: "))
        memo = self.dao.get_memo_by_id(memo_id)

        if not memo:
            print("삭제할 과제 메모가 없습니다")
            return

        result = self.dao.delete_memo(memo_id)

        if result > 0:
            print("과제 메모가 삭제되었습니다")
        else:
            print("과제 메모 삭제에 실패했습니다")

    def show_summary(self):
        summary = self.dao.get_summary()

        print(f"과목: {summary['subject_count']}개")
        print(f"전체 과제: {summary['task_count']}개")
        print(f"완료 과제: {summary['done_count']}개")
        print(f"대기 과제: {summary['waiting_count']}개")
        print(f"학습 계획: {summary['plan_count']}개")
        print(f"학습 기록: {summary['log_count']}개")
        print(f"총 학습 시간: {summary['total_time']}분")
        print(f"과제 메모: {summary['memo_count']}개")
