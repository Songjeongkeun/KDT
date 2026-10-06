"""
ROI(Region of Interest)
이미지 전체가 아닌 특정 관심 영역만 선택해서 처리
"""

import cv2

img = cv2.imread("./images/sun.jpg")

x = 183
y = 22
w = 120
h = 110

roi = img[y:y+h, x:x+w]
roi_copy = roi.copy()

start_point = (x, y)
end_point = (x+w+w, y+h)
color = (0, 255, 0)
thickness = 2 
img[y:y+h, x+w:x+w+w] = roi_copy

cv2.rectangle(img, start_point, end_point, color, thickness)

cv2.imshow("original", img)
cv2.imshow("ROI result", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()