# fruits/__init__.py
from .apple import info as apple_info, func1
from .banana import info as banana_info

# 예) import fruits
# 예) from fruits import apple_info, banana_info
# 예) from frutis import *
__all__ = ["apple_info", "banana_info", "func1"]