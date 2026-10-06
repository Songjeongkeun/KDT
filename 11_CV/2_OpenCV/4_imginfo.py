import cv2
import numpy as np

img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR 생략 가능
img_original = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR)

print('img_gray type: ', type(img_gray))    # <class 'numpy.ndarray' >
print('img_gray shape: ', img_gray.shape)   # (364, 548)
print('img_gray dtype: ', img_gray.dtype)   # uint8


print('img_color type: ', type(img_color))    # <class 'numpy.ndarray' >
print('img_color shape: ', img_color.shape)   # (364, 548, 3)
print('img_color dtype: ', img_color.dtype)   # uint8

h, w = img_color.shape[:2]
print(f'이미지 크기: {w} * {h}')

if img_color.ndim == 3:
    print('img_color는 컬러 이미징비니다.')
elif img_color.ndim == 2:
    print('img_color는 그레이스케일 이미지입니다.')
    
img1 = np.zeros((240, 320, 3), dtype=np.uint8) # 가로 320, 세로 240, 컬러(검은색)
# np.empty(): 메모리 공간만 할당하고 예츠할 수 없는 값을 저장함
img2 = np.empty((240, 320), dtype=np.uint8)
img3 = np.full((240, 320), 120, dtype=np.uint8)
img4 = np.full((240, 320, 3), (255, 102, 255), dtype=np.uint8)


height, width = img_color.shape[:2]

"""
for y in range(height):
    for x in range(width):
        img_color[y, x] = (255, 102, 255)
"""

img_color[:, :] = (255, 102, 255)


cv2.imshow('original', img_original)
cv2.imshow('img_color', img_color)
cv2.imshow('zeros', img1)
cv2.imshow('empty', img2)
cv2.imshow('full_120', img3)
cv2.imshow('full_color', img4)
# cv2.waitKey(0)

while True:
    key = cv2.waitKey(0)
    if key in (ord("i"), ord("I")): # ord() 함수: ASKII 코드 값을 반환해줌
        # uint8 이미지에서 ~(반전)은 각 필셀에 대해 (255 - 값)과 같은 결과를 만듦
        img_original = ~img_original
        cv2.imshow('original', img_original)
    elif key == 27:
        break


cv2.destroyAllWindows()