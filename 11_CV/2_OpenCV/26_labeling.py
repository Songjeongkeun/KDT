import cv2

'''
연결 요소 라벨링(Connected Components Labeling)
이진 영상에서 서로 붙어 있는 흰색 픽셀 덩어리를 하나의 객체로 보고 번호를 붙이는 작업
'''

img = cv2.imread('./images/keyboard.bmp', cv2.IMREAD_GRAYSCALE)

_, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

dst = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# cv2.connectedComponentsWithStats()
# 라벨링을 수행하면서 객체에 대한 정보를 계산
# connectivity: 픽셀들이 어떤 방향으로 붙어 있으면 같은 객체로 판단할지를 결정
# count: 전체 라벨 개수. 배경도 하나의 라벨로 인식
# labels: 원본 영상과 크기가 같은 2차원 배열이며, 각각의 픽셀이 몇 번 객체에 속하는지 저장
# stats: 각 객체의 위치와 크기 정보. [left, top, width, height, area]
# centroids: 각 객체의 중심 좌표
count, labels, stats, centroids = cv2.connectedComponentsWithStats(img_bin, connectivity=8)
print('라벨 개수(배경 포함):', count)
print('라벨 개수(배경 제외):', count-1)

print('labels shape:', labels.shape)
print('labels 일부:', labels[:10, :10])

print('stats:')
print(stats)

print('centroids:')
print(centroids)

for i in range(1, count):
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]

    if area < 30:
        continue

    cx, cy  = centroids[i]

    cv2.rectangle(dst, (x, y), (x+w, y+h), (0, 255, 255), 2)
    cv2.circle(dst, (int(cx), int(cy)), 3, (0, 255, 255), -1)

cv2.imshow('img', img)
cv2.imshow('bin', img_bin)
cv2.imshow('labeling result', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()