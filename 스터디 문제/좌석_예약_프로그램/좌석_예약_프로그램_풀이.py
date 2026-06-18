seats = ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]
reserved = []

while True:
    print("1. 좌석 예약")
    print("2. 예약 취소")
    print("3. 예약 현황")
    print("4. 종료")
    
    menu = input("메뉴 이력: ")
    
    match menu:
        case "1":
            available_seats = [seat for seat in seats if seat not in reserved]
            print(f"예약 가능한 좌석: {available_seats}")
            seat = input("좌석 입력: ")
            seat =seat.upper() # 대문자로 변환
            if seat in available_seats:
                reserved.append(seat)
                print(f"{seat} 좌석 예약 완료")
                print()
            elif seat in reserved:
                print(f"{seat}는 이미 예약된 좌석입니다.")
                print()
            else:
                print("없는 좌석입니다.")
                print()
            pass
        case "2":
            print(f"예약된 좌석: {reserved}")
            seat = input("취소할 좌석 입력: ")
            seat = seat.upper() # 대문자로 변환
            if seat in reserved:
                reserved.remove(seat)
                print(f"{seat} 좌석 예약 취소 완료")
                print()
            elif seat in seats:
                print(f"{seat}는 예약되지 않은 좌석입니다.")
                print()
            else:
                print("없는 좌석입니다.")
                print() 
            pass
        case "3":
            available_seats = [seat for seat in seats if seat not in reserved]
            print(f"예약 현황: {reserved}")
            print(f"예약 좌석수: {len(reserved)}")
            print(f"남은 좌석수: {len(seats) - len(reserved)}")
            print(f"예약 가능한 좌석: {available_seats}")
            print()
            pass
        case "4":
            print("프로그램 종료")
            print("최종 예약 현황: ", reserved)
            print(f"최종 예약 좌석수: {len(reserved)}")
            break
        case _:
            print("잘못된 메뉴입니다. 다시 입력해주세요.")
            pass
        
            