menu = {
    "아메리카노": 3000,
    "카페라떼": 4000,
    "바닐라라떼": 4500,
    "레몬에이드": 4200,
    "치즈케이크": 5500,
    "쿠키": 2000
}

orders = {}

while True:
    command = input("명령어 입력: ")

    match command:
        case "메뉴":
            # TODO: 메뉴판 제목 출력하기

            # TODO: menu 딕셔너리를 순회하며 상품명과 가격 출력하기
            # 힌트: for item, price in menu.items():
            pass

        case "주문":
            print("주문 모드를 시작합니다.")

            while True:
                order = input("주문: ")

                # TODO: order가 "종료"이면 주문 모드를 종료하기
                # 힌트: break 사용

                # TODO: "상품명 수량" 형식으로 입력받은 값을 나누기
                # 힌트: split() 사용
                item = ""
                quantity = 0

                # TODO: 수량을 정수로 변환하기

                # TODO: 메뉴판에 없는 상품이면 메시지를 출력하고 다시 주문받기
                # 힌트: continue 사용

                # TODO: 같은 상품을 다시 주문하면 기존 수량에 누적하기
                # 힌트: orders[item] = orders.get(item, 0) + quantity
                pass

            print("주문 모드를 종료합니다.")

        case "주문 완료":
            print("=== 최종 주문 내역 ===")

            # TODO: 상품 금액 합계를 저장할 변수 만들기
            total_price = 0

            # TODO: orders 딕셔너리를 순회하며 상품별 수량과 금액 출력하기
            # 힌트:
            # for item, quantity in orders.items():
            #     item_price = menu[item] * quantity
            #     total_price += item_price

            # TODO: 상품 금액이 30000원 이상이면 10% 할인 금액 계산하기
            discount = 0

            # TODO: 결제 금액 계산하기
            final_price = 0

            # TODO: 상품 금액, 할인 금액, 결제 금액 출력하기

            break

        case _:
            print("존재하지 않는 명령어입니다.")

    print()
