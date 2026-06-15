PI = 3.14

def print_fruit(name):
    print(f"{name}입니다.")

def add_quantity(quantity, amount):
    return quantity + amount

class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def print_info(self):
        print(f"과일 이름: {self.name}")
        print(f"수량: {self.quantity}")
        
def hello():
    print("과일 모듈입니다.")

print("__name__ 값:", __name__)

if __name__ == "__main__":
    print("직접 실행되었습니다.")
    hello()