import cv2
import sys

# 녹색 배경 동영상 불러오기
cap_forground = cv2.VideoCapture("./movies/woman.mp4")

if not cap_forground.isOpened():
    print("video open failed")
    sys.exit()

# 바다 배경 동영상 불러오기
cap_background = cv2.VideoCapture("./movies/sea.mp4")

if not cap_background.isOpened():
    print("video open failed")
    sys.exit()
    
w = round(cap_forground.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(cap_forground.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_cnt1 = round(cap_forground.get(cv2.CAP_PROP_FRAME_COUNT))
frame_cnt2 = round(cap_background.get(cv2.CAP_PROP_FRAME_COUNT))
fps = round(cap_forground.get(cv2.CAP_PROP_FPS))

# 프레임 간 시간 간격 설정 
delay = max(1, round(1000 / fps)) if fps > 0 else 30

# 전체 동영상 재생
while True: # 무한 루프
    ret1, frame1 = cap_forground.read() # 녹색 배경 영상 읽어오기
    
    if not ret1: # 영상1 프레임이 끝나면 종료
        break
    
    ret2, frame2 = cap_background.read() # 바다 영상 읽어오기
    
    if not ret2: #영상 2 프레임이 끝나면 종료
        cap_background.set(cv2.CAP_PROP_POS_FRAMES, 0) # set: background frame을 처음으로 돌아가게 해주는 함수
        ret2, frame2 = cap_background.read()
        if not ret2:
            break
        
    # 두 영상 크기가 다르면 배경 영상을 전경 영상 크기에 맞춤
    frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
    # 전경 영상을 HSV로 변환
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    
    lower_green = (50, 150, 0)
    upper_green = (90, 255, 255)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    result = frame1.copy()
    cv2.copyTo(frame2, green_mask, result)
    
    cv2.imshow("chromakey", result)
    cv2.imshow("mask", green_mask)
    
    key = cv2.waitKey(delay)
    
    if key == ord(" "):
        cv2.waitKey(0)
    elif key == 27:
        break
    # # HSV 색 공간에서 녹색 영역을 검출하여 합성
    # hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    # mask = cv2.inRange(hsv, (50, 150, 0), (70, 255, 255)) # 영상, 최솟값, 최댓값
    # cv2.copyTo(frame2, mask, frame1)
        
    # cv2.imshow('frame', frame1)
    # key = cv2.waitKey(delay)
    
    # if key == 27: # esc 누르면 영상 종료
    #     break
        
cap_forground.release() # 사용자 자원 해제
cap_background.release()
cv2.destroyAllWindows()