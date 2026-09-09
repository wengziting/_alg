import time
import sys

sys.setrecursionlimit(2000)

def power2n_1(n):
    return 2**n

def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)


def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)


memo = {}
def power2n_3(n):
    if n == 0:
        return 1
    if n in memo:
        return memo[n]

    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    return memo[n]


def test_performance(func, n, func_name, timeout=3.0):
    start_time = time.time()
    try:
        if func_name == "方法 2a" and n > 30:
            print(f"[{func_name}] n={n} 預估執行時間過長 (超時跳過)，無法在合理時間內算完！")
            return
            
        result = func(n)
        elapsed = (time.time() - start_time) * 1000 
        print(f"[{func_name}] n={n} | 執行時間: {elapsed:.4f} ms | 結果位數: {len(str(result))} 位數")
    except Exception as e:
        print(f"[{func_name}] 執行失敗，錯誤訊息: {e}")

if __name__ == "__main__":
    test_n = 100
    print(f"=== 開始計算 2^{test_n} 效能測試 ===")
    
    test_performance(power2n_1, test_n, "方法 1")
    test_performance(power2n_2a, test_n, "方法 2a")
    test_performance(power2n_2b, test_n, "方法 2b")
    test_performance(power2n_3, test_n, "方法 3 (遞迴+查表)")
