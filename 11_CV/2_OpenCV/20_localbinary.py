import cv2
import numpy as np

img = cv2.imread("./images/sudoku.jpg", cv2.IMREAD_GRAYSCALE)


# 전역 Otsu 이진화
otsu_threshold, global_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

print("otsu_threshold", otsu_threshold)

# 지역 Otsu 이진화
# 지역마다 서로 다른 자동 임계값을 사용함
local_otsu = np.zeros_like(img)
rows = 4
cols = 4

# np.linspace()
# 시작값부터 끝값까지 일정한 간격으로 원하는 개수만큼 숫자를 만들어주는 함수
# np.linspace(start, stop, num)
y_edge = np.linspace(0, img.shape[0], rows+1, dtype=int)
x_edge = np.linspace(0, img.shape[1], cols+1, dtype=int)

for row in range(rows):
    for col in range(cols):
        y1 = y_edge[row]
        y2 = y_edge[row + 1]
        x1 = x_edge[col]
        x2 = x_edge[col + 1]
        block = img[y1:y2, x1:x2]
        _, block_binary = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        local_otsu[y1:y2, x1:x2] = block_binary
# bw = img.shape[1] // 4
# # 위드는 1번 자리에 있다.
# bh = img.shape[0] // 4
# # 높이는 0번 자리에 있다.

# # 가로 세로 4등분 하기위해 이중포문을 사용
# for y in range(4):
#     for x in range(4):
#         # : 부터 시작해서
#         # 0이 나오지 않기 위해 ,threshold 입력값으로 주기 위해 입력 영상도 4등분
#         img_ = img[y*bh:(y+1)*bh, x*bw:(x+1)*bw]
#         # 지역 이진화도 똑같이 4등분을 해준다.
#         dst_ = local_otsu[y*bh:(y+1)*bh, x*bw:(x+1)*bw]

#         # cv2 ~ 맨 마지막에오는 dst는 출력영상을 의미한다, 대신 출력영상과 입력영상의 크기는 동일해야한다
#         # 앞에 img_ 는 입력영상이다
#         cv2.threshold(img_, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU, dst_)


# 적응형 이미지
# adaptiveThreshold(): 픽셀마다 주변 영역을 보고 임계값을 계산
# adaptiveThreshold(img, maxValue, blockSize, C)
# maxValue: 조건을 만족한 픽셀에 넣을 값, blockSize: 주변 영역의 크기. 반드시 3이상의 홀수, C: 계산된 주변 기준 값에서 빼는 상수
# T = 주변 평균(또는 가중 평균) - C
# C가 커지면 임계값 T가 낮아지므로 같은 영상에서는 흰색으로 판정되는 픽셀이 더 많아질 수 있음
block_size = 9
C = 5
# 주변 픽셀의 단순 평균을 기준으로 사용
adaptive_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)

# 주변 픽셀에 Gaussian 가중치를 적용한 평균을 기준으로 사용
adaptive_gaussian = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)

cv2.imshow("orginal", img)
cv2.imshow("global_otsu", global_otsu)
cv2.imshow("region_otsu", local_otsu)
cv2.imshow("adaptive_mean", adaptive_mean)
cv2.imshow("adaptive_gaussian", adaptive_gaussian)

cv2.waitKey(0)
cv2.destroyAllWindows()