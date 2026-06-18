def solution(keyinput, board):
    left_max = -(board[0] // 2)
    right_max = board[0] // 2
    up_max = board[1] // 2
    down_max = -(board[1] // 2)
    
    x = 0
    y = 0
    
    for key in keyinput:
        if key == "up":
            if y < up_max:
                y += 1
        elif key == "down":
            if y > down_max:
                y -= 1
        elif key == "left":
            if x > left_max:
                x -= 1
        elif key == "right":
            if x < right_max:
                x += 1
                
    return [x, y]


print(solution(["left", "right", "up", "right", "right"], [11, 11]))
print(solution(["down" , "down", "down", "down", "down"], [7, 9]))