from contacts_service import ContactsService


class Menu:
    def __init__(self):
        self.service = ContactsService()

    def run(self):
        while True:
            try:
                print()
                print("===== 전화번호부 =====")
                print("1. 전화번호 등록하기")
                print("2. 전화번호 전체 출력하기")
                print("3. 전화번호 검색하기")
                print("4. 전화번호 수정하기")
                print("5. 전화번호 삭제하기")
                print("6. 종료하기")

                menu = int(input("메뉴를 선택하세요: "))

                if menu == 1:
                    self.service.insert_contact()
                elif menu == 2:
                    self.service.print_all()
                elif menu == 3:
                    self.service.search_contacts()
                elif menu == 4:
                    self.service.edit_contact()
                elif menu == 5:
                    self.service.delete_contact()
                elif menu == 6:
                    print("프로그램을 종료합니다")
                    break
                else:
                    print("메뉴는 1부터 6까지 입력하세요")
            except ValueError as error:
                print("입력 오류:", error)
                print("다시 입력하세요")
            except Exception as error:
                print("오류:", error)
                print("데이터베이스 설정과 입력값을 확인하세요")
