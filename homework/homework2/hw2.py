import math

# 1. T(n) = T(n-1) + 8, T(1) = 1
def T1_recur(n):
    if n == 1:
        return 1
    return T1_recur(n - 1) + 8

def T1_formula(n):
    return 8 * n - 7


# 2. T(n) = 2*T(n-1) + 9, T(1) = 1
def T2_recur(n):
    if n == 1:
        return 1
    return 2 * T2_recur(n - 1) + 9

def T2_formula(n):
    return 5 * (2**n) - 9


# 3. T(n) = 2*T(n/2) + 1, T(1) = 1 (假設 n 為 2 的次方)
def T3_recur(n):
    if n == 1:
        return 1
    return 2 * T3_recur(n // 2) + 1

def T3_formula(n):
    return 2 * n - 1


# 4. T(n) = T(n/2) + 1, T(1) = 1 (假設 n 為 2 的次方)
def T4_recur(n):
    if n == 1:
        return 1
    return T4_recur(n // 2) + 1

def T4_formula(n):
    return int(math.log2(n)) + 1


# 測試與驗證主程式
if __name__ == "__main__":
    print(f"{'題目':<12} | {'n':<6} | {'遞迴執行結果':<12} | {'公式計算結果':<12} | {'Big-O':<10}")
    print("-" * 65)

    # 測試題 1 (n=10)
    print(f"{'1. T(n-1)+8':<12} | {10:<6} | {T1_recur(10):<12} | {T1_formula(10):<12} | O(n)")

    # 測試題 2 (n=10)
    print(f"{'2. 2T(n-1)+9':<12} | {10:<6} | {T2_recur(10):<12} | {T2_formula(10):<12} | O(2^n)")

    # 測試題 3 (n=16)
    print(f"{'3. 2T(n/2)+1':<12} | {16:<6} | {T3_recur(16):<12} | {T3_formula(16):<12} | O(n)")

    # 測試題 4 (n=16)
    print(f"{'4. T(n/2)+1':<12} | {16:<6} | {T4_recur(16):<12} | {T4_formula(16):<12} | O(log n)")
