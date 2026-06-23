# Menu.py
from Online_Store.online_store_service import OnlineStoreService

class Menu:
    def __init__(self):
        # self.service =
        pass

    def print_login_menu(self):
        print()
        print("=") * 20
        print(" 온라인 스토어")
        print("=") * 20
        print("1. 회원가입")
        print("2. 로그인")
        print("0. 프로그램 종료")
        print("=") * 20

    def print_main_menu(self):
        print()
        print("=") * 20
        print(" 메인 메뉴 ")
        print("=") * 20
        print("1. 상품 목록 조회")
        print("2. 상품 검색")
        print("3. 주문하기")
        print("4. 주문 내역 조회")
        print("5. 로그 아웃")
        print("0. 프로그램 종료")
        print("=") * 20
        print("메뉴 번호를 선택하세요: ")

    def run(self):
        while True:
            try:
                self.print_login_menu()
                login = int(input("메뉴 번호를 선택하세요: "))

                if login == 1:
                    # 회원 가입
                    self.service.register_membership()
                    pass
                elif login == 2:
                    self.service.login()
                    self.print_main_menu()
                    menu = int(input("메뉴 번호를 선택하세요 : "))
                    if menu == 1:
                        # 상품 목록 조회
                        pass
                    elif menu == 2:
                        # 상품 검색
                        pass
                    elif menu == 3:
                        # 주문하기
                        pass
                    elif menu == 4:
                        # 주문 내역 조회
                        pass
                    elif menu == 5:
                        # 로그아웃 
                        pass
                    elif menu == 0:
                        print("프로그램을 종료합니다.")
                        break
                    else:
                        print("메뉴 번호는 0부터 5까지 입력하세요.")


                elif login == 0:
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("메뉴 번호는 0부터 2까지 입력하세요. ")
                    continue

            except ValueError as error:
                print("입력 오류:", error)
                print("다시 입력하세요")
            except Exception as error:
                print("오류:", error)
                print("데이터베이스 설정과 입력값을 확인하세요")
