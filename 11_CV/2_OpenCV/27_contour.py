import cv2
import numpy as np

'''
윤곽선(Contour)
객체의 바깥 경계선을 이루는 좌표들의 집합
'''

img = cv2.imread('./images/contours.bmp', cv2.IMREAD_GRAYSCALE)
milkdrop = cv2.imread('./images/milkdrop.bmp', cv2.IMREAD_GRAYSCALE)

_, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
_, milk_bin = cv2.threshold(milkdrop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

'''
cv2.findContours(image, mode, method)
mode: 윤곽선 사이의 부모/자식 관계를 어떻게 가져올지 설정
    RETR_EXTERNAL: 바깥 윤곽선만 반환
    RETR_CCOMP: 바깥 윤곽선과 내부 윤곽선을 모두 반환
    RETR_LIST: 부모-자식 관계를 중요하게 관리하지 않고 모든 윤곽선을 반환
    RETR_TREE: 모든 윤곽선을 반환하며 부모-자식관계까지 전체 구조를 보존
method: 경계 좌표를 얼마나 자세하게 저장할 것인지 설정

contours: 모든 윤곽선. 하나의 좌표가 아니라 여러 좌표의 집합
RETR_CCOMP: 바깥 윤곽선과 내부 윤곽선을 모두 반환
CHAIN_APPROX_SIMPLE: 윤곽선 경계의 중간 좌표들을 줄임
hierarchy: 윤곽선끼리의 관계를 저장. 예) [2, -1, 1, -1] next, previous, first_child, parent
'''

contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

milk_contours, milk_hierarchy = cv2.findContours(milk_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

print('contours 개수:', len(contours))
print('milk contours 개수:', len(milk_contours))

print('hierarchy:')
print(hierarchy)

dst = cv2.cvtColor(img_bin, cv2.COLOR_GRAY2BGR)
cv2.drawContours(dst, contours, -1, (0, 0, 255), 2)

h, w = milk_bin.shape[:2]
dst_milk = np.zeros((h, w, 3), dtype=np.uint8)

for i, contour in enumerate(milk_contours):
    color = ((37 * i) % 256, (97 * i) % 256, (173 * i) % 256)
    cv2.drawContours(dst_milk, milk_contours, i, color, 2)

cv2.imshow('img_bin', img_bin)
cv2.imshow('dst', dst)
cv2.imshow('milk_bin', milk_bin)
cv2.imshow('dst_milk', dst_milk)

cv2.waitKey(0)
cv2.destroyAllWindows()