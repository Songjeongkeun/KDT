menus = {
    "아메리카노": ("음료", 3000),
    "라떼": ("음료", 4000),
    "레몬에이드": ("음료", 4200),
    "쿠키": ("디저트", 2000),
    "케이크": ("디저트", 5000),
    "마카롱": ("디저트", 2500)
}

orders = {}

while True:
    command = input("명령어 입력: ")

    match command:
        case "메뉴":
            # TODO: 메뉴판 제목 출력하기
            # TODO: menus 딕셔너리를 순회하며 메뉴 출력하기
            # 출력 형식: [카테고리] 상품명: 가격원
            # 힌트:
            # for item, info in menus.items():
            #     category, price = info
            pass

        case "주문":
            print("주문 모드를 시작합니다.")

            while True:
                order = input("주문: ")

                # TODO: "종료"를 입력하면 주문 모드를 종료하기
                # 주문 모드를 종료할 때 "주문 모드를 종료합니다." 출력하기

                # TODO: "상품명 수량" 형태의 입력을 상품명과 수량으로 나누기
                item = ""
                quantity = 0

                # TODO: 수량을 정수로 변환하기

                # TODO: 메뉴판에 없는 상품이면 "없는 메뉴입니다." 출력 후 다시 주문받기

                # TODO: 주문 수량 누적하기
                # 힌트: orders[item] = orders.get(item, 0) + quantity
                pass

        case "주문 완료":
            print("=== 최종 주문 내역 ===")

            # TODO: 음료 매출과 디저트 매출을 저장할 변수 만들기
            drink_total = 0
            dessert_total = 0

            # TODO: orders 딕셔너리를 순회하며 최종 주문 내역 출력하기
            # 1. menus에서 category, price 꺼내기
            # 2. item_total = price * quantity 계산하기
            # 3. [카테고리] 상품명: 수량개, 금액원 형식으로 출력하기
            # 4. 카테고리에 따라 drink_total 또는 dessert_total에 누적하기

            # TODO: 전체 매출 계산하기
            total_price = 0

            # TODO: 전체 매출이 30000원 이상이면 10% 할인 계산하기
            discount = 0

            # TODO: 결제 금액 계산하기
            final_price = 0

            # TODO: 음료 매출, 디저트 매출, 전체 매출, 할인 금액, 결제 금액 출력하기

            break

        case _:
            print("존재하지 않는 명령어입니다.")

    print()
