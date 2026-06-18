def solution(emergency):
    result = []
    sorted_emergency = sorted(emergency, reverse=True)
        
    for n in emergency:
        rank = sorted_emergency.index(n) + 1
        result.append(rank)
    
    return result
    
print(solution([3, 76, 4]))   
print(solution([1, 2, 3, 4, 5, 6, 7]))
print(solution([30, 10, 23, 6, 100]))