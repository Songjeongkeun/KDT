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
            print("=== 메뉴판 ===")

            for item, info in menus.items():
                category, price = info
                print(f"[{category}] {item}: {price}원")

        case "주문":
            print("주문 모드를 시작합니다.")

            while True:
                order = input("주문: ")

                if order == "종료":
                    print("주문 모드를 종료합니다.")
                    break

                item, quantity = order.split()
                quantity = int(quantity)

                if item not in menus:
                    print("없는 메뉴입니다.")
                    continue

                orders[item] = orders.get(item, 0) + quantity

        case "주문 완료":
            print("=== 최종 주문 내역 ===")

            drink_total = 0
            dessert_total = 0

            for item, quantity in orders.items():
                category, price = menus[item]
                item_total = price * quantity

                print(f"[{category}] {item}: {quantity}개, {item_total}원")

                if category == "음료":
                    drink_total += item_total
                elif category == "디저트":
                    dessert_total += item_total

            total_price = drink_total + dessert_total

            if total_price >= 30000:
                discount = total_price // 10
            else:
                discount = 0

            final_price = total_price - discount

            print()
            print(f"음료 매출: {drink_total}원")
            print(f"디저트 매출: {dessert_total}원")
            print(f"전체 매출: {total_price}원")
            print(f"할인 금액: {discount}원")
            print(f"결제 금액: {final_price}원")
            break

        case _:
            print("존재하지 않는 명령어입니다.")

    print()
