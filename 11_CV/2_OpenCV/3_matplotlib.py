import cv2
import matplotlib.pyplot as plt

img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR 생략 가능

""" 
OpenCV의 RGB 색상 채널 순서: BGR
Matplotlib RGB 색상 채널 순서 : RGB
"""

img_color_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)

plt.subplot(1, 2, 1)
plt.axis("off")
plt.title("Grayscale")
plt.imshow(img_gray, cmap="gray")

plt.subplot(1, 2, 2)
plt.axis("off") # 격자 없앰
plt.title("Color")
plt.imshow(img_color_rgb)

plt.tight_layout() # 사진 안 찌그러지게 잡아줌
plt.show()