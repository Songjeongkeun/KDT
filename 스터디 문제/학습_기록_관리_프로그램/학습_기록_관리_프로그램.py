def input_study_logs():
    user_name = input("이름: ")
    subject_count = int(input("과목 수: "))
    study_logs = {}

    for _ in range(subject_count):
        subject_name = input("과목명: ")
        study_time = float(input("공부 시간: "))
        study_logs[subject_name] = study_time

    return user_name, study_logs


def calculate_total_time(study_logs):
    total_time = 0

    for study_time in study_logs.values():
        total_time += study_time

    return total_time


def find_max_subject(study_logs):
    max_subject = ""
    max_time = 0

    for subject_name, study_time in study_logs.items():
        if study_time > max_time:
            max_subject = subject_name
            max_time = study_time

    return max_subject


def find_review_subjects(study_logs):
    review_subjects = []

    for subject_name, study_time in study_logs.items():
        if study_time < 1:
            review_subjects.append(subject_name)

    return review_subjects


def print_study_summary(user_name, study_logs, total_time, average_time, max_subject, review_subjects):
    print()
    print(f"===== {user_name}님의 오늘 학습 기록 =====")

    for subject_name, study_time in study_logs.items():
        print(f"{subject_name}: {study_time}시간")

    print()
    print(f"총 공부 시간: {total_time}시간")
    print(f"평균 공부 시간: {average_time:.2f}시간")
    print(f"가장 오래 공부한 과목: {max_subject}")

    if review_subjects:
        print(f"복습 필요 과목: {', '.join(review_subjects)}")
    else:
        print("복습 필요 과목: 없음")


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