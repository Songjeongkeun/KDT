import cv2
import numpy as np

img = cv2.imread("./images/dog.bmp")

h, w = img.shape[:2]

# 이동(translation)
"""
2 * 3 이동 변환 행렬
[ 1 0 tx ] 
[ 0 1 ty ]
tx = x 축 이동 거리 
ty = y 축 이동 거리

"""
aff_translate = np.array([
    [1, 0, 150],
    [0, 1, 100]
], dtype=np.float32)

dst_translate = cv2.warpAffine(img, aff_translate, (w, h)) # 어떤 변환을 적용시키는 함수, 이미지 크기도 명시 

# 크기 변걍(Resize)
# 보간(Interpolation): 이미 알고 있는 주변 값들을 이용해서 중간에 필요한 값을 추정하는 것
# INTER_NEAREST: 최근접 이웃. 가장 가까운 픽셀 사용
# INTER_LINEAR: 선형 보간. 주변 픽셀을 이용해서 계산
# INTER_CUBIC: 3차 보간. 더 넓은 주변 픽셀을 이용해 부드럽게 계산
# INTER_AREA: 영역 보간. 축소할 때 주로 사용
dst_nearest = cv2.resize(img, (1280, 1024), interpolation=cv2.INTER_NEAREST) # pixel의 개수를 늘리거나 줄여서 해당 해상도를 늘리거나 줄이는 함수
dst_cubic = cv2.resize(img, (1280, 1024), interpolation=cv2.INTER_CUBIC) # pixel의 개수를 늘리거나 줄여서 해당 해상도를 늘리거나 줄이는 함수


# 회전
center = (w / 2, h / 2)
# getRoationMatirx2D(회전 중심좌표, 회전 각도, 확대/축소 비율)
# 회전 각도는 양수일 경우 반시계 반향
rot_matrix = cv2.getRotationMatrix2D(center, 30, 0.7) # 반시계 반향으로 회전
dot_rotate = cv2.warpAffine(img, rot_matrix, (w, h))

cv2.imshow("orginal", img)
cv2.imshow("translate", dst_translate)
cv2.imshow("dst_nearest", dst_nearest)
cv2.imshow("dst_cubic", dst_cubic)
cv2.imshow("rotate", dot_rotate)

cv2.waitKey(0)
cv2.destroyAllWindows()

