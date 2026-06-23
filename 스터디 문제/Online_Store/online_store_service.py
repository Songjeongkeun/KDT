# online_store_service.py
from data import Member, OrderHeader, OrderItem, Payment, Product
from online_store_dao import OnlineStoreDAO


class OnlineStoreService:
    def __init__(self):
        self.dao = OnlineStoreDAO()
        self.login_membership = None

    @staticmethod
    def print_product_list(product_list):
        print("=" * 60)
        print(f"{'ID':<5}{'상품명':<20}{'가격':>10}{'재고':>10}")
        print("=" * 60)

        for product in product_list:
            stock = "품절" if product["stock"] == 0 else f"{product['stock']}개"

            print(
                f"{product['id']:<5}"
                f"{product['name']:<20}"
                f"{product['price']:>10}원"
                f"{stock:>10}"
            )

        print("=" * 60)

    @staticmethod
    def print_order(order):
        print(
            f"주문번호: {order['id']} | "
            f"총금액: {order['total_price']}원 | "
            f"상태: {order['status']} | "
            f"주문일자: {order['created_at']}"
        )
        
    @staticmethod
    def print_order_detail(order):
        paid_status = "paid" if order["payment_id"] else "ready"

        print(
            f"주문번호: {order['id']} | "
            f"상품명: {order['product_name']} | "
            f"수량: {order['quantity']}개 | "
            f"가격: {order['price']}원 | "
            f"총금액: {order['total_price']}원 | "
            f"상태: {order['status']} | "
            f"결제여부: {paid_status}"
        )

    def is_login(self):
        return self.login_membership is not None

    def register_membership(self):
        while True:
            username = input("아이디를 입력하세요: ").strip()

            if self.dao.find_membership(username):
                print("이미 사용 중인 아이디입니다. 아이디를 다시 입력하세요.")
            else:
                break
        password = input("비밀번호를 입력하세요: ").strip()
        name = input("이름을 입력하세요: ").strip()

        while True:
            email = input("이메일을 입력하세요: ").strip()

            if self.dao.find_membership(email):
                print("이미 사용 중인 이메일입니다. 이메일을 다시 입력하세요.")
            else:
                break

        membership = Member(username, password, name, email)
        result = self.dao.insert_membership(membership)

        if result > 0:
            print("회원가입이 완료되었습니다. ")
        else:
            print("회원가입에 실패했습니다.")

    def login(self):
        username = input("아이디를 입력하세요: ").strip()
        password = input("비밀번호를 입력하세요: ").strip()

        membership = self.dao.login(username, password)

        if not membership:
            print("아이디 또는 비밀번호가 일치하지 않습니다.")
            return 0

        self.login_membership = membership
        print()
        print(f"{membership['name']}님, Online Store에 오신 것을 환영합니다.")
        return 1

    def logout(self):
        self.login_membership = None
        print("정상적으로 로그아웃되었습니다.")

    def get_product_list(self):
        product_list = self.dao.get_product_list()

        if not product_list:
            print("상품이 존재하지 않습니다.")
            return

        self.print_product_list(product_list)

    def search_product_list(self):
        keyword = input("검색할 상품명 키워드를 입력하세요: ").strip()
        product_list = self.dao.search_product_list(keyword)

        if not product_list:
            print("검색 결과 없음")
            return

        self.print_product_list(product_list)

    def order(self):
        product_id = int(input("주문할 상품 ID를 입력하세요: ").strip())
        quantity = int(input("주문 수량을 입력하세요: ").strip())
        product = self.dao.find_product(product_id)

        if not product:
            print("상품 ID를 확인하세요. ")
            return
        if quantity <= 0:
            print("주문 수량을 확인하세요.")
            return
        elif quantity > product["stock"]:
            print("재고가 부족합니다.")
            return

        item = OrderItem(product_id, quantity, product["price"])
        total_price = item.quantity * item.price

        print(f"주문 금액은 {total_price}원 입니다.")
        order_check = input("주문을 생성하시겠습니까?(y/n): ").strip().lower()

        if order_check == "n":
            print("주문이 취소되었습니다.")
            return

        order_header = OrderHeader(self.login_membership["id"], total_price)
        order_id = self.dao.create_order(order_header, item)

        if order_id:
            print("주문이 생성되었습니다.")

    def show_order_list(self):
        order_list = self.dao.select_order_list(self.login_membership["id"])

        if not order_list:
            print("주문 내역이 없습니다.")
            return

        for order in order_list:
            self.print_order(order)
        
        index_order = input("상세 조회할 주문 번호를 입력하세요(생략하려면 enter를 눌러주세요): ").strip()
        
        if index_order:
            self.show_order_detail(int(index_order))
        
        print()
        pay_check = input("모든 주문을 결제하시겠습니까?(y/n): ").strip().lower()

        if pay_check != "y":
            print("결제를 진행하지 않습니다.")
            return

        self.pay_order()
              
    def show_order_detail(self, order_id): 
        order = self.dao.select_order_header(order_id, self.login_membership["id"])
        
        if not order:
            print("주문 번호를 확인해주세요.")
            return
        
        self.print_order_detail(order)

    def pay_order(self):
        ready_order_list = self.dao.select_ready_order_list(self.login_membership["id"])

        if not ready_order_list:
            print("결제 가능한 주문이 없습니다.")
            return

        total_pay = 0

        print("결제 가능한 주문 목록입니다.")

        for order in ready_order_list:
            self.print_order(order)
            total_pay += order["total_price"]

        print(f"총 결제 금액은 {total_pay}원 입니다.")
        print("결제 방식을 선택하세요.")
        print("1. 카드")
        print("2. 계좌이체")

        method_int = int(input("결제 방식: ").strip())

        if method_int == 1:
            method = "card"
        elif method_int == 2:
            method = "bank"
        else:
            print("1. 카드 또는 2. 중 하나를 선택하세요.")
            return

        pay = int(input("결제 금액을 입력하세요: ").strip())

        if pay != total_pay:
            print("결제 금액이 총 주문 금액과 일치하지 않습니다.")
            return

        for order in ready_order_list:
            payment = Payment(order["id"], method, order["total_price"])
            self.dao.pay_order(payment)

        print("모든 주문의 결제가 완료되었습니다.")

 
