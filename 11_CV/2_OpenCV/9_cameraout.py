import cv2
import sys

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print('카메라를 열 수 없습니다.')
    sys.exit()

print('카메라 연결 성공!')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print('너비: ', width)
print('높이: ', height)
print('FPS: ', fps)

fourcc = cv2.VideoWriter_fourcc(*"XIVD")
out = cv2.VideoWriter("camera.avi", fourcc, fps, (width, height))

print(f'녹화 시작: {width}x{height}, {fps:.1f}FPS')
print('ESC 키를 누르면 녹화를 종료합니다.')

while True:
    ret, frame = cap.read()
    if not ret:
        print('카메라 프레임을 읽지 못했습니다.')
        break
    out.write(frame)
    cv2.imshow("camera", frame)
    if cv2.waitKey(1) == 27:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()