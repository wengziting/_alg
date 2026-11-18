import numpy as np

# ===== 1. 單變數:數值微分與積分 =====
def derivative(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)           

def integrate_1d(f, a, b, n=100_000):
    dx = (b - a) / n
    x = a + (np.arange(n) + 0.5) * dx               
    return np.sum(f(x)) * dx

# ===== 2. 單變數:蒙地卡羅積分 =====
def mc_1d(f, a, b, N=1_000_000, rng=None):
    rng = rng or np.random.default_rng(0)
    return (b - a) * np.mean(f(rng.uniform(a, b, N)))

# ===== 3. n 變數:梯度(微分)與黎曼積分(超體積) =====
def gradient(f, x, h=1e-5):
    x = np.asarray(x, float)
    g = np.zeros_like(x)
    for i in range(len(x)):
        e = np.zeros_like(x); e[i] = h
        g[i] = (f(x + e) - f(x - e)) / (2 * h)
    return g

# ===== 5. integral(f, low, high):n = len(low) =====
def integral(f, low, high, k=10, batch=200_000, max_points=5e7):
    low, high = np.asarray(low, float), np.asarray(high, float)
    n = len(low)
    total = float(k) ** n
    if total > max_points:
        raise MemoryError(f"需要 k^n = {k}^{n} ≈ {total:.2e} 個格點,算不完(維度災難)")
    dx = (high - low) / k
    dV = np.prod(dx)
    mids = [low[i] + (np.arange(k) + 0.5) * dx[i] for i in range(n)]
    total = int(total)
    idx = np.arange(total)
    s = 0.0
    for start in range(0, total, batch):
        chunk = idx[start:start + batch]
        pts = np.empty((len(chunk), n))
        r = chunk.copy()
        for d in range(n - 1, -1, -1):
            pts[:, d] = mids[d][r % k]
            r //= k
        s += np.sum(f(pts))
    return s * dV

# ===== 4 / 6. n 變數蒙地卡羅積分 =====
def integral_mc(f, low, high, N=1_000_000, rng=None):
    rng = rng or np.random.default_rng(0)
    low, high = np.asarray(low, float), np.asarray(high, float)
    V = np.prod(high - low)
    return V * np.mean(f(rng.uniform(low, high, size=(N, len(low)))))

# ===================== 測試 =====================
if __name__ == "__main__":
    print("== 1. 單變數數值微分/積分 ==")
    print("d/dx x^2 @1 =", derivative(lambda x: x**2, 1.0), "(真值 2)")
    print("∫0~1 x^2    =", integrate_1d(lambda x: x**2, 0, 1), "(真值 1/3)")

    print("\n== 2. 單變數蒙地卡羅 ==")
    print("∫0~1 x^2    =", mc_1d(lambda x: x**2, 0, 1), "(真值 1/3)")

    print("\n== 3. n 變數梯度 ==")
    f = lambda x: np.sum(x**2, axis=-1)
    print("∇f @(1,2,3) =", gradient(f, [1, 2, 3]), "(真值 [2,4,6])")

    print("\n== 5. 黎曼積分 f=Σxi², low=0, high=1 ==")
    for n in [1, 2, 5, 100]:
        try:
            r = f"{integral(f, np.zeros(n), np.ones(n)):.6f}"
        except MemoryError as e:
            r = f"失敗 ({e})"
        print(f"n={n:3d}  真值={n/3:.6f}  黎曼={r}")

    print("\n== 4 / 6. 蒙地卡羅 f=Σxi², low=0, high=1 ==")
    for n in [1, 2, 5, 100]:
        m = integral_mc(f, np.zeros(n), np.ones(n))
        print(f"n={n:3d}  真值={n/3:.6f}  MC={m:.6f}  誤差={abs(m-n/3):.2e}")
