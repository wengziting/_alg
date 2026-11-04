MAZE = [
    "##########",
    "#S.#.....#",
    "#..#.###.#",
    "#.##...#.#",
    "#....#.#.#",
    "####.#.#.#",
    "#....#...#",
    "#.####.#.#",
    "#......#E#",
    "##########",
]
DIRS = [(-1, 0), (0, 1), (0, -1), (1, 0)]  # 上 右 左 下(順序會影響走出的路徑)


def find(maze, ch):
    for r, row in enumerate(maze):
        if ch in row:
            return r, row.index(ch)


def solve(maze):
    start, end = find(maze, "S"), find(maze, "E")
    rows, cols = len(maze), len(maze[0])
    visited, path = set(), []

    def dfs(r, c):
        visited.add((r, c))
        path.append((r, c))            
        if (r, c) == end:
            return True
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and maze[nr][nc] != "#" and (nr, nc) not in visited):
                if dfs(nr, nc):
                    return True
        path.pop()                    
        return False

    found = dfs(*start)
    return (path if found else None), visited


def shortest_len(maze):
    """用 BFS 算最短步數,只用來和 DFS 的結果對照。"""
    from collections import deque
    start, end = find(maze, "S"), find(maze, "E")
    dist, q = {start: 0}, deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            n = (r + dr, c + dc)
            if maze[n[0]][n[1]] != "#" and n not in dist:
                dist[n] = dist[(r, c)] + 1
                q.append(n)
    return dist[end]


def show(maze, path, visited):
    grid = [list(row) for row in maze]
    for r, c in visited:
        if grid[r][c] == ".":
            grid[r][c] = "x"           
    for r, c in path[1:-1]:
        grid[r][c] = "*"                
    print("\n".join("".join(row) for row in grid))


if __name__ == "__main__":
    path, visited = solve(MAZE)
    if path:
        show(MAZE, path, visited)
        print(f"\n找到出口!路徑長度 {len(path) - 1} 步,共探索 {len(visited)} 格")
        print("(* = 路徑, x = 走過但回溯的死路)")
        print(f"對照:BFS 的最短路徑是 {shortest_len(MAZE)} 步 —— DFS 能找到出口,但不保證最短")
    else:
        print("迷宮無解")
