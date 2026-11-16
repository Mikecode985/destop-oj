#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 21～22 章可编程习题。"""
import heapq
from collections import deque

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


def dsu_find(par, x):
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x


# ================================================================ 第 21 章
def p2101(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    edges = []
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        edges.append((w, u, v))
    edges.sort()
    par = list(range(n + 1))
    total = used = 0
    for w, u, v in edges:
        a, b = dsu_find(par, u), dsu_find(par, v)
        if a != b:
            par[a] = b
            total += w
            used += 1
            if used == n - 1:
                break
    return str(total) if used == n - 1 else "-1"


add(id="p-21-01", chapter=21, label="习题 21-1", title="Kruskal 求最小生成树",
    difficulty=2,
    statement_md="给一张无向带权图，求最小生成树的总权值；图不连通输出 -1。要求用 Kruskal，n ≤ 10^5，m ≤ 2×10^5。\n\n本题是第 21 章习题 1。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9）。",
    output_md="一个整数，表示最小生成树总权值；不连通输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，答案用 `long long`。",
    hint_md="边按权值排序，用并查集判断是否成环；选够 n-1 条边就停。",
    tags=["Kruskal", "并查集"],
    cases=["4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n1 3 5", "3 1\n1 2 1",
           "2 1\n1 2 1000000000", "4 6\n1 2 1\n2 3 2\n3 4 3\n4 1 5\n1 3 4\n2 4 10"],
    solve=p2101)

def p2102(t):
    lines = t.strip().splitlines()
    p = 0
    n = int(lines[p]); p += 1
    g = []
    for _ in range(n):
        g.append(list(map(int, lines[p].split()))); p += 1
    INF = 10 ** 18
    dist = [INF] * n
    used = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u = -1
        for i in range(n):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] >= INF:
            return "-1"
        used[u] = True
        total += dist[u]
        for v in range(n):
            if g[u][v] and not used[v] and g[u][v] < dist[v]:
                dist[v] = g[u][v]
    return str(total)


add(id="p-21-02", chapter=21, label="习题 21-2", title="Prim 求最小生成树（邻接矩阵）",
    difficulty=2,
    statement_md="用 Prim 重做第 21 章习题 1。说明题面给的是邻接矩阵还是邻接表时，应该选哪种写法。\n\n本题是第 21 章习题 2。本题直接给邻接矩阵：`g[u][v] = 0` 表示没有边，否则是边权。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 200）。\n接下来 n 行，每行 n 个整数，表示邻接矩阵（对角线为 0，边权 1 ≤ w ≤ 10^9）。",
    output_md="一个整数，表示最小生成树总权值；不连通输出 -1。",
    constraints_md="1 ≤ n ≤ 200，边权 ≤ 10^9。",
    hint_md="Prim 维护 `dist` 数组：每轮选一个未使用且 dist 最小的点加入生成树，再用它更新邻居。",
    tags=["Prim", "最小生成树"],
    cases=["4\n0 1 5 10\n1 0 2 0\n5 2 0 3\n10 0 3 0", "3\n0 5 0\n5 0 0\n0 0 0",
           "2\n0 7\n7 0", "1\n0"],
    solve=p2102)

def p2103(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v)
        indeg[v] += 1
    h = [i for i in range(1, n + 1) if indeg[i] == 0]
    heapq.heapify(h)
    out = []
    while h:
        u = heapq.heappop(h)
        out.append(str(u))
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(h, v)
    return " ".join(out) if len(out) == n else "No"


add(id="p-21-03", chapter=21, label="习题 21-3", title="课程表（字典序最小）",
    difficulty=2,
    statement_md="有 n 门课、m 条先修关系，判断能不能排出合法顺序；如果能，输出字典序最小的那个顺序。\n\n本题是第 21 章习题 3：把入度为 0 的点放进小根堆，每次取编号最小的。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 是 v 的先修课（u 必须在 v 之前）。",
    output_md="能排出一行 n 个整数（字典序最小的拓扑序）；有环输出 `No`。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="Kahn 算法 + 小根堆；若最后输出的点少于 n 个，说明有环。",
    tags=["拓扑排序", "堆"],
    cases=["4 3\n1 2\n1 3\n3 4", "3 3\n1 2\n2 3\n3 1", "5 0", "6 6\n2 1\n3 1\n4 2\n5 2\n6 3\n6 4"],
    solve=p2103)

def p2105(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v)
        indeg[v] += 1
    q = deque(i for i in range(1, n + 1) if indeg[i] == 0)
    dp = [0] * (n + 1)
    dp[1] = 1
    MOD = 1000000007
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            dp[v] = (dp[v] + dp[u]) % MOD
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if len(order) < n:
        return "0"
    return str(dp[n] % MOD)


add(id="p-21-05", chapter=21, label="习题 21-5", title="DAG 路径计数",
    difficulty=3,
    statement_md="给一张有向无环图，求从 1 到 n 有多少条路径，答案对 10^9+7 取余。要求在拓扑排序的同时完成 DP。\n\n本题是第 21 章习题 5。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示一条 u→v 的边。",
    output_md="一个整数，表示路径条数对 10^9+7 取余的结果；没有路径输出 0。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，保证是 DAG。",
    hint_md="拓扑序上 `dp[v] += dp[u]`，`dp[1] = 1`；注意 1 可能不是入度为 0 的点。",
    tags=["拓扑排序", "DP"],
    cases=["4 4\n1 2\n1 3\n2 4\n3 4", "3 3\n1 2\n2 3\n1 3", "2 0",
           "5 5\n1 2\n2 5\n1 3\n3 5\n1 5"],
    solve=p2105)

def p2106(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    edges = []
    for i in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        edges.append((w, u, v, i))
    edges.sort()
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    tree = [[] for _ in range(n + 1)]
    total = 0
    used = 0
    non_tree = []
    for w, u, v, idx in edges:
        a, b = find(u), find(v)
        if a != b:
            par[a] = b
            total += w
            used += 1
            tree[u].append((v, w))
            tree[v].append((u, w))
        else:
            non_tree.append((u, v, w))
    if used != n - 1:
        return "-1"

    # 对每条非树边，求树上 u-v 路径上的最大边权
    ans = None
    for u, v, w in non_tree:
        # BFS 找路径
        pre = [(-1, 0)] * (n + 1)
        pre[u] = (0, 0)
        st = [u]
        while st:
            x = st.pop()
            if x == v:
                break
            for y, ww in tree[x]:
                if pre[y][0] == -1:
                    pre[y] = (x, ww)
                    st.append(y)
        mx = 0
        x = v
        while x != u:
            px, ww = pre[x]
            mx = max(mx, ww)
            x = px
        cand = total + w - mx
        if ans is None or cand < ans:
            ans = cand
    return str(ans if ans is not None else -1)


add(id="p-21-06", chapter=21, label="习题 21-6", title="次小生成树",
    difficulty=3,
    statement_md="给一张连通无向带权图，求边权和第二小的生成树（允许和最小生成树权和相同）。提示：先求出一棵 MST，再枚举「删掉树上的一条边、加入一条非树边」。\n\n本题是第 21 章习题 6。",
    input_md="第一行两个整数 n、m（2 ≤ n ≤ 1000，n-1 ≤ m ≤ 2000）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9）。",
    output_md="一个整数，表示次小生成树的权值和；不连通输出 -1。",
    constraints_md="2 ≤ n ≤ 1000，n-1 ≤ m ≤ 2000。",
    hint_md="MST + 每条非树边：加上它会成环，环上删掉一条最大边，得到 `total + w - maxEdge(u,v)`，取最小值。",
    tags=["MST", "枚举"],
    cases=["4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n1 3 5", "3 3\n1 2 1\n2 3 1\n1 3 1",
           "3 3\n1 2 1\n2 3 2\n1 3 3", "4 4\n1 2 1\n2 3 1\n3 4 1\n4 1 1"],
    solve=p2106)

# ================================================================ 第 22 章
def tree_order(n, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    par = [0] * (n + 1)
    depth = [0] * (n + 1)
    order = [1]
    par[1] = 0
    for u in order:
        for v in adj[u]:
            if v != par[u]:
                par[v] = u
                depth[v] = depth[u] + 1
                order.append(v)
    return adj, par, depth, order


def p2201(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    edges = []
    for _ in range(n - 1):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        edges.append((u, v))
    adj, par, depth, order = tree_order(n, edges)
    sz = [1] * (n + 1)
    for u in reversed(order):
        if par[u]:
            sz[par[u]] += sz[u]
    out = []
    for i in range(1, n + 1):
        out.append("%d %d" % (depth[i], sz[i]))
    return "\n".join(out)


add(id="p-22-01", chapter=22, label="习题 22-01", title="每个点的深度与子树大小",
    difficulty=2,
    statement_md="给定一棵 n 个点的树，根为 1。输出每个点的深度（根的深度为 0）和子树大小。要求不用递归（n ≤ 10^5，树可能退化成一条链）。\n\n本题是第 22 章习题 1。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n-1 行，每行两个整数 u、v，表示一条边。",
    output_md="共 n 行，第 i 行两个整数：点 i 的深度、点 i 的子树大小。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="用 BFS/栈求出 `order` 和 `par`，再按 `order` 倒序把子树大小累加到父亲。",
    tags=["树", "遍历"],
    cases=["5\n1 2\n1 3\n2 4\n2 5", "1", "4\n1 2\n2 3\n3 4", "3\n1 2\n1 3"],
    solve=p2201)

def p2203(t):
    d = t.split()
    p = 0
    n, q = int(d[p]), int(d[p + 1]); p += 2
    edges = []
    for _ in range(n - 1):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        edges.append((u, v))
    adj, par, depth, order = tree_order(n, edges)
    LOG = max(1, (n).bit_length())
    up = [[0] * (n + 1) for _ in range(LOG)]
    up[0] = par[:]
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k - 1][up[k - 1][i]]

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return par[u]

    out = []
    for _ in range(q):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        w = lca(u, v)
        out.append(str(depth[u] + depth[v] - 2 * depth[w]))
    return "\n".join(out)


add(id="p-22-03", chapter=22, label="习题 22-3", title="树上两点距离（LCA）",
    difficulty=3,
    statement_md="n 个点的树，q 次询问，每次给 u、v，输出两点之间的边数。提示：先求 w = LCA(u, v)，答案是 `depth[u] + depth[v] - 2*depth[w]`，体会一下为什么这个式子成立。\n\n本题是第 22 章习题 3。",
    input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 10^5）。\n接下来 n-1 行，每行两个整数 u、v。\n接下来 q 行，每行两个整数 u、v。",
    output_md="对每次询问输出一行，表示两点间边数。",
    constraints_md="1 ≤ n, q ≤ 10^5。",
    hint_md="倍增：先让深的点跳到同一深度，再一起往上跳；`up[k][i]` 表示 i 的 2^k 级祖先。",
    tags=["LCA", "倍增"],
    cases=["5 3\n1 2\n1 3\n2 4\n2 5\n4 5\n3 4\n1 5", "1 1\n1 1", "4 2\n1 2\n2 3\n3 4\n1 4\n2 4",
           "6 3\n1 2\n1 3\n2 4\n2 5\n3 6\n4 5\n4 6\n1 6"],
    solve=p2203)

def p2204(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    edges = []
    for _ in range(n - 1):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        edges.append((u, v))
    adj, par, depth, order = tree_order(n, edges)
    LOG = max(1, n.bit_length())
    up = [[0] * (n + 1) for _ in range(LOG)]
    up[0] = par[:]
    for k in range(1, LOG):
        for i in range(1, n + 1):
            up[k][i] = up[k - 1][up[k - 1][i]]

    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        k = 0
        while diff:
            if diff & 1:
                u = up[k][u]
            diff >>= 1
            k += 1
        if u == v:
            return u
        for k in range(LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return par[u]

    diff = [0] * (n + 1)
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        w = lca(u, v)
        diff[u] += 1
        diff[v] += 1
        diff[w] -= 2
    for u in reversed(order):
        if par[u]:
            diff[par[u]] += diff[u]
    return "\n".join(str(diff[v]) for v in range(2, n + 1))


add(id="p-22-04", chapter=22, label="习题 22-4", title="每条边被经过几次",
    difficulty=3,
    statement_md="贵阳某小区的配送路线：树上有 m 条路径，第 i 条从 u 到 v，每条路径上的边都算被经过一次。输出每条边被经过的次数（按「这个点连向它父亲的那条边」输出，点 2 到 n 各一行）。用点差分和边差分各写一遍，比较两者的差别。\n\n本题是第 22 章习题 4。",
    input_md="第一行两个整数 n、m（2 ≤ n ≤ 10^5，1 ≤ m ≤ 10^5）。\n接下来 n-1 行，每行两个整数 u、v。\n接下来 m 行，每行两个整数 u、v，表示一条路径。",
    output_md="共 n-1 行，第 i 行表示点 i+1 连向它父亲的那条边被经过的次数。",
    constraints_md="2 ≤ n ≤ 10^5，1 ≤ m ≤ 10^5。",
    hint_md="`diff[u]++`、`diff[v]++`、`diff[lca]-=2`，最后自底向上把子树和累加到父亲，`diff[x]` 就是 x 到父亲那条边的次数。",
    tags=["树上差分", "LCA"],
    cases=["4 1\n1 2\n2 3\n3 4\n1 4", "3 2\n1 2\n2 3\n1 2\n2 3",
           "5 2\n1 2\n1 3\n2 4\n2 5\n4 5\n3 5"],
    solve=p2204)

def p2205(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    edges = []
    for _ in range(n - 1):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        edges.append((u, v))
    adj, par, depth, order = tree_order(n, edges)
    sz = [1] * (n + 1)
    for u in reversed(order):
        if par[u]:
            sz[par[u]] += sz[u]
    centroid = 1
    best = n + 1
    for u in range(1, n + 1):
        mx = n - sz[u]
        for v in adj[u]:
            if par[v] == u:
                mx = max(mx, sz[v])
        if mx < best:
            best = mx
            centroid = u
    # 到所有点的距离之和（换根 DP）
    sub = [0] * (n + 1)
    for u in reversed(order):
        for v in adj[u]:
            if par[v] == u:
                sub[u] += sub[v] + sz[v]
    total = [0] * (n + 1)
    total[1] = sub[1]
    for u in order:
        for v in adj[u]:
            if par[v] == u:
                total[v] = total[u] + (n - 2 * sz[v])
    return "\n".join([str(centroid)] + [str(total[i]) for i in range(1, n + 1)])


add(id="p-22-05", chapter=22, label="习题 22-5", title="快递柜选址（重心与换根）",
    difficulty=3,
    statement_md="给定一棵 n 个点的树（边权都为 1），先求它的重心（删掉该点后剩余最大连通块最小的点，若有多个取编号最小的）；再求以每个点为根时到所有点的距离之和，要求 O(n)。\n\n本题是第 22 章习题 5。第二问就是换根 DP：`sum[v] = sum[u] + n - 2*sz[v]`。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n-1 行，每行两个整数 u、v。",
    output_md="第一行一个整数，表示重心编号；接下来 n 行，第 i 行表示以点 i 为根时到所有点的距离之和。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="先求子树大小；重心的判据是「最大子树 ≤ n/2」。换根时从父亲 u 挪到儿子 v，v 子树内的点近一步、其余点远一步。",
    tags=["树", "换根 DP", "重心"],
    cases=["5\n1 2\n1 3\n2 4\n2 5", "1", "4\n1 2\n2 3\n3 4",
           "6\n1 2\n1 3\n2 4\n2 5\n3 6"],
    solve=p2205)


def p2202(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    def farthest(s):
        dist = [-1] * (n + 1)
        dist[s] = 0
        st = [s]
        while st:
            u = st.pop()
            for v, w in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + w
                    st.append(v)
        best = 0
        for i in range(1, n + 1):
            if dist[i] > dist[best]:
                best = i
        return best, dist[best]

    if n == 1:
        return "0"
    a, _ = farthest(1)
    _, ans = farthest(a)
    return str(ans)


add(id="p-22-02", chapter=22, label="习题 22-2", title="树的直径（两次遍历）",
    difficulty=2,
    statement_md="用「两次遍历」求带权树的直径：先从任意点出发找到离它最远的 a，再从 a 出发找到离它最远的 b，a 到 b 的距离就是直径。请写完跟第 26 章的树形 DP 版本对拍，并说明为什么第一次找到的 a 一定在直径的一端。\n\n本题是第 22 章习题 2。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n-1 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9）。",
    output_md="一个整数，表示树的直径（最长路径的边权和）。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ w ≤ 10^9，答案用 `long long`。",
    hint_md="两次 DFS/BFS：第一次从 1 出发求最远点 a，第二次从 a 出发求最远距离。n 很大时用迭代，别递归。",
    tags=["树", "直径"],
    cases=["5\n1 2 3\n2 3 4\n2 4 5\n4 5 6", "1", "2\n1 2 10", "6\n1 2 1\n2 3 2\n3 4 3\n4 5 4\n5 6 5"],
    solve=p2202)