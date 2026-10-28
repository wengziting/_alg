import sys, math, random
import numpy as np
 
N    = int(sys.argv[1]) if len(sys.argv) > 1 else 12
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 7
random.seed(SEED)
P = np.random.default_rng(SEED).random((N, 2)) * 100         
D = np.linalg.norm(P[:, None] - P[None], axis=2)            
 
def L(t):
    return sum(D[t[i], t[(i + 1) % N]] for i in range(N))
 
def rand_tour():
    t = list(range(N)); random.shuffle(t); return t
 
# ---------- 5. 貪婪 (最近鄰) ----------
def greedy(start=0):
    t, left = [start], set(range(N)) - {start}
    while left:
        c = min(left, key=lambda x: D[t[-1], x])
        t.append(c); left.remove(c)
    return t
 
# ---------- 1. 改良法 (2-opt) ----------
def two_opt(t):
    t, improved = t[:], True
    while improved:
        improved = False
        for i in range(1, N - 1):
            for j in range(i + 1, N):
                n = t[:i] + t[i:j + 1][::-1] + t[j + 1:]
                if L(n) < L(t) - 1e-9:
                    t, improved = n, True
    return t
 
# ---------- 2. 爬山----------
def hill_climb(iters=5000):
    t = rand_tour(); cur = L(t)
    for _ in range(iters):
        i, j = random.sample(range(N), 2)
        n = t[:]; n[i], n[j] = n[j], n[i]
        v = L(n)
        if v < cur: t, cur = n, v
    return t
 
# ---------- 3. 模擬退火 ----------
def simulated_annealing(T=100.0, alpha=0.999, Tmin=1e-3):
    t = rand_tour(); cur = L(t); best, bl = t[:], cur
    while T > Tmin:
        i, j = sorted(random.sample(range(N), 2))
        n = t[:i] + t[i:j + 1][::-1] + t[j + 1:]
        v = L(n)
        if v < cur or random.random() < math.exp((cur - v) / T):
            t, cur = n, v
            if cur < bl: best, bl = t[:], cur
        T *= alpha
    return best
 
# ---------- 4. 梯度下降 (彈性網路 Elastic Net) ----------
def elastic_net(iters=6000):
    M = 4 * N
    th = np.linspace(0, 2 * np.pi, M, endpoint=False)
    Y = P.mean(0) + 10 * np.c_[np.cos(th), np.sin(th)]   # 環上的點
    K = 30.0
    for it in range(iters):
        d2 = ((P[:, None] - Y[None]) ** 2).sum(2)
        W = np.exp(-d2 / (2 * K * K)); W /= W.sum(1, keepdims=True) + 1e-12
        pull = (W[:, :, None] * (P[:, None] - Y[None])).sum(0)       
        tension = np.roll(Y, 1, 0) - 2 * Y + np.roll(Y, -1, 0)       
        Y += 0.2 * pull + max(0.2 * K / 30, 0.02) * tension         
        if it % 20 == 0: K = max(K * 0.97, 1.0)                       
    key = [int(np.argmin(((Y - p) ** 2).sum(1))) for p in P]
    return [int(x) for x in np.argsort(key, kind="stable")]
 
# ---------- 最佳解  ----------
def held_karp():
    INF = 1e18; full = 1 << (N - 1)
    dp = [[INF] * (N - 1) for _ in range(full)]
    for j in range(N - 1): dp[1 << j][j] = D[N - 1][j]
    for m in range(full):
        for j in range(N - 1):
            if dp[m][j] >= INF or not m >> j & 1: continue
            for k in range(N - 1):
                if m >> k & 1: continue
                v = dp[m][j] + D[j][k]
                if v < dp[m | 1 << k][k]: dp[m | 1 << k][k] = v
    return min(dp[full - 1][j] + D[j][N - 1] for j in range(N - 1))
 
if __name__ == "__main__":
    g = greedy()
    results = {
        "5 貪婪":          g,
        "1 改良法(2-opt)": two_opt(g),
        "2 爬山":          hill_climb(),
        "3 模擬退火":      simulated_annealing(),
        "4 梯度下降":      elastic_net(),
    }
    opt = held_karp() if N <= 15 else None
    print(f"N={N}, seed={SEED}" + (f", 最佳解={opt:.2f}" if opt else ""))
    for name, t in results.items():
        gap = f"  (+{(L(t)/opt-1)*100:.1f}%)" if opt else ""
        print(f"{name:<14} 長度={L(t):8.2f}{gap}  路徑={t}")
