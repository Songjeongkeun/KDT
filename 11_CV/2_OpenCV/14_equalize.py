import cv2
import matplotlib.pyplot as plt

img_gray = cv2.imread("./images/Hawkes.jpg", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/field.bmp")

"""
YCrCb
- 컬러 이미지를 표현하는 또 다른 색 공간
- 밝기와 색상 정보를 분리해서 저장
- Y: 밝기 정보, Cr(붉은 성향), Bb(푸른 성향): 색상 정보
"""

ycrcb = cv2.cvtColor(img_color, cv2.COLOR_BGR2YCrCb)
ycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0]) # 밝기 정보만 contrast
equalized_color = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)


"""
normalize()
- 정규화. 값의 범위 조정
- 값의 범위 조정
- 최솟값/최댓값
- 기본적으로 비율을 유지하며 변화
- 대비 개선이 주목적은 아님
- 데이터 범위 통일. 시각화. 전처리
"""

normalized_gray = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX) # 2번째 argument: output 영상 크기

"""
- 히스토그램 평활화
- 대비 향상
- 픽셀들의 분포
- 일반적으로 0 ~ 255
- 대비 개선에 특화
"""

equalized_gray = cv2.equalizeHist(img_gray)

hist_original = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
hist_equalized = cv2.calcHist([equalized_gray], [0], None, [256], [0, 256])
hist_normalized = cv2.calcHist([normalized_gray], [0], None, [256], [0, 256])

cv2.imshow("gray original", img_gray)
cv2.imshow("color original", img_color)
cv2.imshow("gray normaliszed ", normalized_gray)
cv2.imshow("gray equalized", equalized_gray)
cv2.imshow("color equalized", equalized_color)

plt.figure(figsize=(12, 4))
histograms = {'original': hist_original, 'equalized': hist_equalized, 'normalized': hist_normalized}

for i, (title, hist) in enumerate(histograms.items(), start=1):
    plt.subplot(1, 3, i)
    plt.plot(hist)
    plt.title(title)
    plt.xlim([0, 256])
plt.tight_layout()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()



