#!/python3
# -*- coding: utf-8 -*-
"""第 19～20 章可编程习题。"""
from collections import deque
import heapq

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 19 章
def p1901(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    deg = [0] * (n + 1)
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        deg[u] += 1
        deg[v] += 1
    best = max(range(1, n + 1), key=lambda i: (deg[i], -i))
    return "\n".join(str(deg[i]) for i in range(1, n + 1)) + "\n" + str(best)


add(id="p-19-01", chapter=19, label="习题 19-1", title="每个点的度数",
    difficulty=1,
    statement_md="读入一张无向图，输出每个点的度数，以及度数最大的点的编号（并列时取编号小的）。\n\n本题是第 19 章习题 1。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示一条无向边。",
    output_md="前 n 行，第 i 行是点 i 的度数；最后一行一个整数，表示度数最大的点（并列取小编号）。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="每读一条边给两个端点各加一；最后遍历找最大值，同值取小编号。",
    tags=["图", "度数"],
    cases=["5 4\n1 2\n1 3\n2 4\n3 5", "3 0", "4 4\n1 2\n2 3\n3 4\n4 1",
           "5 6\n1 2\n1 2\n1 3\n2 3\n3 4\n4 5"],
    solve=p1901)

def p1902(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        a, b = find(u), find(v)
        if a == b:
            return "Yes"
        par[a] = b
    return "No"


add(id="p-19-02", chapter=19, label="习题 19-2", title="判断无向图有没有环",
    difficulty=2,
    statement_md="判断一张无向图里有没有环。可以先用 DFS 找「回到祖先」的边，也可以用并查集：加边时如果两个端点已经同根，就说明出现了环。\n\n本题是第 19 章习题 2。自环和重边都算环。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v。",
    output_md="有环输出 `Yes`，否则输出 `No`。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="并查集：每条边加入前检查两个端点是否已连通，已连通就成环。",
    tags=["图", "并查集"],
    cases=["3 2\n1 2\n2 3", "3 3\n1 2\n2 3\n1 3", "2 2\n1 2\n1 2", "3 1\n1 1",
           "5 4\n1 2\n2 3\n4 5\n3 4"],
    solve=p1902)

def p1903(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v)
        adj[v].append(u)
    col = [-1] * (n + 1)
    for s in range(1, n + 1):
        if col[s] != -1:
            continue
        col[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if col[v] == -1:
                    col[v] = col[u] ^ 1
                    q.append(v)
                elif col[v] == col[u]:
                    return "No"
    c0 = sum(1 for i in range(1, n + 1) if col[i] == 0)
    c1 = n - c0
    return "\n".join(["Yes"] + [str(col[i]) for i in range(1, n + 1)] + ["%d %d" % (c0, c1)])


add(id="p-19-03", chapter=19, label="习题 19-3", title="二分图分组",
    difficulty=2,
    statement_md="在二分图判定的基础上再进一步：如果不能分两组，输出 `No`；如果能，输出每个点分在哪一组（0 或 1），以及两组的点数。\n\n本题是第 19 章习题 3。为了让答案唯一：从编号最小的未染色点开始染色，把它染成 0，它的邻点染成 1。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v。",
    output_md="若能分成两组：第一行 `Yes`，接下来 n 行每行一个 0 或 1，最后一行两个整数表示两组的人数；不能则只输出 `No`。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="BFS/DFS 染色，邻点颜色取反；遇到已染色且颜色相同的邻点就失败。",
    tags=["二分图", "BFS"],
    cases=["4 2\n1 2\n3 4", "3 3\n1 2\n2 3\n1 3", "5 4\n1 2\n2 3\n3 4\n4 5",
           "2 1\n1 2"],
    solve=p1903)

def p1904(t):
    d = t.split()
    p = 0
    n, m, s = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
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
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return " ".join(str(dist[i]) for i in range(1, n + 1))


add(id="p-19-04", chapter=19, label="习题 19-4", title="无权图最短路",
    difficulty=2,
    statement_md="读入 n 个点、m 条边和起点 s，输出 s 到每个点的最少边数，到不了输出 -1。要求 O(n+m)。\n\n本题是第 19 章习题 4。",
    input_md="第一行三个整数 n、m、s（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v。",
    output_md="一行 n 个整数，依次表示 s 到点 1..n 的最少边数；到不了输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="BFS 从 s 出发，第一次访问即最短；最后按编号输出 1..n 的距离。",
    tags=["BFS", "最短路"],
    cases=["5 4 1\n1 2\n1 3\n2 4\n3 5", "3 0 2", "4 4 1\n1 2\n2 3\n3 4\n4 1",
           "6 4 2\n1 2\n2 3\n4 5\n5 6"],
    solve=p1904)

def p1906(t):
    d = t.split()
    p = 0
    n, m, k = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
    edges = []
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        edges.append((u, v))
        adj[u].append(v)
        adj[v].append(u)
    dels = [int(d[p + i]) for i in range(k)]
    deleted = [False] * (n + 1)
    for x in dels:
        deleted[x] = True
    par = list(range(n + 1))
    active = [not deleted[i] for i in range(n + 1)]

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    comp = sum(1 for i in range(1, n + 1) if active[i])
    for u, v in edges:
        if active[u] and active[v]:
            a, b = find(u), find(v)
            if a != b:
                par[a] = b
                comp -= 1
    ans = []
    for x in reversed(dels):
        ans.append(comp)
        active[x] = True
        comp += 1
        for v in adj[x]:
            if active[v]:
                a, b = find(x), find(v)
                if a != b:
                    par[a] = b
                    comp -= 1
    # ans[i] 是删掉第 i 个点之后的状态（反向加入前记录）
    return "\n".join(str(ans[i]) for i in range(k - 1, -1, -1))


add(id="p-19-06", chapter=19, label="习题 19-6", title="倒着加点：删点后的连通块",
    difficulty=3,
    statement_md="一张无向图，每次删掉一个点（以及它连的所有边），问删掉后图分成几个连通块。要求对 m 次删除，总复杂度不超过 O((n+m) log n)。提示：反过来想，把「删点」看成「倒着加点」，用并查集。\n\n本题是第 19 章习题 6。注意孤立点各算一个连通块；点被删光时连通块数为 0。",
    input_md="第一行三个整数 n、m、k（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ k ≤ n）。\n接下来 m 行，每行两个整数 u、v。\n最后一行 k 个整数，依次表示要删掉的点（互不相同）。",
    output_md="共 k 行，第 i 行表示删掉第 i 个点之后图中的连通块个数。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ k ≤ n。",
    hint_md="先按「最终还活着的点」建图计数，然后倒序把点加回来：每加一个点先 +1，再与已激活的邻居合并、每成功合并一次 -1。",
    tags=["并查集", "离线"],
    cases=["5 4 2\n1 2\n2 3\n3 4\n4 5\n2 4", "3 2 3\n1 2\n2 3\n1 2 3",
           "4 2 1\n1 2\n3 4\n1", "6 5 2\n1 2\n2 3\n4 5\n5 6\n3 4\n2 5"],
    solve=p1906)

# ================================================================ 第 20 章
def p2001(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
    INF = 10 ** 30
    dist = [INF] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        dd, u = heapq.heappop(pq)
        if dd != dist[u]:
            continue
        for v, w in adj[u]:
            nd = dd + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return str(dist[n]) if dist[n] < INF else "-1"


add(id="p-20-01", chapter=20, label="习题 20-1", title="Dijkstra 求 1 到 n",
    difficulty=2,
    statement_md="给一张有向图，每条边有权，求从 1 号点到 n 号点的最短距离，走不到输出 -1。要求用堆优化 Dijkstra，n ≤ 10^5。\n\n本题是第 20 章习题 1。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9），表示一条 u→v 的有向边。",
    output_md="一个整数，表示最短距离；走不到输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ w ≤ 10^9。",
    hint_md="堆里存 `(距离, 点)`，弹出时若距离已过期就跳过；距离用 `long long`。",
    tags=["Dijkstra"],
    cases=["5 6 1 5\n1 2 4\n1 3 2\n3 2 1\n2 4 5\n3 4 8\n4 5 1", "2 0",
           "3 3 1 3\n1 2 1\n2 3 1\n1 3 5", "4 3 1 4\n1 2 1\n2 3 1\n3 4 1",
           "3 2 1 2\n1 2 2\n1 3 1"],
    solve=p2001)

def p2002(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
    INF = 10 ** 30
    dist = [INF] * (n + 1)
    pre = [0] * (n + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        dd, u = heapq.heappop(pq)
        if dd != dist[u]:
            continue
        for v, w in adj[u]:
            nd = dd + w
            if nd < dist[v]:
                dist[v] = nd
                pre[v] = u
                heapq.heappush(pq, (nd, v))
    if dist[n] >= INF:
        return "-1"
    path = []
    x = n
    while x:
        path.append(str(x))
        if x == 1:
            break
        x = pre[x]
    path.reverse()
    return str(dist[n]) + "\n" + " ".join(path)


add(id="p-20-02", chapter=20, label="习题 20-2", title="Dijkstra 输出路径",
    difficulty=2,
    statement_md="在第 20 章习题 1 的基础上，输出从 1 到 n 的一条最短路径。如果最短路不唯一，输出任意一条即可。\n\n本题是第 20 章习题 2。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9）。",
    output_md="第一行一个整数，表示最短距离；第二行为路径上依次经过的点，用空格隔开。走不到时只输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="松弛成功时记 `pre[v] = u`，最后从 n 沿着 pre 倒退回 1，再反转输出。",
    tags=["Dijkstra", "路径"],
    cases=["5 6 1 5\n1 2 4\n1 3 2\n3 2 1\n2 4 5\n3 4 8\n4 5 1", "2 0",
           "3 3 1 3\n1 2 1\n2 3 1\n1 3 5"],
    solve=p2002)

def p2003(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    edges = []
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        edges.append((u, v, w))
    INF = 10 ** 30
    dist = [INF] * (n + 1)
    dist[1] = 0
    for it in range(n):
        changed = False
        for u, v, w in edges:
            if dist[u] < INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
                if it == n - 1:
                    return "Yes"
        if not changed:
            break
    return "No"


add(id="p-20-03", chapter=20, label="习题 20-3", title="负环判定",
    difficulty=2,
    statement_md="判断一张有向图里有没有从起点 1 能到达的负环。如果有，输出 `Yes`；否则输出 `No`。用 Bellman-Ford 实现，并说明为什么扫到第 n 轮还能更新就说明有负环。\n\n本题是第 20 章习题 3。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 1000，0 ≤ m ≤ 5000）。\n接下来 m 行，每行三个整数 u、v、w（-10^9 ≤ w ≤ 10^9）。",
    output_md="`Yes` 或 `No`。",
    constraints_md="1 ≤ n ≤ 1000，0 ≤ m ≤ 5000。",
    hint_md="从 1 出发松弛 n 轮；第 n 轮仍能松弛说明存在从 1 可达的负环（只更新可达的点）。",
    tags=["Bellman-Ford", "负环"],
    cases=["3 3\n1 2 1\n2 3 -2\n3 2 -1", "3 2\n1 2 1\n2 3 1", "2 1\n2 1 -5",
           "4 4\n1 2 1\n2 3 1\n3 4 1\n4 2 -5", "3 3\n1 2 1\n2 2 -1\n2 3 1"],
    solve=p2003)

def p2004(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
    INF = 10 ** 18
    dist = [INF] * (n + 1)
    dist[1] = 0
    dq = deque([1])
    inq = [False] * (n + 1)
    inq[1] = True
    while dq:
        u = dq.popleft()
        inq[u] = False
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not inq[v]:
                    inq[v] = True
                    if w == 0:
                        dq.appendleft(v)
                    else:
                        dq.append(v)
    return str(dist[n]) if dist[n] < INF else "-1"


add(id="p-20-04", chapter=20, label="习题 20-4", title="0-1 BFS",
    difficulty=2,
    statement_md="一张图里每条边的权不是 0 就是 1，求 1 到 n 的最短距离。要求 O(n+m)，不能用堆。\n\n本题是第 20 章习题 4：用双端队列，权为 0 的边把新点放队首，权为 1 的放队尾。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（w 为 0 或 1）。",
    output_md="一个整数，表示最短距离；走不到输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="0-1 BFS 本质是 Dijkstra 的简化：0 边入队首、1 边入队尾，每个点可能入队多次，需判距离。",
    tags=["0-1 BFS"],
    cases=["5 5 1 5\n1 2 1\n1 3 0\n3 2 0\n2 4 1\n4 5 0", "2 0",
           "3 2\n1 2 0\n2 3 0", "4 4\n1 2 1\n2 3 1\n3 4 1\n1 4 0"],
    solve=p2004)

def p2005(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = 10 ** 18
    dist = [INF] * (n + 1)
    cnt = [0] * (n + 1)
    dist[1] = 0
    cnt[1] = 1
    pq = [(0, 1)]
    MOD = 1000000007
    while pq:
        dd, u = heapq.heappop(pq)
        if dd != dist[u]:
            continue
        for v, w in adj[u]:
            nd = dd + w
            if nd < dist[v]:
                dist[v] = nd
                cnt[v] = cnt[u]
                heapq.heappush(pq, (nd, v))
            elif nd == dist[v]:
                cnt[v] = (cnt[v] + cnt[u]) % MOD
    return str(cnt[n] % MOD) if dist[n] < INF else "0"


add(id="p-20-05", chapter=20, label="习题 20-5", title="最短路计数",
    difficulty=3,
    statement_md="给一张非负权无向图，求 1 到 n 的最短路径条数，答案对 10^9+7 取余。请说明为什么不能在 Floyd 上直接做计数。\n\n本题是第 20 章习题 5。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（0 ≤ w ≤ 10^9）。",
    output_md="一个整数，表示最短路条数对 10^9+7 取余；走不到输出 0。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="Dijkstra 松弛：更短就覆盖方案数，相等就累加。注意 0 权边会让同一层的计数有先后，必须等最短路确定后再累加。",
    tags=["最短路计数", "Dijkstra"],
    cases=["4 4\n1 2 1\n1 3 1\n2 4 1\n3 4 1", "3 2\n1 2 1\n2 3 1", "2 0",
           "5 6\n1 2 1\n1 3 1\n2 4 2\n3 4 2\n4 5 3\n2 5 4"],
    solve=p2005)
