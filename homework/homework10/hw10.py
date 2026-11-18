import numpy as np

# ---------- 1. 單變數:數值微分與積分 ----------
def derivative(f, x, h=1e-5):
    """中央差分 f'(x) ≈ (f(x+h)-f(x-h))/2h"""
    return (f(x + h) - f(x - h)) / (2 * h)

def integrate_1d(f, a, b, n=100000):
    """中點黎曼和"""
    dx = (b - a) / n
    x = a + (np.arange(n) + 0.5) * dx
    return np.sum(f(x)) * dx

# ---------- 2. 單變數:蒙地卡羅積分 ----------
def mc_1d(f, a, b, N=1_000_000, rng=np.random.default_rng(0)):
    x = rng.uniform(a, b, N)
    return (b - a) * np.mean(f(x))

# ---------- 3. n 變數:梯度 ----------
def gradient(f, x, h=1e-5):
    x = np.asarray(x, dtype=float)
    g = np.zeros_like(x)
    for i in range(len(x)):
        e = np.zeros_like(x); e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g

# ---------- 5-1. n 變數黎曼積分(中點法)----------
def integral(f, low, high, k=10, batch=200_000, max_points=5e7):
    """每個維度切 k 格,共 k^n 個點。f 接受 shape (m, n) 的陣列。"""
    low, high = np.asarray(low, float), np.asarray(high, float)
    n = len(low)
    total = float(k) ** n
    if total > max_points:
        raise MemoryError(f"需要 k^n = {k}^{n} ≈ {total:.2e} 個格點,算不完(維度災難)")
    dx = (high - low) / k
    dV = np.prod(dx)
    # 每個維度的中點座標
    mids = [low[i] + (np.arange(k) + 0.5) * dx[i] for i in range(n)]
    s = 0.0
    idx = np.arange(int(total))
    for start in range(0, int(total), batch):
        chunk = idx[start:start + batch]
        pts = np.empty((len(chunk), n))
        r = chunk.copy()
        for d in range(n - 1, -1, -1):      # 把一維編號轉成 n 維格子座標
            pts[:, d] = mids[d][r % k]
            r //= k
        s += np.sum(f(pts))
    return s * dV

# ---------- 5-2. n 變數蒙地卡羅積分 ----------
def integral_mc(f, low, high, N=1_000_000, rng=np.random.default_rng(0)):
    low, high = np.asarray(low, float), np.asarray(high, float)
    V = np.prod(high - low)                  # 超體積
    x = rng.uniform(low, high, size=(N, len(low)))
    return V * np.mean(f(x))

# ---------- 測試:f(x) = x1² + ... + xn²,區域 [0,1]^n,真值 = n/3 ----------
if __name__ == "__main__":
    # 1~2 單變數
    print("f'(1) of x^2:", derivative(lambda x: x**2, 1.0))          # ≈ 2
    print("∫0~1 x^2 (Riemann):", integrate_1d(lambda x: x**2, 0, 1)) # ≈ 1/3
    print("∫0~1 x^2 (MC):", mc_1d(lambda x: x**2, 0, 1))

    # 3 梯度
    f = lambda x: np.sum(x**2, axis=-1)
    print("grad at (1,2,3):", gradient(f, [1, 2, 3]))                 # ≈ [2,4,6]

    # 5 各維度比較
    for n in [1, 2, 5, 100]:
        low, high = np.zeros(n), np.ones(n)
        exact = n / 3
        try:
            r = integral(f, low, high, k=10)
        except MemoryError as e:
            r = f"失敗:{e}"
        m = integral_mc(f, low, high, N=1_000_000)
        print(f"n={n:3d} 真值={exact:.4f}  Riemann={r}  MC={m:.4f}")
