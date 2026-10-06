import cv2

"""
OpenCV의 산술 연산
이미지의 각 픽셀 값에 일정한 값을 더하거나 빼는 방식으로 밝기를 조절할 수 있음
"""


img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR)
bright_gray = cv2.add(img_gray, 100)
bright_color = cv2.add(img_color, (100, 100, 100)) # B G R
dark_gray = cv2.subtract(img_gray, 100)
multiply_gray = cv2.multiply(img_gray, 2)
divide_gray = cv2.divide(img_gray, 2)
# 0 ~ 255 값에서 벗어나게 되면 범위를 제한시킨다. ex) 255가 넘어가게되면 255로 제한한다.

cv2.imshow('gray', img_gray)
cv2.imshow('color', img_color)
cv2.imshow('birght_gray', bright_gray)
cv2.imshow('bright_color', bright_color)
cv2.imshow('dark_gray', dark_gray)
cv2.imshow('multiply_gray', multiply_gray)
cv2.imshow('divide_gray', divide_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
