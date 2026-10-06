import cv2
import matplotlib.pyplot as plt

"""
이진화
픽셀 값을 두 그룹으로 나누는 영상 처리 기법

일반적인 8비트 이진 영상 > 검정(0), 흰색(255)

OCR, 문서 스캔, 윤곽선 검출, 객체 분리 등의 전처리에서 자주 사용됨
"""

img = cv2.imread("./images/cells.png", cv2.IMREAD_GRAYSCALE)

hist = cv2.calcHist([img], [0], None, [256], [0, 256])


# 픽셀값 > threshold : 최대값
# 픽셀값 <= threshold : 0
threshold1, dst1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
print("임계값 1: ", threshold1)

threshold2, dst2 = cv2.threshold(img, 210, 255, cv2.THRESH_BINARY)
print("임계값 2: ", threshold2)

"""
Otsu 자동 임계값
THRESH_OTSU를 사용하면 임계값을 사람이 직접 정하지 않고 영상의 히스토그램을 이용해 OpenCV가 임계값을 자동으로 선택
"""
otsu_threshold, dst_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
print("임계값 otsu: ", otsu_threshold)

cv2.imshow("original", img)
cv2.imshow("threshold 100", dst1)
cv2.imshow("threshold 210", dst2)
cv2.imshow("threshold otsu", dst_otsu)

plt.plot(hist)
plt.title("Grayscale Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Count")
plt.xlim([0, 256])
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()


