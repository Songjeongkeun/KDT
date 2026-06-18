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
            print("=== 메뉴판 ===")
            for item, price in menu.items():
                print(f"{item}: {price}원")
            print()
            pass
        
        case "주문":
            print("주문 모드를 시작합니다.")
            while True:
                command_order = input("주문: ")
                if command_order == "종료":
                    break
                else:
                    item, quantity = command_order.split()
                    quantity = int(quantity)
 
                if item not in menu:
                    print("없는 메뉴입니다.")
                    continue
                else:
                    if item in orders:
                        orders[item] += quantity
                    else:
                        orders[item] = quantity
            pass
        
        case "주문 완료":
            print("=== 최종 주문 내역 ===")
            
            item_sum = 0

            for item, quantity in orders.items():
                item_price = menu[item] * quantity
                print(f"{item}: {quantity}개, {item_price}원")
                item_sum += item_price

            if item_sum >= 30000:
                account = item_sum // 10
            else:
                account = 0

            print(f"상품 금액: {item_sum}원")
            print(f"할인 금액: {account}원")
            print(f"결제 금액: {item_sum - account}원")
            
            break
        
        case _ :
            print("존재하지 않는 명령어입니다.")
            pass