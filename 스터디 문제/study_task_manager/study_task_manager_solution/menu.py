from study_service import StudyService


class Menu:
    def __init__(self):
        self.service = StudyService()

    def print_main_menu(self):
        print()
        print("===== Study Task Manager =====")
        print("1. 과목 관리")
        print("2. 과제 관리")
        print("3. 학습 계획 관리")
        print("4. 학습 기록 관리")
        print("5. 과제 메모 관리")
        print("6. 요약 정보")
        print("0. 종료")

    def print_subject_menu(self):
        print()
        print("----- 과목 관리 -----")
        print("1. 과목 등록")
        print("2. 과목 전체 출력")
        print("3. 과목 삭제")
        print("0. 이전 메뉴")

    def print_task_menu(self):
        print()
        print("----- 과제 관리 -----")
        print("1. 과제 등록")
        print("2. 과제 전체 출력")
        print("3. 조건별 과제 조회")
        print("4. 과제 검색")
        print("5. 과제 수정")
        print("6. 과제 완료 처리")
        print("7. 과제 삭제")
        print("0. 이전 메뉴")

    def print_plan_menu(self):
        print()
        print("----- 학습 계획 관리 -----")
        print("1. 학습 계획 등록")
        print("2. 학습 계획 전체 출력")
        print("3. 학습 계획 삭제")
        print("0. 이전 메뉴")

    def print_log_menu(self):
        print()
        print("----- 학습 기록 관리 -----")
        print("1. 학습 기록 등록")
        print("2. 학습 기록 전체 출력")
        print("3. 학습 기록 삭제")
        print("0. 이전 메뉴")

    def print_memo_menu(self):
        print()
        print("----- 과제 메모 관리 -----")
        print("1. 과제 메모 등록")
        print("2. 과제 메모 조회")
        print("3. 과제 메모 삭제")
        print("0. 이전 메뉴")

    def run(self):
        while True:
            try:
                self.print_main_menu()
                menu = int(input("메뉴를 선택하세요: "))

                if menu == 1:
                    self.print_subject_menu()
                    sub_menu = int(input("하위 메뉴를 선택하세요: "))

                    if sub_menu == 1:
                        self.service.add_subject()
                    elif sub_menu == 2:
                        self.service.show_subjects()
                    elif sub_menu == 3:
                        self.service.delete_subject()
                    elif sub_menu == 0:
                        continue
                    else:
                        print("하위 메뉴는 0부터 3까지 입력하세요")

                elif menu == 2:
                    self.print_task_menu()
                    sub_menu = int(input("하위 메뉴를 선택하세요: "))

                    if sub_menu == 1:
                        self.service.add_task()
                    elif sub_menu == 2:
                        self.service.show_all_tasks()
                    elif sub_menu == 3:
                        self.service.filter_tasks()
                    elif sub_menu == 4:
                        self.service.search_tasks()
                    elif sub_menu == 5:
                        self.service.update_task()
                    elif sub_menu == 6:
                        self.service.complete_task()
                    elif sub_menu == 7:
                        self.service.delete_task()
                    elif sub_menu == 0:
                        continue
                    else:
                        print("하위 메뉴는 0부터 7까지 입력하세요")

                elif menu == 3:
                    self.print_plan_menu()
                    sub_menu = int(input("하위 메뉴를 선택하세요: "))

                    if sub_menu == 1:
                        self.service.add_plan()
                    elif sub_menu == 2:
                        self.service.show_plans()
                    elif sub_menu == 3:
                        self.service.delete_plan()
                    elif sub_menu == 0:
                        continue
                    else:
                        print("하위 메뉴는 0부터 3까지 입력하세요")

                elif menu == 4:
                    self.print_log_menu()
                    sub_menu = int(input("하위 메뉴를 선택하세요: "))

                    if sub_menu == 1:
                        self.service.add_log()
                    elif sub_menu == 2:
                        self.service.show_logs()
                    elif sub_menu == 3:
                        self.service.delete_log()
                    elif sub_menu == 0:
                        continue
                    else:
                        print("하위 메뉴는 0부터 3까지 입력하세요")

                elif menu == 5:
                    self.print_memo_menu()
                    sub_menu = int(input("하위 메뉴를 선택하세요: "))

                    if sub_menu == 1:
                        self.service.add_memo()
                    elif sub_menu == 2:
                        self.service.show_memos()
                    elif sub_menu == 3:
                        self.service.delete_memo()
                    elif sub_menu == 0:
                        continue
                    else:
                        print("하위 메뉴는 0부터 3까지 입력하세요")

                elif menu == 6:
                    self.service.show_summary()

                elif menu == 0:
                    print("프로그램을 종료합니다")
                    break

                else:
                    print("메뉴는 0부터 6까지 입력하세요")

            except ValueError as error:
                print("입력 오류:", error)
                print("다시 입력하세요")
            except Exception as error:
                print("오류:", error)
                print("데이터베이스 설정과 입력값을 확인하세요")
