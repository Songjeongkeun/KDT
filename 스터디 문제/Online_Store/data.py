# data.py

class Member:
    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):
        username = username.strip()
        
        if not username:
            raise ValueError("아이디는 꼭 입력해야 합나다.")
        self.__username = username
        
    @property
    def password(self):
        return self.__password
    
    @password.setter
    def password(self, password):
        password = password.strip()
        
        if not password:
            raise ValueError("비밀번호는 꼭 입력해야 합니다.")
        self.__password = password
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        name = name.strip()
        
        if not name:
            raise ValueError("이름은 꼭 입력해야 합니다.")
        self.__name = name 
        
    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        email = email.strip()
        
        if not email:
            raise ValueError("이메일은 꼭 입력해야 합니다.")
        self.__email = email
        
        
class Product:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock
        
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        name = name.strip()
        
        if not name:
            raise ValueError("이름은 꼭 입력해야 합니다.")
        self.__name = name 
        
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("상품 가격은 음수가 될 수 없습니다.")
        self.__price = price
        
    @property
    def stock(self):
        return self.__stock
    
    @stock.setter
    def stock(self, stock):
        if stock < 0:
            raise ValueError("재고 수량은 음수가 될 수 없습니다.")
        self.__stock = stock
        
class OrderHeader:
    status_list = ["ready", "paid", "shipping", "done", "cancel"]
    
    def __init__(self, member_id, total_price, status="ready"):
        self.member_id = member_id
        self.total_price = total_price
        self.status = status
        
    @property
    def member_id(self):
        return self.__member_id
    
    @member_id.setter
    def member_id(self, member_id):
        if member_id <= 0:
            raise ValueError("회원 번호를 확인해주세요. ")
        self.__member_id = member_id
        
    @property
    def total_price(self):
        return self.__total_price
    
    @total_price.setter
    def total_price(self, total_price):
        if total_price < 0:
            raise ValueError("주문 전체 금액을 확인해주세요. ")
        self.__total_price = total_price
        
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, status):
        status = status.strip()
        if status not in self.status_list:
            raise ValueError("주문 상태를 확인해주세요. ")
        self.__status = status        

class OrderItem:
    def __init__(self, product_id, quantity, price):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        
    @property
    def product_id(self):
        return self.__product_id
    
    @product_id.setter
    def product_id(self, product_id):
        if product_id <= 0:
            raise ValueError("상품 번호를 확인해주세요.")
        self.__product_id = product_id
    
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, quantity):
        if quantity <= 0:
            raise ValueError("주문 수량을 확인해주세요. 주문 수량은 1개 이상입니다. ")
        self.__quantity = quantity
        
    @property
    def price(self):
        return self.__price
    
    @price.setter
    def price(self, price):
        if price < 0:
            raise ValueError("상품 가격을 확인해주세요.")
        self.__price = price
        
        
class Payment:
    method_list = ["card", "bank"]
    def __init__(self, order_id, method, paid_amount):
        self.order_id = order_id
        self.method = method
        self.paid_amount = paid_amount
        
    @property
    def order_id(self):
        return self.__order_id
    
    @order_id.setter
    def order_id(self, order_id):
        if order_id <= 0:
            raise ValueError("주문 번호를 확인해주세요.")
        self.__order_id = order_id 
        
    @property
    def method(self):
        return self.__method
    
    @method.setter
    def method(self, method):
        method = method.strip()
        if method not in self.method_list:
            raise ValueError("결제 방식을 확인해주세요.")
        self.__method = method
    
    @property
    def paid_amount(self):
        return self.__paid_amount
    
    @paid_amount.setter
    def paid_amount(self, paid_amount):
        if paid_amount < 0:
            raise ValueError("결제 금액을 확인해주세요. ")
        self.__paid_amount = paid_amount

        
    
