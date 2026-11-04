from collections import deque

NAMES = ["農夫", "狼", "羊", "甘藍菜"]
START, GOAL = (0, 0, 0, 0), (1, 1, 1, 1)


def is_safe(s):
    f, w, g, c = s
    if w == g and f != w:   
        return False
    if g == c and f != g:  
        return False
    return True


def neighbors(s):
    f = s[0]
    for i in range(4):
        if i != 0 and s[i] != f:
            continue
        t = list(s)
        t[0] = 1 - f
        if i != 0:
            t[i] = 1 - f
        t = tuple(t)
        if is_safe(t):
            yield i, t


def bfs():
    queue = deque([START])
    parent = {START: None}             
    while queue:
        cur = queue.popleft()
        if cur == GOAL:
            break
        for who, nxt in neighbors(cur):
            if nxt not in parent:
                parent[nxt] = (cur, who)
                queue.append(nxt)
    if GOAL not in parent:
        return None
    steps, s = [], GOAL
    while parent[s]:
        prev, who = parent[s]
        steps.append((prev, who, s))
        s = prev
    return steps[::-1]


def banks(s):
    left = [NAMES[i] for i in range(4) if s[i] == 0]
    right = [NAMES[i] for i in range(4) if s[i] == 1]
    return f"左岸:{'、'.join(left) or '無':<14} 右岸:{'、'.join(right) or '無'}"


if __name__ == "__main__":
    steps = bfs()
    print(f"初始    {banks(START)}")
    for n, (prev, who, s) in enumerate(steps, 1):
        direction = "→ 過河" if prev[0] == 0 else "← 回來"
        cargo = "獨自" if who == 0 else f"帶著{NAMES[who]}"
        print(f"第{n}步  農夫{cargo}{direction}\n        {banks(s)}")
    print(f"\n最少 {len(steps)} 步")
