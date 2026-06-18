def solution(common):
    # 등차
    if (common[2] - common[1]) == (common[1] - common[0]):
        d = common[1] - common[0]
        return int(common[0] + len(common) * d)
    else:
        r = common[1] // common[0]
        ans = common[0]
        for i in range(len(common)):
            ans *= r
        return ans


print(solution([1, 2, 3, 4]))
print(solution([2, 4, 8]))