# models.py 
# 데이터를 담는 클래스 파일

class Subject:
    def __init__(self, subject_name, description="", subject_id = None, created_at = None):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.description = description
        self.created_at = created_at
        
    def __repr__(self):
        return(
            f"Subject(subject_id='{self.subject_id}', "
            f"subject_name='{self.subject_name}', "
            f"description='{self.description}')"
        )
    
    @property
    def subject_id(self):
        return self.__subject_id
    
    @subject_id.setter
    def subject_id(self, subject_id):
        self.__subject_id = subject_id
        
    @property
    def subject_name(self):
        return self.__subject_name

    @subject_name.setter
    def subject_name(self, subject_name):
        subject_name = subject_name.strip()

        if not subject_name:
            raise ValueError("과목명은 비워둘 수 없습니다")

        self.__subject_name = subject_name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description.strip()

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at


class Task:
    priorities = ["낮음", "보통", "높음"]
    statuses = ["대기", "완료"]

    def __init__(
        self,
        subject_id,
        title,
        content="",
        priority="보통",
        due_date=None,
        status="대기",
        task_id=None,
        created_at=None,
    ):
        self.task_id = task_id
        self.subject_id = subject_id
        self.title = title
        self.content = content
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.created_at = created_at

    def __repr__(self):
        return (
            f"Task(task_id={self.task_id}, subject_id={self.subject_id}, "
            f"title='{self.title}', priority='{self.priority}', "
            f"status='{self.status}', due_date={self.due_date})"
        )

    @property
    def task_id(self):
        return self.__task_id

    @task_id.setter
    def task_id(self, task_id):
        self.__task_id = task_id

    @property
    def subject_id(self):
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, subject_id):
        if subject_id is None:
            raise ValueError("과목 번호는 비워둘 수 없습니다")

        self.__subject_id = subject_id

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        title = title.strip()

        if not title:
            raise ValueError("과제 제목은 비워둘 수 없습니다")

        self.__title = title

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        self.__content = content.strip()

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, priority):
        priority = priority.strip()

        if priority not in self.priorities:
            raise ValueError("우선순위는 낮음, 보통, 높음 중에서 입력하세요")

        self.__priority = priority

    @property
    def due_date(self):
        return self.__due_date

    @due_date.setter
    def due_date(self, due_date):
        self.__due_date = due_date

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        status = status.strip()

        if status not in self.statuses:
            raise ValueError("상태는 대기 또는 완료만 입력할 수 있습니다")

        self.__status = status

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at
        
class StudyPlan:
    def __init__(
        self,
        subject_id,
        plan_title,
        plan_date,
        start_time = None,
        end_time = None,
        memo="",
        plan_id=None,
        created_at=None
    ):
        self.plan_id = plan_id
        self.subject_id = subject_id
        self.plan_title = plan_title
        self.plan_date = plan_date
        self.start_time = start_time
        self.end_time = end_time
        self.memo = memo
        self.created_at = created_at
        
    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        self.__plan_id = plan_id

    @property
    def subject_id(self):
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, subject_id):
        if subject_id is None:
            raise ValueError("과목 번호는 비워둘 수 없습니다")
        self.__subject_id = subject_id

    @property
    def plan_title(self):
        return self.__plan_title

    @plan_title.setter
    def plan_title(self, plan_title):
        plan_title = plan_title.strip()
        if not plan_title:
            raise ValueError("계획 제목은 비워둘 수 없습니다")
        if len(plan_title) > 100:
            raise ValueError("계획 제목은 100자 이하로 입력하세요")
        self.__plan_title = plan_title

    @property
    def plan_date(self):
        return self.__plan_date

    @plan_date.setter
    def plan_date(self, plan_date):
        if not plan_date:
            raise ValueError("계획 날짜는 비워둘 수 없습니다")
        self.__plan_date = plan_date

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time

    @property
    def memo(self):
        return self.__memo

    @memo.setter
    def memo(self, memo):
        memo = (memo or "").strip()
        if len(memo) > 200:
            raise ValueError("계획 메모는 200자 이하로 입력하세요")
        self.__memo = memo

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at


class StudyLog:
    def __init__(
        self,
        subject_id,
        study_date,
        study_time,
        content,
        log_id=None,
        created_at=None,
    ):
        self.log_id = log_id
        self.subject_id = subject_id
        self.study_date = study_date
        self.study_time = study_time
        self.content = content
        self.created_at = created_at

    @property
    def log_id(self):
        return self.__log_id

    @log_id.setter
    def log_id(self, log_id):
        self.__log_id = log_id

    @property
    def subject_id(self):
        return self.__subject_id

    @subject_id.setter
    def subject_id(self, subject_id):
        if subject_id is None:
            raise ValueError("과목 번호는 비워둘 수 없습니다")
        self.__subject_id = subject_id

    @property
    def study_date(self):
        return self.__study_date

    @study_date.setter
    def study_date(self, study_date):
        if not study_date:
            raise ValueError("학습 날짜는 비워둘 수 없습니다")
        self.__study_date = study_date

    @property
    def study_time(self):
        return self.__study_time

    @study_time.setter
    def study_time(self, study_time):
        if study_time < 0:
            raise ValueError("학습 시간은 0 이상이어야 합니다")
        self.__study_time = study_time

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, content):
        content = content.strip()
        if not content:
            raise ValueError("학습 내용은 비워둘 수 없습니다")
        if len(content) > 300:
            raise ValueError("학습 내용은 300자 이하로 입력하세요")
        self.__content = content

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at


class TaskMemo:
    def __init__(self, task_id, memo, memo_id=None, created_at=None):
        self.memo_id = memo_id
        self.task_id = task_id
        self.memo = memo
        self.created_at = created_at

    @property
    def memo_id(self):
        return self.__memo_id

    @memo_id.setter
    def memo_id(self, memo_id):
        self.__memo_id = memo_id

    @property
    def task_id(self):
        return self.__task_id

    @task_id.setter
    def task_id(self, task_id):
        if task_id is None:
            raise ValueError("과제 번호는 비워둘 수 없습니다")
        self.__task_id = task_id

    @property
    def memo(self):
        return self.__memo

    @memo.setter
    def memo(self, memo):
        memo = memo.strip()
        if not memo:
            raise ValueError("메모는 비워둘 수 없습니다")
        if len(memo) > 300:
            raise ValueError("메모는 300자 이하로 입력하세요")
        self.__memo = memo

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, created_at):
        self.__created_at = created_at
