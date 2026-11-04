def solve(n=8):
    solutions = []
    cols, diag1, diag2 = set(), set(), set()
    board = []                            

    def dfs(r):
        if r == n:
            solutions.append(board[:])
            return
        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue                   
            cols.add(c); diag1.add(r - c); diag2.add(r + c); board.append(c)
            dfs(r + 1)
            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c); board.pop()

    dfs(0)
    return solutions


def show(sol):
    n = len(sol)
    for c in sol:
        print(" ".join("Q" if i == c else "." for i in range(n)))


if __name__ == "__main__":
    sols = solve(8)
    print(f"八皇后共有 {len(sols)} 組解,第一組:{sols[0]}\n")
    show(sols[0])
    print("\n其他 N 的解數:", {n: len(solve(n)) for n in range(4, 9)})

