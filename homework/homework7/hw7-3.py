def min_distance_optimized(word1: str, word2: str) -> int:
    if len(word1) > len(word2):
        word1, word2 = word2, word1
        
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))
    
    for i in range(1, m + 1):
        new_dp = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                new_dp[j] = dp[j - 1]
            else:
                new_dp[j] = 1 + min(
                    dp[j],      
                    new_dp[j-1],
                    dp[j-1]    
                )
        dp = new_dp
        
    return dp[n]
print("空間優化解答案：", min_distance_optimized("horse", "ros"))  # 輸出: 3
