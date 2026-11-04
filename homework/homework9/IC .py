import heapq
import itertools
from collections import deque

ROWS, COLS = 10, 14
OBSTACLES = {(r, c) for r in range(3, 7) for c in range(4, 7)} | \
            {(r, c) for r in range(2, 6) for c in range(8, 10)}
NETS = {"A": ((1, 1), (1, 12)),
        "B": ((8, 1), (8, 12)),
        "C": ((4, 0), (5, 13))}
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def inside(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def lee(blocked, src, dst):
    dist, q, expanded = {src: 0}, deque([src]), 0
    while q:                                 
        cur = q.popleft(); expanded += 1
        if cur == dst:
            break
        for dr, dc in DIRS:
            n = (cur[0] + dr, cur[1] + dc)
            if inside(*n) and n not in blocked and n not in dist:
                dist[n] = dist[cur] + 1
                q.append(n)
    if dst not in dist:
        return None, expanded
    path, cur = [dst], dst                   
    while cur != src:
        for dr, dc in DIRS:
            n = (cur[0] + dr, cur[1] + dc)
            if dist.get(n) == dist[cur] - 1:
                cur = n; path.append(n); break
    return path[::-1], expanded


def astar(blocked, src, dst):
    h = lambda p: abs(p[0] - dst[0]) + abs(p[1] - dst[1])
    heap, g, parent, closed, expanded = [(h(src), 0, src)], {src: 0}, {src: None}, set(), 0
    while heap:
        _, gc, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur); expanded += 1
        if cur == dst:
            path = []
            while cur:
                path.append(cur); cur = parent[cur]
            return path[::-1], expanded
        for dr, dc in DIRS:
            n = (cur[0] + dr, cur[1] + dc)
            if inside(*n) and n not in blocked and gc + 1 < g.get(n, 1e9):
                g[n], parent[n] = gc + 1, cur
                heapq.heappush(heap, (gc + 1 + h(n), gc + 1, n))
    return None, expanded


def route_all(router, order):
    all_pins = {p for pair in NETS.values() for p in pair}
    wires, used, total_expanded = {}, set(), 0
    for name in order:
        src, dst = NETS[name]
        blocked = OBSTACLES | used | (all_pins - {src, dst})
        path, exp = router(blocked, src, dst)
        total_expanded += exp
        if path is None:
            return None, total_expanded
        wires[name] = path
        used |= set(path)
    return wires, total_expanded


def route_with_retry(router):
    for order in itertools.permutations(NETS):   # 第一個排列就是預設順序
        wires, exp = route_all(router, order)
        if wires:
            return order, wires, exp
    return None, None, 0


def render(wires):
    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    for r, c in OBSTACLES:
        grid[r][c] = "#"
    for name, path in wires.items():
        for r, c in path[1:-1]:
            grid[r][c] = name.lower()
        for r, c in (path[0], path[-1]):
            grid[r][c] = name
    return "\n".join(" ".join(row) for row in grid)


if __name__ == "__main__":
    for title, router in (("Lee (BFS 波前)", lee), ("A* 繞線器", astar)):
        order, wires, exp = route_with_retry(router)
        length = sum(len(p) - 1 for p in wires.values())
        print(f"=== {title} ===  net 順序 {order},總線長 {length},展開節點 {exp}")
        print(render(wires), "\n")
    print("# = 障礙(巨集), 大寫 = pin, 小寫 = 導線")
