import cv2
import sys

cap1 = cv2.VideoCapture("./movies/232538_tiny.mp4")
cap2 = cv2.VideoCapture("./movies/276624_tiny.mp4")

if not cap1.isOpened or not cap2.isOpened():
    print('입력 동영상 중 하나 이상을 열 수 없습니다.')
    sys.exit()
    
width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps1 = cap1.get(cv2.CAP_PROP_FPS)
fps2 = cap2.get(cv2.CAP_PROP_FPS)

print('너비: ', width)
print('높이: ', height)
print('FPS1: ', fps1)
print('FPS2: ', fps2)

# fourcc(Four Character code)
# 4개의 문자로 동영상 코덱을 지정하는 코드

"""
1920 * 1080 * 3byte = 6.2MB 
1초에 30fps > 186MB
1분 > 11GB

코덱 / 동영상 포멧

.mp4, avi, mov, mkv ..: 컨테이너. 동영상 파일 포맷
H.264, H265, XVID, MJPEG, AVI: 코덱(압축하는 알고리즘)

movie.mp4
MP4 컨테이너
Video: H.264
Audio: AAC
자막 / 시간정보 등 ..

코텍의 종류
XVID, MJPG, H.264(H264), H.265/HEVC(H265), VP9, AV1
"""

# *: unpacking > 'x', 'y', 'i', 'd'
fourcc = cv2.VideoWriter_fourcc(*"XVID") # XVID : avi 확장 컨테이너에서 Video 를 압축하는 코덱
out = cv2.VideoWriter("mix.avi", fourcc, fps1, (width, height))

if not out.isOpened():
    cap1.release()
    cap2.release()
    raise RuntimeError('출력 동영상 파일을 생성할 수 없습니다.')

delay = max(1, round(1000 / fps1))
stop = False

for cap in (cap1, cap2):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, (width, height))
        out.write(frame)
        cv2.imshow('output', frame)
        if cv2.waitKey(delay) == 27:
            stop = True
            break
    if stop:
        break
    
cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()