# 數值微分與積分(Python)

用數值方法計算單變數與 n 變數的微分、積分,並比較「黎曼積分」與「蒙地卡羅積分」在不同維度下的表現。

## 功能

| 項目 | 函數 | 方法 |
|---|---|---|
| 單變數微分 | `derivative(f, x, h)` | 中央差分 |
| 單變數積分 | `integrate_1d(f, a, b, n)` | 中點黎曼和 |
| 單變數積分 | `mc_1d(f, a, b, N)` | 蒙地卡羅 |
| n 變數微分(梯度) | `gradient(f, x, h)` | 逐維中央差分 |
| n 變數積分(超體積) | `integral(f, low, high, k)` | 中點黎曼和(每維切 k 格) |
| n 變數積分(超體積) | `integral_mc(f, low, high, N)` | 蒙地卡羅 |

## 環境需求

- Python 3.8+
- NumPy(`pip install numpy`)

## 程式碼(存成 `numerical_calculus.py`)

約定:`f` 的輸入是 shape 為 `(..., n)` 的陣列,沿最後一軸取變數。

```python
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
    print("f'(1) of x^2:", derivative(lambda x: x**2, 1.0))          # ≈ 2
    print("∫0~1 x^2 (Riemann):", integrate_1d(lambda x: x**2, 0, 1)) # ≈ 1/3
    print("∫0~1 x^2 (MC):", mc_1d(lambda x: x**2, 0, 1))

    f = lambda x: np.sum(x**2, axis=-1)
    print("grad at (1,2,3):", gradient(f, [1, 2, 3]))                 # ≈ [2,4,6]

    for n in [1, 2, 5, 100]:
        low, high = np.zeros(n), np.ones(n)
        exact = n / 3
        try:
            r = integral(f, low, high, k=10)
        except MemoryError as e:
            r = f"失敗:{e}"
        m = integral_mc(f, low, high, N=1_000_000)
        print(f"n={n:3d} 真值={exact:.4f}  Riemann={r}  MC={m:.4f}")
```

執行:

```bash
python numerical_calculus.py
```

## 測試案例

被積函數 `f(x) = x₁² + ... + xₙ²`,區域 `[0, 1]ⁿ`,真值 `n/3`(一般區間 `[a, b]` 為 `n·(b³ − a³)/3`)。

| 維度 n | 真值 | 黎曼積分(k=10) | 蒙地卡羅(N=10⁶) |
|---|---|---|---|
| 1 | 0.3333 | 誤差約 8e-4 | 誤差約 3e-4 |
| 2 | 0.6667 | 誤差約 2e-3 | 誤差約 4e-4 |
| 5 | 1.6667 | 10⁵ 個格點,誤差約 4e-3 | 誤差約 7e-4 |
| 100 | 33.333 | 需要 10¹⁰⁰ 個格點,無法計算 | 誤差約 3e-3 |

> 以上誤差為理論推算,尚未實際執行驗證,實際數值會依隨機種子略有不同。

## 原理說明

### 1. 單變數微分:中央差分

`f'(x) ≈ (f(x+h) − f(x−h)) / 2h`

- 泰勒展開後一階誤差項抵消,截斷誤差為 `h²·f'''(x)/6`,是二階精度。前向差分只有一階。
- h 太小會有浮點捨入誤差,約 `ε/h`(ε≈1e-16)。兩種誤差相加,最佳 h 約 `ε^(1/3) ≈ 6e-6`,所以預設 `1e-5` 合理。

### 2. 單變數積分:中點黎曼和

把 [a,b] 切成 n 格,每格取中點函數值乘以寬度 `dx` 再加總。

- 二階精度,誤差約 `(b−a)·dx²·f''/24`,比左右端點法(一階)準很多。
- 對 x² 在 [0,1] 切 10⁵ 格,誤差約 1e-11。

### 3. 單變數蒙地卡羅積分

`∫ₐᵇ f dx ≈ (b−a) · mean(f(Xᵢ)),Xᵢ ~ Uniform(a,b)`

- 積分等於「區間長度 × f 的期望值」,用樣本平均估計。
- 標準誤差 `(b−a)·σ_f/√N`。對 x² 在 [0,1],σ≈0.298,N=10⁶ 時誤差約 3e-4。
- 一維時黎曼法遠比蒙地卡羅準,蒙地卡羅的優勢在高維。

### 4. n 變數微分:梯度

`∇f(x) = [∂f/∂x₁, ..., ∂f/∂xₙ]`

- 每個分量用中央差分,只擾動第 i 個座標。
- 需要 2n 次函數呼叫,成本線性,沒有維度災難。

### 5. n 變數黎曼積分

每一維切 k 格,共 kⁿ 個小方盒,取中心點,`dV = Π(highᵢ−lowᵢ)/kⁿ`,`∫ f ≈ dV · Σ f(中心點)`。

- **編號轉座標**:用 `r % k` 與 `r //= k`(類似 k 進位)把一維編號轉成 n 維座標,不需要 n 層迴圈或 `meshgrid`。
- **分批計算**:每次 `batch` 個點,記憶體用量固定。
- **保護機制**:kⁿ 超過 `max_points` 直接報錯。
- **誤差**:f=Σxᵢ² 時約 `n·(1/k)²/12`。
- **成本**:kⁿ。n=100、k=10 是 10¹⁰⁰ 個點,遠超宇宙原子數(約 10⁸⁰)。

### 6. n 變數蒙地卡羅積分

`∫ f ≈ V · mean(f(Xᵢ)),Xᵢ ~ Uniform(方盒),V = Π(highᵢ−lowᵢ)`

- 成本 `N × n`,對維度線性。
- 誤差 `V·σ_f/√N` 的收斂速率與維度無關。f=Σxᵢ² 時 σ² = n·4/45,n=100 時 σ≈2.98,N=10⁶ 誤差約 0.003。
- 誤差降 10 倍需要 100 倍樣本。

### 7. 黎曼法 vs 蒙地卡羅

| | 黎曼法 | 蒙地卡羅 |
|---|---|---|
| 成本 | kⁿ(指數) | N×n(線性) |
| 誤差收斂 | `O(k⁻²)`,但高維時 k 受 kⁿ 限制 | `O(N⁻½)`,與維度無關 |
| 適用 | 約 1 到 3 維 | 高維度、不規則區域 |

## 使用注意事項

- `integral` / `integral_mc` 的 `f` 必須能一次吃 `(m, n)` 陣列,例如 `np.sum(x**2, axis=-1)`;`gradient` 的 `f` 則吃單一點 `(n,)` 並回傳純量。
- 題目「low, high 都是 1」我解讀為每維範圍 [0,1]。若是別的範圍,修改 `low`、`high` 即可。
- `rng` 預設在函數定義時建立一次,同一程式連續呼叫會接續同一個亂數序列。需要獨立結果時請每次傳入新的 `np.random.default_rng(seed)`。
- 想提升精度:黎曼法增加 k(注意 kⁿ),蒙地卡羅增加 N,或改用準蒙地卡羅(`scipy.stats.qmc` 的 Sobol 序列),收斂可接近 `O(N⁻¹)`。
