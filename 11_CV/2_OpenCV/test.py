import cv2
import os
import time

# 웹캠 번호: 기본 웹캠은 보통 0
CAMERA_INDEX = 0

# 얼굴 이미지를 저장할 크기
SAVE_SIZE = (224, 224)

# 사람 한 명당 수집할 얼굴 이미지 수
TARGET_IMAGE_COUNT = 100

# 이미지 저장 간격(초)
SAVE_INTERVAL = 0.2


def get_largest_face(faces):
    """
    웹캠에 여러 명이 잡혔을 때,
    가장 크게 검출된 얼굴 하나를 선택하는 함수
    """
    if len(faces) == 0:
        return None

    # 얼굴 박스의 넓이(w * h)가 가장 큰 얼굴 반환
    return max(faces, key=lambda face: face[2] * face[3])


def apply_filter(frame, mode, brightness, contrast):
    """
    선택된 필터를 웹캠 프레임에 적용하는 함수

    mode
    0: 원본
    1: 흑백
    2: 블러
    3: 엣지 검출
    4: 밝기 및 대비 조절
    """

    if mode == 0:
        return frame

    if mode == 1:
        # BGR 이미지를 흑백으로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 화면 출력 형식을 맞추기 위해 다시 BGR로 변환
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    if mode == 2:
        # Gaussian Blur 적용
        return cv2.GaussianBlur(frame, (15, 15), 0)

    if mode == 3:
        # 엣지 검출은 흑백 이미지에서 수행
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 160)

        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    if mode == 4:
        # contrast 값은 0~100이므로 50을 기준값으로 사용
        alpha = contrast / 50.0

        # brightness 값도 50을 기준으로 밝거나 어둡게 조절
        beta = brightness - 50

        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    return frame


def draw_glasses(frame, x, y, w, h):
    """AR 아이템 1: 얼굴 위치를 기준으로 안경 그리기"""

    # 얼굴 박스 높이를 기준으로 눈 위치를 대략 계산
    eye_y = y + int(h * 0.40)

    left_center = (x + int(w * 0.30), eye_y)
    right_center = (x + int(w * 0.70), eye_y)

    radius = int(w * 0.18)
    thickness = max(2, int(w * 0.03))

    # 안경 렌즈 2개
    cv2.circle(frame, left_center, radius, (0, 0, 0), thickness)
    cv2.circle(frame, right_center, radius, (0, 0, 0), thickness)

    # 렌즈 사이 연결 부분
    cv2.line(
        frame,
        (left_center[0] + radius, eye_y),
        (right_center[0] - radius, eye_y),
        (0, 0, 0),
        thickness,
    )


def draw_hat(frame, x, y, w, h):
    """AR 아이템 2: 얼굴 위에 모자 그리기"""

    # 얼굴 바깥 위쪽에도 모자가 보이도록 y값을 조절
    hat_top = max(0, y - int(h * 0.28))
    hat_bottom = y + int(h * 0.08)

    # 모자 몸통
    cv2.rectangle(
        frame,
        (x + int(w * 0.15), hat_top),
        (x + int(w * 0.85), hat_bottom),
        (255, 80, 30),
        -1,
    )

    # 모자 챙
    cv2.ellipse(
        frame,
        (x + w // 2, hat_bottom),
        (int(w * 0.55), int(h * 0.10)),
        0,
        0,
        180,
        (255, 80, 30),
        -1,
    )


def draw_mustache(frame, x, y, w, h):
    """AR 아이템 3: 얼굴 아래쪽에 콧수염 그리기"""

    center_x = x + w // 2
    center_y = y + int(h * 0.68)
    size = int(w * 0.18)

    # 타원 2개를 이용해 콧수염 모양 생성
    cv2.ellipse(
        frame,
        (center_x - size // 2, center_y),
        (size, size // 2),
        20,
        0,
        180,
        (40, 20, 10),
        -1,
    )

    cv2.ellipse(
        frame,
        (center_x + size // 2, center_y),
        (size, size // 2),
        160,
        0,
        180,
        (40, 20, 10),
        -1,
    )


def register_face(frame, face, user_name, image_count):
    """
    검출된 얼굴 영역만 잘라서 dataset/이름 폴더에 저장
    """

    x, y, w, h = face

    # 원본 프레임에서 얼굴 영역만 자르기
    face_img = frame[y:y + h, x:x + w]

    # 얼굴 이미지가 비어 있으면 저장하지 않음
    if face_img.size == 0:
        return

    # 모델 입력 크기에 맞게 224 x 224로 변경
    face_img = cv2.resize(face_img, SAVE_SIZE)

    # 예: dataset/song/ 폴더 생성
    save_dir = os.path.join("dataset", user_name)
    os.makedirs(save_dir, exist_ok=True)

    # 예: dataset/song/song_000.jpg
    file_path = os.path.join(
        save_dir,
        f"{user_name}_{image_count:03d}.jpg"
    )

    cv2.imwrite(file_path, face_img)
    print(f"저장 완료: {file_path}")


def main():
    # 웹캠 열기
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return

    # 웹캠 출력 크기 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # OpenCV에 포함된 Haar Cascade 얼굴 검출기 불러오기
    cascade_path = (
        cv2.data.haarcascades
        + "haarcascade_frontalface_default.xml"
    )

    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print("얼굴 검출기를 불러오지 못했습니다.")
        return

    # 화면 창 생성
    cv2.namedWindow("Smart Camera")
    cv2.namedWindow("Control")

    # 밝기와 대비를 조절할 트랙바 생성
    cv2.createTrackbar("Brightness", "Control", 50, 100, lambda x: None)
    cv2.createTrackbar("Contrast", "Control", 50, 100, lambda x: None)

    filter_mode = 0
    ar_item = 0

    register_mode = False
    user_name = ""
    image_count = 0
    last_save_time = 0

    while True:
        # 웹캠 프레임 읽기
        success, frame = cap.read()

        if not success:
            print("웹캠 프레임을 읽지 못했습니다.")
            break

        # 거울처럼 보이도록 좌우 반전
        frame = cv2.flip(frame, 1)

        # 얼굴 등록용 원본 이미지 보관
        original_frame = frame.copy()

        # Haar Cascade 얼굴 검출을 위해 흑백 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 위치 검출
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(80, 80),
        )

        # 여러 얼굴 중 가장 큰 얼굴 선택
        face = get_largest_face(faces)

        if face is not None:
            x, y, w, h = face

            # 검출된 얼굴 영역 표시
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2,
            )

            # 선택된 AR 아이템 적용
            if ar_item == 1:
                draw_glasses(frame, x, y, w, h)

            elif ar_item == 2:
                draw_hat(frame, x, y, w, h)

            elif ar_item == 3:
                draw_mustache(frame, x, y, w, h)

            # ------------------------------
            # 나중에 얼굴 분류 모델을 연결할 위치
            # ------------------------------
            # face_img = original_frame[y:y+h, x:x+w]
            # name, confidence = predict_identity(face_img)
            #
            # cv2.putText(
            #     frame,
            #     f"{name}: {confidence:.1%}",
            #     (x, y - 10),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.7,
            #     (0, 255, 0),
            #     2,
            # )

            # 얼굴 등록 모드일 때 일정 간격으로 이미지 저장
            now = time.time()

            if (
                register_mode
                and image_count < TARGET_IMAGE_COUNT
                and now - last_save_time >= SAVE_INTERVAL
            ):
                register_face(
                    original_frame,
                    face,
                    user_name,
                    image_count,
                )

                image_count += 1
                last_save_time = now

            # 목표 수만큼 저장하면 등록 종료
            if register_mode and image_count >= TARGET_IMAGE_COUNT:
                register_mode = False
                print(
                    f"{user_name} 등록 완료: "
                    f"{TARGET_IMAGE_COUNT}장"
                )

        # 트랙바 값 가져오기
        brightness = cv2.getTrackbarPos("Brightness", "Control")
        contrast = cv2.getTrackbarPos("Contrast", "Control")

        # 현재 선택된 영상 필터 적용
        result = apply_filter(
            frame,
            filter_mode,
            brightness,
            contrast,
        )

        # 현재 필터와 AR 아이템 상태 표시
        cv2.putText(
            result,
            f"Filter: {filter_mode} | AR: {ar_item}",
            (15, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        # 등록 중이면 저장 진행 상태 표시
        if register_mode:
            cv2.putText(
                result,
                f"Registering {user_name}: "
                f"{image_count}/{TARGET_IMAGE_COUNT}",
                (15, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

        # 결과 화면 출력
        cv2.imshow("Smart Camera", result)

        # 키보드 입력 읽기
        key = cv2.waitKey(1) & 0xFF

        # q: 프로그램 종료
        if key == ord("q"):
            break

        # 0~4: 필터 변경
        elif key == ord("0"):
            filter_mode = 0
        elif key == ord("1"):
            filter_mode = 1
        elif key == ord("2"):
            filter_mode = 2
        elif key == ord("3"):
            filter_mode = 3
        elif key == ord("4"):
            filter_mode = 4

        # a: AR 아이템 순서대로 변경
        elif key == ord("a"):
            ar_item = (ar_item + 1) % 4

        # n: 등록할 사람 이름 입력
        elif key == ord("n"):
            user_name = input("등록할 이름 입력: ").strip()

        # r: 얼굴 등록 시작
        elif key == ord("r"):
            if user_name:
                register_mode = True
                image_count = 0
                last_save_time = 0
                print(f"{user_name} 얼굴 등록을 시작합니다.")

            else:
                print("'n' 키를 눌러 이름을 먼저 입력하세요.")

    # 웹캠 연결 해제 및 모든 OpenCV 창 닫기
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()