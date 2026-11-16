#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 11～12 章可编程习题。"""
from collections import deque
from itertools import permutations

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 11 章
def p1101(t):
    lines = t.strip().splitlines()
    n, m = map(int, lines[0].split())
    g = [list(lines[i + 1].strip()) for i in range(n)]
    cnt = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] != "1":
                continue
            cnt += 1
            g[i][j] = "0"
            st = [(i, j)]
            while st:
                x, y = st.pop()
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == "1":
                            g[nx][ny] = "0"
                            st.append((nx, ny))
    return str(cnt)


add(id="p-11-01", chapter=11, label="习题 11-1", title="八连通块计数",
    difficulty=1,
    statement_md="把例题 11-2 的四个方向改成八个方向（上下左右加四个斜角），重做连通块计数：地图中 1 表示草地，0 表示空地，求草地分成多少块。\n\n本题是第 11 章习题 1。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行 m 个字符（0 或 1）。",
    output_md="一个整数，表示八连通草地块的个数。",
    constraints_md="1 ≤ n, m ≤ 1000。",
    hint_md="只需要把 `dx/dy` 从 4 个方向换成 8 个方向，其余逻辑不变；格子多时用显式栈。",
    tags=["DFS", "连通块"],
    cases=["3 3\n101\n010\n101", "2 2\n10\n01", "1 1\n1", "3 3\n000\n000\n000",
           "4 4\n1001\n0000\n0110\n1001"],
    solve=p1101)

def p1102(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    out = []
    cur = []

    def dfs(start):
        if len(cur) == k:
            out.append(" ".join(map(str, cur)))
            return
        for x in range(start, n + 1):
            if n - x + 1 < k - len(cur):
                break
            cur.append(x)
            dfs(x + 1)
            cur.pop()

    dfs(1)
    return "\n".join(out)


add(id="p-11-02", chapter=11, label="习题 11-2", title="组合数输出",
    difficulty=2,
    statement_md="给 n 和 k，按字典序输出从 1 到 n 中选 k 个数的所有组合。\n\n本题是第 11 章习题 2：在 DFS 里加一个 `start` 参数，规定下一个数必须比当前数大。",
    input_md="一行两个整数 n、k（1 ≤ k ≤ n ≤ 15）。",
    output_md="每行一个组合，k 个数用空格隔开，按字典序升序输出。",
    constraints_md="1 ≤ k ≤ n ≤ 15。",
    hint_md="`dfs(start)` 表示从 start 开始选；选满 k 个就输出，天然按字典序。",
    tags=["DFS", "组合"],
    cases=["4 2", "3 3", "5 1", "5 5", "5 3"],
    solve=p1102)

def p1103(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = int(d[p]) - 1, int(d[p + 1]) - 1; p += 2
        adj[u].append(v)
        adj[v].append(u)
    color = [0] * n

    def dfs(u):
        if u == n:
            return True
        used = set(color[v] for v in adj[u] if color[v])
        for c in range(1, 5):
            if c in used:
                continue
            color[u] = c
            if dfs(u + 1):
                return True
            color[u] = 0
        return False

    if dfs(0):
        return "\n".join(map(str, color))
    return "No"


add(id="p-11-03", chapter=11, label="习题 11-3", title="地图着色",
    difficulty=2,
    statement_md="给一张 n 个区域的地图，相邻区域不能同色，只有 4 种颜色（编号 1～4）。用 DFS 尝试给每个区域染色，输出一种可行方案，或者报告无解。\n\n本题是第 11 章习题 3。为了让答案唯一：按区域 1 到 n 的顺序，每个区域从小到大尝试颜色，输出搜索到的第一种方案（它的颜色序列字典序最小）。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 20，0 ≤ m ≤ 100）。\n接下来 m 行，每行两个整数 u、v，表示区域 u 与 v 相邻。",
    output_md="共 n 行，第 i 行一个整数，表示第 i 个区域的颜色（1～4）；无解输出 `No`。",
    constraints_md="1 ≤ n ≤ 20，0 ≤ m ≤ 100。",
    hint_md="`dfs(u)` 给第 u 个区域染色，枚举 1～4，跳过邻点已用的颜色；全部染完即成功。",
    tags=["DFS", "回溯"],
    cases=["3 3\n1 2\n2 3\n1 3", "2 1\n1 2", "4 0", "5 5\n1 2\n2 3\n3 4\n4 5\n5 1",
           "1 0"],
    solve=p1103)

def p1106(t):
    n = int(t.split()[0])
    primes = set()
    for x in range(2, 2 * n + 1):
        ok = True
        for i in range(2, int(x ** 0.5) + 1):
            if x % i == 0:
                ok = False
                break
        if ok:
            primes.add(x)
    out = []
    cur = []
    used = [False] * (n + 1)

    def dfs():
        if len(cur) == n:
            out.append(" ".join(map(str, cur)))
            return
        for x in range(1, n + 1):
            if used[x]:
                continue
            if cur and cur[-1] + x not in primes:
                continue
            used[x] = True
            cur.append(x)
            dfs()
            cur.pop()
            used[x] = False

    dfs()
    return "\n".join(out) if out else "No"


add(id="p-11-06", chapter=11, label="习题 11-6", title="相邻之和为质数的排列",
    difficulty=3,
    statement_md="求 1 到 n 的所有排列中，满足「相邻两个数之和都是质数」的排列。n ≤ 8，按字典序输出全部方案。\n\n本题是第 11 章习题 6：在 DFS 填下一个数时，提前判断与上一个数之和是否为质数，不满足就剪枝。",
    input_md="一个整数 n（1 ≤ n ≤ 8）。",
    output_md="每行一个满足条件的排列，n 个数用空格隔开，按字典序升序输出；没有方案输出 `No`。",
    constraints_md="1 ≤ n ≤ 8。",
    hint_md="先预处理 2～2n 内的质数；DFS 每层枚举没用过的数，检查与上一个数的和。",
    tags=["DFS", "剪枝"],
    cases=["1", "2", "3", "4", "5", "8"],
    solve=p1106)

# ================================================================ 第 12 章
def p1201(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    s, e = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * (n + 1)
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        if u == e:
            return str(dist[u])
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return str(dist[e])


add(id="p-12-01", chapter=12, label="习题 12-1", title="地铁最少坐几站",
    difficulty=1,
    statement_md="贵阳地铁有 n 个站，给出 m 对「相邻」关系。问从 s 站到 t 站最少坐几站；不连通输出 -1。\n\n本题是第 12 章习题 1。每坐一站算 1。",
    input_md="第一行四个整数 n、m、s、t（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 与 v 相邻。",
    output_md="一个整数，表示最少乘坐站数；不连通输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="BFS 第一次访问到 t 时的层数就是答案，因为 BFS 是按层扩展的。",
    tags=["BFS"],
    cases=["6 6 1 6\n1 2\n2 3\n3 4\n4 5\n5 6\n1 6", "3 1 1 3\n1 2", "2 0 1 2",
           "5 4 1 5\n1 2\n2 3\n3 4\n4 5"],
    solve=p1201)

def p1202(t):
    lines = t.strip().splitlines()
    n, m = map(int, lines[0].split())
    g = [list(lines[i + 1].strip()) for i in range(n)]
    dist = [[-1] * m for _ in range(n)]
    q = deque()
    for i in range(n):
        for j in range(m):
            if g[i][j] == "X":
                dist[i][j] = 0
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == "." and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    out = []
    for i in range(n):
        row = []
        for j in range(m):
            if g[i][j] == "#":
                row.append("#")
            elif g[i][j] == "X":
                row.append("0")
            else:
                row.append(str(dist[i][j]))
        out.append(" ".join(row))
    return "\n".join(out)


add(id="p-12-02", chapter=12, label="习题 12-2", title="古镇出口的距离",
    difficulty=2,
    statement_md="一个 n×m 的古镇地图上有若干个出口（用 X 标记），`.` 是巷道，`#` 是墙。求每个格子到最近出口的步数，到不了输出 -1。\n\n本题是第 12 章习题 2：应该用普通 BFS 还是多源 BFS？请说明理由。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行 m 个字符：`.` 巷道、`#` 墙、`X` 出口。",
    output_md="共 n 行，每行 m 个值，用空格隔开：巷道输出到最近出口的最少步数，到不了输出 -1；墙输出 `#`；出口本身输出 0。",
    constraints_md="1 ≤ n, m ≤ 1000，至少有一个出口。",
    hint_md="把所有出口先入队，做多源 BFS，一次就能算出每个格子到最近出口的距离。",
    tags=["BFS", "多源"],
    cases=["3 4\nX..X\n.#..\n....", "2 2\nX#\n#.", "1 3\nX..", "3 3\nX#X\n.#.\n...",
           "2 3\nX#X\n###"],
    solve=p1202)

def p1204(t):
    lines = t.strip().splitlines()
    start = "".join(lines[i].strip() for i in range(3))
    target = "123456780"
    if start == target:
        return "Yes"
    # 逆序对判可达（忽略 0）
    def parity(s):
        a = [int(c) for c in s if c != "0"]
        inv = 0
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                if a[i] > a[j]:
                    inv += 1
        return inv & 1

    return "Yes" if parity(start) == parity(target) else "No"


add(id="p-12-04", chapter=12, label="习题 12-4", title="八数码能否到达",
    difficulty=2,
    statement_md="一个 3×3 的九宫格，8 个滑块加一个空格（用 0 表示），每次只能把空格旁边的滑块滑进空格。给定初始局面，问能否走到目标局面（第一行 1 2 3，第二行 4 5 6，第三行 7 8 0）。\n\n本题是第 12 章习题 4：说明状态怎么表示、状态总数是多少、为什么必须去重。",
    input_md="三行，每行三个数字（0～8，互不重复），表示初始局面。",
    output_md="能到达输出 `Yes`，否则输出 `No`。",
    constraints_md="局面保证是 0～8 的一个排列。",
    hint_md="把 3×3 压成一个 9 位整数做状态，BFS 去重；n=8 时状态总数是 9! = 362880。也可以直接用逆序对奇偶性判断（空格左右移动不改变奇偶性）。",
    tags=["BFS", "状态空间"],
    cases=["123\n456\n780", "123\n456\n708", "123\n456\n870", "120\n453\n786",
           "876\n543\n210"],
    solve=p1204)


# ================================================================ 第 12 章（单词接龙）
def p1206(t):
    lines = [x.strip() for x in t.strip().splitlines() if x.strip() != ""]
    n = int(lines[0])
    words = lines[1:1 + n]
    start = lines[1 + n]
    target = lines[2 + n]
    if start == target:
        return "0"
    idx = {w: i for i, w in enumerate(words)}
    if start not in idx or target not in idx:
        return "-1"
    from collections import deque
    dist = [-1] * n
    dist[idx[start]] = 0
    q = deque([idx[start]])
    while q:
        u = q.popleft()
        w = words[u]
        for v, ww in enumerate(words):
            if dist[v] != -1 or len(ww) != len(w):
                continue
            diff = 0
            for a, b in zip(w, ww):
                if a != b:
                    diff += 1
            if diff == 1:
                dist[v] = dist[u] + 1
                if v == idx[target]:
                    return str(dist[v])
                q.append(v)
    return "-1"


add(id="p-12-06", chapter=12, label="习题 12-6", title="单词接龙",
    difficulty=2,
    statement_md="给一个词典、一个起始单词和一个目标单词。每一步只能改动一个字母，并且改完的单词必须出现在词典里。求从起始单词到目标单词最少要几步；走不到输出 -1。\n\n本题是第 12 章习题 6：把它建成一张图，每条边是「只差一个字母」，然后 BFS。想一想：为什么 BFS 第一次搜到目标就是最短？",
    input_md="第一行一个整数 n（1 ≤ n ≤ 500）。\n接下来 n 行，每行一个小写单词，表示词典（长度都相同）。\n接下来两行，分别是起始单词和目标单词（都保证在词典里）。",
    output_md="一个整数，表示最少步数（不含起始单词本身）；走不到输出 -1。",
    constraints_md="1 ≤ n ≤ 500，单词长度 ≤ 10，只含小写字母。",
    hint_md="两层循环枚举词典里任意两个单词，只差一个字母就建边；从起点 BFS，第一次访问目标时的距离即答案。",
    tags=["BFS", "字符串"],
    cases=["5\nhot\ndot\ndog\nlot\nlog\nhot\ndog", "2\nabc\nabd\nabc\nabd",
           "4\nabc\nabd\nabe\nxyz\nabc\nxyz", "1\nabc\nabc\nabc"],
    solve=p1206)