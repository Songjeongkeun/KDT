import cv2

'''
모폴로지(Morphology)
- 이미지의 모양을 다듬는 연산
- 이진화된 이미지에서 흰색 영역을 기준으로 두껍게 만들거나, 얇게 만들거나, 작은 점을 없애거나, 구멍을 매우는 작업에 사용
- 작은 커널을 이미지 위에서 움직이면서 흰색 영역의 모양을 바꾸는 것

1. 침식
- 흰색 영역을 깎아냄
- cv2.erode()
- 작은 흰색 노이즈 제거

2. 팽창
- 흰색 영역을 바깥쪽으로 키움
- cv2.dilate()
- 끊어진 객체를 연결할 때

커널의 크기가 커지면 강한 효과를 낼 수 있음
'''

img = cv2.imread('./images/circuit.bmp', cv2.IMREAD_GRAYSCALE)

# getStructuringElement(): 모폴로지 연산에서 주변 픽셀을 어떤 모양으로 확인할지 결정
# MORPH_RECT(사각형), MORPH_ELLIPSE(타원), MORPH_CROSS(십자)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

# 팽창
dilated = cv2.dilate(img, kernel, iterations=1)

# 침식
eroded = cv2.erode(img, kernel, iterations=1)

# Opening
# 침식 > 팽창
# 작은 흰색 노이즈를 제거하기 위해
# 이미 제거된 작은 점은 다시 살아나기 어려움 > 주요 객체 크기 복원
opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

# Closing
# 팽창 > 침식
# 객체 내부에 작은 검은 구멍이나 끊어진 부분을 메우기 위해
# 작은 구멍을 제거 / 끊어진 선을 연결 후 전체 객체 크기를 다시 줄임
closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

cv2.imshow('original', img)
cv2.imshow('dilation', dilated)
cv2.imshow('erosion', eroded)
cv2.imshow('opened', opened)
cv2.imshow('closed', closed)

cv2.waitKey(0)
cv2.destroyAllWindows()