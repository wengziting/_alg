import heapq
from collections import deque

MAP = [
    "N....#......",
    ".###.#.####.",
    ".#...#.#....",
    ".#.###.#.###",
    ".#.....#...P",
    ".#######.##.",
    "............",
]
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def find(m, ch):
    for r, row in enumerate(m):
        if ch in row:
            return r, row.index(ch)


def h(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def passable(m, r, c):
    return 0 <= r < len(m) and 0 <= c < len(m[0]) and m[r][c] != "#"


def astar(m, start, goal):
    open_heap = [(h(start, goal), 0, start)]   # (f, g, 位置)
    g_cost, parent, expanded = {start: 0}, {start: None}, 0
    closed = set()
    while open_heap:
        _, g, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)
        expanded += 1
        if cur == goal:
            path = []
            while cur:
                path.append(cur)
                cur = parent[cur]
            return path[::-1], expanded
        for dr, dc in DIRS:
            nxt = (cur[0] + dr, cur[1] + dc)
            if not passable(m, *nxt):
                continue
            ng = g + 1
            if ng < g_cost.get(nxt, 1e9):
                g_cost[nxt], parent[nxt] = ng, cur
                heapq.heappush(open_heap, (ng + h(nxt, goal), ng, nxt))
    return None, expanded


def bfs_expanded(m, start, goal):
    q, seen, n = deque([start]), {start}, 0
    while q:
        cur = q.popleft(); n += 1
        if cur == goal:
            return n
        for dr, dc in DIRS:
            nxt = (cur[0] + dr, cur[1] + dc)
            if passable(m, *nxt) and nxt not in seen:
                seen.add(nxt); q.append(nxt)


def render(m, path, npc, player):
    grid = [list(row.replace("N", ".").replace("P", ".")) for row in m]
    for r, c in (path or [])[1:-1]:
        grid[r][c] = "*"
    grid[npc[0]][npc[1]], grid[player[0]][player[1]] = "N", "P"
    return "\n".join("".join(row) for row in grid)


def chase_demo(m):
    npc, player = find(m, "N"), find(m, "P")
    flee = [(4, 10), (4, 9), (4, 8)]
    print("\n--- 追逐模擬:NPC 每回合重新規劃路徑 ---")
    for t in range(1, 60):
        if t <= len(flee):
            player = flee[t - 1]             # 玩家移動
        path, _ = astar(m, npc, player)      # 玩家位置變了,重新規劃
        if len(path) == 1:
            print(f"第 {t} 回合:NPC 抓到玩家!")
            return
        npc = path[1]                        # NPC 只走一步
        if t <= 5 or len(path) <= 3:
            print(f"第 {t} 回合:玩家 {player}, NPC {npc}, 剩 {len(path) - 2} 步")
        elif t == 6:
            print("   ...")


if __name__ == "__main__":
    npc, player = find(MAP, "N"), find(MAP, "P")
    path, exp = astar(MAP, npc, player)
    print(render(MAP, path, npc, player))
    print(f"\nA* 路徑長度 {len(path) - 1} 步,展開 {exp} 個節點")
    print(f"BFS 同樣問題需展開 {bfs_expanded(MAP, npc, player)} 個節點")
    chase_demo(MAP)
