import cv2
import sys 

cap = cv2.VideoCapture("./movies/232538_tiny.mp4")

if not cap.isOpened():
    print('동영상을 불러올 수 없습니다.')
    sys.exit()

print('동영상 로드 성공!')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print('너비: ', width)
print('높이: ', height)
print('프레임 수: ', frame_count)
print('FPS: ', fps)

delay = max(1, round(1000 / fps)) if fps > 0 else 40

while True:
    # ret: 프레임을 정상적으로 읽었는지 여부
    # frame: 읽어온 한 장의 영상 프레임 (numpy 배열)
    ret, frame = cap.read()
    if not ret: 
        break
    cv2.imshow("frame", frame)
    if cv2.waitKey(delay) == 27:
        break
    
cap.release() # 메모리에서 객체 날림
cap.destroyAllWindows()
