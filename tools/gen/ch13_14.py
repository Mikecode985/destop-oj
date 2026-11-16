#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 13～14 章可编程习题。"""
PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 13 章
def p1301(t):
    n = int(t.split()[0])
    col = [False] * n
    d1 = [False] * (2 * n)
    d2 = [False] * (2 * n)
    board = [-1] * n

    def dfs(r):
        if r == n:
            return True
        for c in range(n):
            if col[c] or d1[r + c] or d2[r - c + n]:
                continue
            col[c] = d1[r + c] = d2[r - c + n] = True
            board[r] = c
            if dfs(r + 1):
                return True
            col[c] = d1[r + c] = d2[r - c + n] = False
        return False

    if not dfs(0):
        return "No"
    return "\n".join("".join("Q" if board[r] == c else "." for c in range(n)) for r in range(n))


add(id="p-13-01", chapter=13, label="习题 13-1", title="n 皇后的第一个解",
    difficulty=2,
    statement_md="把例题 13-1 改成输出「第一个解」：找到一种摆法就立刻输出棋盘并结束。\n\n本题是第 13 章习题 1。输出搜索到的第一种摆法：从上到下逐行放皇后，每行从小到大尝试列号，因此得到的是字典序最小的解。",
    input_md="一个整数 n（1 ≤ n ≤ 10）。",
    output_md="共 n 行，每行 n 个字符：`Q` 表示皇后，`.` 表示空位；无解输出 `No`。",
    constraints_md="1 ≤ n ≤ 10。",
    hint_md="`dfs(r)` 放第 r 行，找到解就一路 `return true` 回去，不再继续搜索。",
    tags=["回溯", "n 皇后"],
    cases=["1", "4", "6", "8", "3"],
    solve=p1301)

def p1302(t):
    n = int(t.split()[0])
    out = []
    cur = []

    def dfs(open_, close):
        if len(cur) == 2 * n:
            out.append("".join(cur))
            return
        if open_ < n:
            cur.append("(")
            dfs(open_ + 1, close)
            cur.pop()
        if close < open_:
            cur.append(")")
            dfs(open_, close + 1)
            cur.pop()

    dfs(0, 0)
    return "\n".join(out)


add(id="p-13-02", chapter=13, label="习题 13-2", title="括号生成",
    difficulty=2,
    statement_md="给定 n 对括号，列出所有合法的括号序列。\n\n本题是第 13 章习题 2：说明回溯时用哪几个参数记录状态，什么样的分支必须剪掉。",
    input_md="一个整数 n（1 ≤ n ≤ 10）。",
    output_md="每行一个合法括号序列，按字典序升序输出（`(` 排在 `)` 前面）。",
    constraints_md="1 ≤ n ≤ 10。",
    hint_md="`dfs(open, close)`：还能放左括号就放；右括号数量小于左括号时才放右括号。",
    tags=["回溯", "括号"],
    cases=["1", "2", "3", "4"],
    solve=p1302)

def p1303(t):
    d = t.split()
    n = int(d[0])
    a = sorted(map(int, d[1:1 + n]))
    out = []
    cur = []

    def dfs(start):
        out.append("{" + ",".join(map(str, cur)) + "}")
        for i in range(start, n):
            if i > start and a[i] == a[i - 1]:
                continue
            cur.append(a[i])
            dfs(i + 1)
            cur.pop()

    dfs(0)
    return "\n".join(out)


add(id="p-13-03", chapter=13, label="习题 13-3", title="子集 II（含重复元素）",
    difficulty=2,
    statement_md="给定一个可能含重复元素的数组，列出所有不重复的子集。\n\n本题是第 13 章习题 3：模仿例题 13-2，写出「排序 + 同层跳过重复值」的那一行，并解释 `i > start` 的作用。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 15）。\n第二行 n 个整数（1 ≤ a[i] ≤ 100）。",
    output_md="每行一个子集，写成 `{}` 或 `{1,2}` 的形式，元素升序；按 DFS 顺序（先不含当前元素、再含）输出，且相同子集只出现一次。",
    constraints_md="1 ≤ n ≤ 15。",
    hint_md="先排序；`dfs(start)` 每层从 start 枚举，`i > start && a[i]==a[i-1]` 就跳过，避免同一层选到相同的值。",
    tags=["回溯", "子集"],
    cases=["3\n1 2 2", "1\n0", "2\n1 2", "3\n2 2 2", "4\n1 1 2 2"],
    solve=p1303)

def p1304(t):
    lines = t.strip().splitlines()
    n, m = map(int, lines[0].split())
    g = [list(lines[i + 1].strip()) for i in range(n)]
    sx = sy = ex = ey = -1
    for i in range(n):
        for j in range(m):
            if g[i][j] == "S":
                sx, sy = i, j
            elif g[i][j] == "E":
                ex, ey = i, j
    vis = [[False] * m for _ in range(n)]
    cnt = 0

    def dfs(x, y):
        nonlocal cnt
        if x == ex and y == ey:
            cnt += 1
            return
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not vis[nx][ny] and g[nx][ny] != "#":
                vis[nx][ny] = True
                dfs(nx, ny)
                vis[nx][ny] = False

    vis[sx][sy] = True
    dfs(sx, sy)
    return str(cnt)


add(id="p-13-04", chapter=13, label="习题 13-4", title="迷宫方案数",
    difficulty=3,
    statement_md="在一个 n×m 的网格迷宫里，从 S 走到 E，每格最多经过一次，问一共有多少条路径。\n\n本题是第 13 章习题 4：为什么必须「走过就标记、回溯就撤销」？",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 6）。\n接下来 n 行，每行 m 个字符：`.` 空地、`#` 墙、`S` 起点、`E` 终点。",
    output_md="一个整数，表示从 S 到 E 且不重复经过格子的路径条数。",
    constraints_md="1 ≤ n, m ≤ 6。",
    hint_md="DFS 时进入格子先置 `vis=1`，四个方向递归，返回时撤销；到 E 就计数并返回。",
    tags=["DFS", "回溯"],
    cases=["3 3\nS..\n.#.\n..E", "2 2\nSE\n..", "3 3\nS#E\n###\n...",
           "4 4\nS...\n....\n....\n...E", "1 5\nS...E"],
    solve=p1304)

def p1305(t):
    d = t.split()
    p = 0
    n, W = int(d[p]), int(d[p + 1]); p += 2
    items = []
    for _ in range(n):
        w, v = int(d[p]), int(d[p + 1]); p += 2
        items.append((w, v))
    items.sort(key=lambda x: -(x[1] / x[0]))
    best = 0

    def dfs(i, cap, val):
        nonlocal best
        if val > best:
            best = val
        if i == n:
            return
        # 上界：剩余容量按性价比从高到低装满
        bound = val
        rem = cap
        for j in range(i, n):
            if items[j][0] <= rem:
                rem -= items[j][0]
                bound += items[j][1]
            else:
                bound += items[j][1] * rem / items[j][0]
                break
        if bound <= best:
            return
        if items[i][0] <= cap:
            dfs(i + 1, cap - items[i][0], val + items[i][1])
        dfs(i + 1, cap, val)

    dfs(0, W, 0)
    return str(best)


add(id="p-13-05", chapter=13, label="习题 13-5", title="背包最优性剪枝",
    difficulty=3,
    statement_md="给一个容量为 W 的背包和 n 个物品，求能装下的最大价值。请设计一个最优性剪枝：按性价比排序后，当前价值加上「剩余容量全装最高性价比物品」的上界，如果上界不超过已有最优就回头。\n\n本题是第 13 章习题 5。",
    input_md="第一行两个整数 n、W（1 ≤ n ≤ 20，1 ≤ W ≤ 10^9）。\n接下来 n 行，每行两个整数 w[i]、v[i]（1 ≤ w[i] ≤ 10^9，1 ≤ v[i] ≤ 10^9）。",
    output_md="一个整数，表示最大总价值。",
    constraints_md="1 ≤ n ≤ 20，1 ≤ W ≤ 10^9。",
    hint_md="按 `v/w` 降序排序，DFS 每件选或不选；用分数背包的值作上界，`bound <= best` 时剪枝。",
    tags=["回溯", "剪枝", "背包"],
    cases=["3 10\n5 10\n4 40\n6 30", "1 5\n6 100", "3 5\n1 1\n2 2\n3 3",
           "4 10\n2 3\n2 3\n2 3\n2 3", "5 15\n10 20\n5 30\n3 9\n7 14\n2 5"],
    solve=p1305)

# ================================================================ 第 14 章
def p1401(t):
    tokens = t.split()
    st = []
    for tk in tokens:
        if tk in "+-*/":
            b = st.pop(); a = st.pop()
            if tk == "+":
                st.append(a + b)
            elif tk == "-":
                st.append(a - b)
            elif tk == "*":
                st.append(a * b)
            else:
                q = abs(a) // abs(b)
                st.append(q if (a >= 0) == (b >= 0) else -q)
        else:
            st.append(int(tk))
    return str(st[0])


add(id="p-14-01", chapter=14, label="习题 14-1", title="逆波兰表达式求值",
    difficulty=2,
    statement_md="给一个后缀表达式（如 `3 4 2 * +`），用栈求值。数字入栈；遇到运算符，弹出两个数、按「先弹出的在右」的顺序算，再把结果压回去。\n\n本题是第 14 章习题 1。除法向零取整。",
    input_md="一行后缀表达式，元素之间用空格隔开：整数（-10^9 ≤ x ≤ 10^9）或 `+`、`-`、`*`、`/`。",
    output_md="一个整数，表示表达式的值。",
    constraints_md="表达式长度不超过 10^5 个元素，保证合法且不会除以 0，中间结果在 64 位范围内。",
    hint_md="`st.top()` 先弹出的是右操作数：`b = st.top(); st.pop(); a = st.top();`。",
    tags=["栈"],
    cases=["3 4 2 * +", "5 1 2 + 4 * + 3 -", "7", "-10 3 /", "2 3 -"],
    solve=p1401)

def p1402(t):
    s = t.strip()
    depth = 0
    best = 0
    for ch in s:
        if ch == "(":
            depth += 1
            best = max(best, depth)
        elif ch == ")":
            depth -= 1
    return str(best)


add(id="p-14-02", chapter=14, label="习题 14-2", title="括号深度",
    difficulty=1,
    statement_md="给一串合法括号，求它的最大嵌套深度（如 `(()(()))` 的深度是 3）。这题需要真的用栈吗？还是用一个计数器就够了？请说明理由。\n\n本题是第 14 章习题 2。",
    input_md="一行一个合法括号串，长度不超过 10^5。",
    output_md="一个整数，表示最大嵌套深度。",
    constraints_md="1 ≤ 长度 ≤ 10^5，保证括号合法。",
    hint_md="只需要一个计数器：遇 `(` 加一、遇 `)` 减一，过程中记录最大值。",
    tags=["栈", "括号"],
    cases=["(()(()))", "()", "((()))", "()()()", "((())(()))"],
    solve=p1402)

def p1403(t):
    d = t.split()
    n = int(d[0])
    h = list(map(int, d[1:1 + n]))
    st = []
    best = 0
    for i in range(n + 1):
        cur = h[i] if i < n else 0
        while st and h[st[-1]] > cur:
            hh = h[st.pop()]
            left = st[-1] if st else -1
            best = max(best, hh * (i - left - 1))
        st.append(i)
    return str(best)


add(id="p-14-03", chapter=14, label="习题 14-3", title="柱状图最大矩形",
    difficulty=3,
    statement_md="给 n 根相邻柱子的高度（宽度都是 1），求能框出的最大矩形面积。请用单调栈，对每根柱子找「左边第一个更矮」和「右边第一个更矮」的位置。\n\n本题是第 14 章习题 3。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 h[i]（1 ≤ h[i] ≤ 10^9）。",
    output_md="一个整数，表示最大矩形面积。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ h[i] ≤ 10^9，答案可能超过 `int`。",
    hint_md="维护高度单调递增的栈；弹出时左右边界都确定了，面积是 `h * (右-左-1)`；末尾补一个高度 0 的哨兵。",
    tags=["单调栈"],
    cases=["6\n2 1 5 6 2 3", "1\n5", "5\n1 2 3 4 5", "5\n5 4 3 2 1",
           "7\n6 2 5 4 5 1 6"],
    solve=p1403)

def p1404(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    dq = []
    out = []
    for i in range(n):
        while dq and a[dq[-1]] >= a[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.pop(0)
        if i >= k - 1:
            out.append(str(a[dq[0]]))
    return " ".join(out)


add(id="p-14-04", chapter=14, label="习题 14-4", title="滑动窗口最小值",
    difficulty=2,
    statement_md="把例题 14-3 改成求每个窗口的最小值。窗口长度为 k，从数组最左滑到最右，每次输出窗口内的最小值。\n\n本题是第 14 章习题 4：需要改哪几行？单调队列里的递减规矩应该变成什么？",
    input_md="第一行两个整数 n、k（1 ≤ k ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一行 n-k+1 个整数，依次表示每个窗口的最小值，用空格隔开。",
    constraints_md="1 ≤ k ≤ n ≤ 10^5。",
    hint_md="队列里维护单调递增：新元素比队尾小就弹出队尾，队首超出窗口就弹出队首，队首即最小值。",
    tags=["单调队列"],
    cases=["8 3\n1 3 -1 -3 5 3 6 7", "1 1\n5", "5 5\n1 2 3 4 5", "4 2\n4 3 2 1",
           "6 3\n3 3 3 3 3 3"],
    solve=p1404)
