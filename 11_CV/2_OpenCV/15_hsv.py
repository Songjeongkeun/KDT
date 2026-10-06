"""
HSV
색을 사람이 느끼는 방식에 조금 더 가깝게 표현하는 색 공간

H: 무슨 색. 색상환 형태(0~179)
S: 얼마나 선명한 색(0~255)
V: 얼마나 밝은가(0~255)

H 범위
빨강: 0 ~
노링: 약 30 ~
초록: 약 60 ~
청록: 약 90 ~
파랑: 약 120 ~ 
보라: 약 150 ~ 179
"""

import cv2

img = cv2.imread("./images/candies.png")
airplane = cv2.imread("./images/airplane.bmp")
field = cv2.imread("./images/field.bmp")
mask = cv2.imread("./images/mask_plane.bmp", cv2.IMREAD_GRAYSCALE)
# 의료영상 label 만드는 법: 4만 x 4만 의료 이미지 사용 -> 해당 부분(위, 신장)을 mask로 만듬 

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 파란색에 해당하는 HSV 범위를 지정
# 실제 영상에서는 조명과 카메라에 따라 범위를 적절하게 조정 
lower_blue = (90, 150, 0)
upper_blue = (150, 255, 255)

# 범위 안에 있는 픽셀은 255(흰색), 범위 밖에 픽셀은 0(검정)인 마스크를 만듦
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

# mask 부분에 해당되는 부분만 뽑아서 저장해준다.
airplane_only = cv2.copyTo(airplane, mask)
composite = field.copy()
cv2.copyTo(airplane, mask, composite)

cv2.imshow("original", img)
cv2.imshow("blue mask", blue_mask)
cv2.imshow('airplane_only', airplane_only)
cv2.imshow('composite', composite)

cv2.waitKey(0)
cv2.destroyAllWindows()