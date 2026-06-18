def solution(A, B):
    if A == B:
        return 0   
    
    for i in range(len(A)):
        A = A[-1] + A[:-1]
        if A == B:
            return 1   

    return -1

print(solution("hello", "ohell"))
print(solution("apple", "elppa"))
print(solution("atat", "tata"))
print(solution("abc", "abc"))