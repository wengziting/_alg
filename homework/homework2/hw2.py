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


