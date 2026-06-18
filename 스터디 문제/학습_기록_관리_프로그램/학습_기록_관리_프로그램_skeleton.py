def input_study_logs():
    user_name = input("이름: ")
    subject_count = int(input("과목 수: "))
    study_logs = {}

    for _ in range(subject_count):
        subject_name = input("과목명: ")
        study_time = float(input("공부 시간: "))

        # TODO: 과목명을 key, 공부 시간을 value로 study_logs에 저장하세요.

    # TODO: user_name과 study_logs를 반환하세요.


def calculate_total_time(study_logs):
    total_time = 0

    # TODO: study_logs의 공부 시간을 모두 더하세요.

    # TODO: total_time을 반환하세요.


def find_max_subject(study_logs):
    max_subject = ""
    max_time = 0

    # TODO: 가장 오래 공부한 과목명과 시간을 찾으세요.

    # TODO: max_subject를 반환하세요.


def find_review_subjects(study_logs):
    review_subjects = []

    # TODO: 공부 시간이 1시간 미만인 과목을 review_subjects에 추가하세요.

    # TODO: review_subjects를 반환하세요.


def print_study_summary(user_name, study_logs, total_time, average_time, max_subject, review_subjects):
    print()
    print(f"===== {user_name}님의 오늘 학습 기록 =====")

    # TODO: study_logs에 저장된 전체 학습 기록을 출력하세요.

    print()
    print(f"총 공부 시간: {total_time}시간")
    print(f"평균 공부 시간: {average_time:.2f}시간")
    print(f"가장 오래 공부한 과목: {max_subject}")

    # TODO: 복습 필요 과목이 있으면 출력하고, 없으면 "없음"을 출력하세요.


user_name, study_logs = input_study_logs()

total_time = calculate_total_time(study_logs)
average_time = total_time / len(study_logs)
max_subject = find_max_subject(study_logs)
review_subjects = find_review_subjects(study_logs)

print_study_summary(
    user_name,
    study_logs,
    total_time,
    average_time,
    max_subject,
    review_subjects
)