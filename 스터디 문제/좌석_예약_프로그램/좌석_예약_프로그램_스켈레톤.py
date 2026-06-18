seats = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
reserved = []

while True:
    print("1. 좌석 예약")
    print("2. 예약 취소")
    print("3. 예약 현황 보기")
    print("4. 종료")

    menu = input("메뉴 입력: ")

    match menu:
        case "1":
            # TODO: 리스트 컴프리헨션으로 예약 가능한 좌석 목록 만들기
            # 힌트: seats에는 있지만 reserved에는 없는 좌석만 담기
            available_seats = []

            print(f"예약 가능한 좌석: {available_seats}")

            # TODO: 좌석 번호 입력받기
            # 힌트: 대소문자를 구분하지 않도록 upper() 사용하기
            seat = ""

            # TODO: 좌석 예약 조건 처리하기
            # 1. seat가 available_seats에 있으면 reserved에 추가
            # 2. seat가 reserved에 있으면 이미 예약된 좌석 메시지 출력
            # 3. seat가 seats에 없으면 없는 좌석 메시지 출력
            pass

        case "2":
            print(f"예약된 좌석: {reserved}")

            # TODO: 취소할 좌석 번호 입력받기
            # 힌트: 대소문자를 구분하지 않도록 upper() 사용하기
            seat = ""

            # TODO: 예약 취소 조건 처리하기
            # 1. seat가 reserved에 있으면 reserved에서 제거
            # 2. seat가 seats에는 있지만 reserved에는 없으면 예약되지 않은 좌석 메시지 출력
            # 3. seat가 seats에 없으면 없는 좌석 메시지 출력
            pass

        case "3":
            # TODO: 리스트 컴프리헨션으로 예약 가능한 좌석 목록 만들기
            available_seats = []

            # TODO: 예약 현황 출력하기
            # 예약 현황, 예약 좌석수, 남은 좌석수, 예약 가능한 좌석을 출력한다.
            pass

        case "4":
            print("프로그램 종료")

            # TODO: 최종 예약 현황 출력하기
            # 최종 예약 현황과 최종 예약 좌석수를 출력한다.

            break

        case _:
            print("잘못된 메뉴입니다. 다시 입력해주세요.")

    print()
