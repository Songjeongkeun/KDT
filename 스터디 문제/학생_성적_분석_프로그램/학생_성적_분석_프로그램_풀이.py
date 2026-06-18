def input_students():
    student_count = int(input("학생 수: "))
    students = []

    for _ in range(student_count):
        student_name = input("학생 이름: ")

        while True:
            student_score = int(input("학생 점수: "))

            if 0 <= student_score <= 100:
                break

            print("잘못된 점수입니다. 0~100 사이로 다시 입력하세요.")

        student = {
            "name": student_name,
            "score": student_score
        }
        students.append(student)

    return students


def calculate_average_score(students):
    total_score = 0

    for student in students:
        total_score += student["score"]

    average_score = total_score / len(students)
    return average_score


def find_max_score(students):
    max_score = students[0]["score"]

    for student in students:
        if student["score"] > max_score:
            max_score = student["score"]

    return max_score


def find_min_score(students):
    min_score = students[0]["score"]

    for student in students:
        if student["score"] < min_score:
            min_score = student["score"]

    return min_score


def find_passed_students(students):
    passed_students = [student["name"] for student in students if student["score"] >= 60]
    return passed_students


def print_students(students):
    print()
    print("===== 전체 학생 목록 =====")

    for index, student in enumerate(students, start=1):
        result = "합격" if student["score"] >= 60 else "불합격"
        print(f"{index}. {student['name']} - {student['score']}점 - {result}")


def print_score_summary(students, average_score, max_score, min_score, passed_students):
    print()
    print("===== 성적 요약 =====")
    print(f"평균 점수: {average_score:.1f}")
    print(f"최고 점수: {max_score}")
    print(f"최저 점수: {min_score}")

    if passed_students:
        print(f"합격자: {', '.join(passed_students)}")
    else:
        print("합격자: 없음")


def print_sorted_students(sorted_students):
    print()
    print("===== 점수 높은 순 =====")

    for index, student in enumerate(sorted_students, start=1):
        print(f"{index}. {student['name']} - {student['score']}점")


students = input_students()

average_score = calculate_average_score(students)
max_score = find_max_score(students)
min_score = find_min_score(students)
passed_students = find_passed_students(students)
sorted_students = sorted(students, key=lambda student: student["score"], reverse=True)

print_students(students)
print_score_summary(students, average_score, max_score, min_score, passed_students)
print_sorted_students(sorted_students)