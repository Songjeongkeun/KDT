import fruit
from fruits import apple_info, banana_info 
# from fruits.apple import func1
from fruits import *

fruit.print_fruit("사과")

result = fruit.add_quantity(10, 5)
print(result)

apple = fruit.Fruit("사과",10)
apple.print_info()

print("*" * 30)
print(apple_info())
print(banana_info())
print(func1())