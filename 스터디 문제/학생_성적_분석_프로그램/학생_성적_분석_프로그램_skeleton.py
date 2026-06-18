def input_students():
    student_count = int(input("학생 수: "))
    students = []

    for _ in range(student_count):
        student_name = input("학생 이름: ")

        while True:
            student_score = int(input("학생 점수: "))

            # TODO: 점수가 0~100 사이이면 반복문을 종료하세요.

            # TODO: 잘못된 점수이면 안내 문구를 출력하세요.

        student = {
            "name": student_name,
            "score": student_score
        }

        # TODO: student 딕셔너리를 students 리스트에 추가하세요.

    # TODO: students를 반환하세요.


def calculate_average_score(students):
    total_score = 0

    # TODO: 모든 학생의 점수를 total_score에 더하세요.

    # TODO: 평균 점수를 계산해 average_score에 저장하세요.

    # TODO: average_score를 반환하세요.


def find_max_score(students):
    max_score = students[0]["score"]

    # TODO: students를 반복하면서 최고 점수를 찾으세요.

    # TODO: max_score를 반환하세요.


def find_min_score(students):
    min_score = students[0]["score"]

    # TODO: students를 반복하면서 최저 점수를 찾으세요.

    # TODO: min_score를 반환하세요.


def find_passed_students(students):
    # TODO: 리스트 컴프리헨션으로 60점 이상인 학생 이름만 저장하세요.
    passed_students = []

    # TODO: passed_students를 반환하세요.


def print_students(students):
    print()
    print("===== 전체 학생 목록 =====")

    # TODO: enumerate()를 사용해서 번호, 이름, 점수, 합격 여부를 출력하세요.


def print_score_summary(students, average_score, max_score, min_score, passed_students):
    print()
    print("===== 성적 요약 =====")

    # TODO: 평균 점수, 최고 점수, 최저 점수를 출력하세요.

    # TODO: 합격자가 있으면 이름 목록을 출력하고, 없으면 "없음"을 출력하세요.


def print_sorted_students(sorted_students):
    print()
    print("===== 점수 높은 순 =====")

    # TODO: 점수 높은 순으로 정렬된 학생 목록을 번호와 함께 출력하세요.


students = input_students()

average_score = calculate_average_score(students)
max_score = find_max_score(students)
min_score = find_min_score(students)
passed_students = find_passed_students(students)

# TODO: sorted()를 사용해 점수 높은 순으로 정렬한 결과를 sorted_students에 저장하세요.
sorted_students = []

print_students(students)
print_score_summary(students, average_score, max_score, min_score, passed_students)
print_sorted_students(sorted_students)