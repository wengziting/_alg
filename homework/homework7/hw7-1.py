def min_distance_recursive(word1: str, word2: str) -> int:
    def helper(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if word1[i - 1] == word2[j - 1]:
            return helper(i - 1, j - 1)
        
        insert_op = helper(i, j - 1)    
        delete_op = helper(i - 1, j)      
        replace_op = helper(i - 1, j - 1) 
        
        return 1 + min(insert_op, delete_op, replace_op)

    return helper(len(word1), len(word2))

print("遞迴解答案：", min_distance_recursive("horse", "ros"))  
