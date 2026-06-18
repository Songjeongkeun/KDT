def solution(babbling):
    words = ["aya", "ye", "woo", "ma"]
    count = 0
    for babble in babbling:
        for word in words:
            babble = babble.replace(word, " ")

        if babble.strip() == "":
            count += 1

    return count

print(solution(["aya", "yee", "u", "maa", "wyeoo"]))  
print(solution(["ayaye", "uuuma", "ye", "yemawoo", "ayaa"]))