#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 17～18 章可编程习题。"""
PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


class DSU:
    def __init__(self, n):
        self.p = list(range(n + 1))
        self.sz = [1] * (n + 1)

    def find(self, x):
        p = self.p
        while p[x] != x:
            p[x] = p[p[x]]
            x = p[x]
        return x

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.p[b] = a
        self.sz[a] += self.sz[b]
        return True


# ================================================================ 第 17 章
def p1701(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    dsu = DSU(n)
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        dsu.union(u, v)
    roots = [dsu.find(i) for i in range(1, n + 1)]
    groups = len(set(roots))
    best = max(dsu.sz[r] for r in set(roots))
    return "%d %d" % (groups, best)


add(id="p-17-01", chapter=17, label="习题 17-1", title="朋友圈",
    difficulty=1,
    statement_md="n 个人、m 对朋友，朋友的朋友也是朋友。读入后输出朋友圈的个数，以及最大的朋友圈有多少人。\n\n本题是第 17 章习题 1：提示在根上维护 `sz`。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 与 v 是朋友。",
    output_md="一行两个整数：朋友圈个数、最大朋友圈人数。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="并查集合并，同时在根上维护集合大小；最后数不同根的个数，取最大大小。",
    tags=["并查集"],
    cases=["5 3\n1 2\n2 3\n4 5", "3 0", "4 6\n1 2\n2 3\n3 4\n1 4\n1 3\n2 4",
           "6 2\n1 2\n4 5"],
    solve=p1701)

def p1702(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    dsu = DSU(n)
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        dsu.union(u, v)
    return str(len({dsu.find(i) for i in range(1, n + 1)}) - 1)


add(id="p-17-02", chapter=17, label="习题 17-2", title="还要修几条路",
    difficulty=1,
    statement_md="有 n 个村子，已经修了 m 条路（可能重复、可能有自环）。问最少还要修几条路才能让所有村子连通？如果已经连通，输出 0。\n\n本题是第 17 章习题 2。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 与 v 之间已有道路。",
    output_md="一个整数，表示最少还要修的路数。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="把所有已有道路合并，最后统计不同连通块个数 k，答案是 k-1。",
    tags=["并查集"],
    cases=["4 2\n1 2\n3 4", "3 0", "3 3\n1 2\n2 3\n1 3", "2 1\n1 1"],
    solve=p1702)

def p1704(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    dsu = DSU(n)
    cnt = n
    out = []
    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        if dsu.union(u, v):
            cnt -= 1
        out.append(str(cnt))
    return "\n".join(out)


add(id="p-17-04", chapter=17, label="习题 17-4", title="动态连通块",
    difficulty=2,
    statement_md="初始有 n 个孤立点，依次加入 m 条无向边，每加一条边后输出当前的连通块个数。要求总复杂度 O((n+m)α(n))，不能每次重新数。\n\n本题是第 17 章习题 4。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，1 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v。",
    output_md="共 m 行，第 i 行表示加入第 i 条边后的连通块个数。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ m ≤ 2×10^5。",
    hint_md="初始答案 n；每次 `union` 成功（两个端点原本不同根）就把答案减一。",
    tags=["并查集"],
    cases=["4 3\n1 2\n3 4\n2 3", "2 2\n1 2\n1 2", "3 3\n1 1\n2 2\n3 3",
           "5 4\n1 2\n2 3\n3 4\n4 5"],
    solve=p1704)

# ================================================================ 第 18 章
def p1801(t):
    d = t.split()
    p = 0
    n, q = int(d[p]), int(d[p + 1]); p += 2
    tree = [0] * (n + 1)

    def add(i, v):
        while i <= n:
            tree[i] += v
            i += i & -i

    def pref(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s

    out = []
    for _ in range(q):
        op = int(d[p]); p += 1
        if op == 1:
            x, v = int(d[p]), int(d[p + 1]); p += 2
            add(x, v)
        else:
            l, r = int(d[p]), int(d[p + 1]); p += 2
            out.append(str(pref(r) - pref(l - 1)))
    return "\n".join(out)


add(id="p-18-01", chapter=18, label="习题 18-1", title="树状数组：单点加、区间和",
    difficulty=2,
    statement_md="维护一个长度为 n 的数组，初始全为 0，支持两种操作：把 `a[x]` 加上 k；询问 `[l, r]` 的和。n、操作数都不超过 10^5，要求每次操作 O(log n)。用树状数组实现。\n\n本题是第 18 章习题 1。",
    input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 10^5）。\n接下来 q 行：`1 x k` 表示 `a[x] += k`；`2 l r` 表示询问区间和。",
    output_md="对每次询问输出一行，表示 `[l, r]` 的和。",
    constraints_md="1 ≤ n, q ≤ 10^5，1 ≤ k ≤ 10^9，答案可能超过 `int`。",
    hint_md="`add` 沿 `i += i&-i` 向上，`query` 沿 `i -= i&-i` 向下；区间和等于两个前缀相减。",
    tags=["树状数组"],
    cases=["5 4\n1 2 3\n2 1 5\n1 4 10\n2 2 4\n2 1 1", "1 2\n1 1 5\n2 1 1",
           "3 3\n2 1 3\n1 2 1\n2 1 3", "4 5\n1 1 1\n1 2 2\n1 3 3\n2 1 3\n2 2 4"],
    solve=p1801)

def p1802(t):
    d = t.split()
    p = 0
    n, q = int(d[p]), int(d[p + 1]); p += 2
    diff = [0] * (n + 2)

    def add(i, v):
        while i <= n:
            diff[i] += v
            i += i & -i

    def query(i):
        s = 0
        while i > 0:
            s += diff[i]
            i -= i & -i
        return s

    out = []
    for _ in range(q):
        op = int(d[p]); p += 1
        if op == 1:
            l, r, k = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
            add(l, k)
            if r + 1 <= n:
                add(r + 1, -k)
        else:
            x = int(d[p]); p += 1
            out.append(str(query(x)))
    return "\n".join(out)


add(id="p-18-02", chapter=18, label="习题 18-2", title="树状数组：区间加、单点查",
    difficulty=2,
    statement_md="维护一个数组（初始全 0），支持「区间 `[l, r]` 每个数加 k」和「询问 `a[x]` 的值」。用差分 + 树状数组实现，说明为什么只需要改两个位置。\n\n本题是第 18 章习题 2。",
    input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 10^5）。\n接下来 q 行：`1 l r k` 表示区间加；`2 x` 表示询问。",
    output_md="对每次询问输出一行，表示 `a[x]` 的值。",
    constraints_md="1 ≤ n, q ≤ 10^5，1 ≤ k ≤ 10^9。",
    hint_md="对差分数组做树状数组：区间加变成 `d[l]+=k`、`d[r+1]-=k`，单点值就是前缀和。",
    tags=["树状数组", "差分"],
    cases=["5 4\n1 1 5 1\n2 3\n1 2 4 10\n2 4\n2 1", "1 3\n1 1 1 5\n2 1\n2 1",
           "3 4\n2 1\n1 1 3 2\n2 2\n2 3"],
    solve=p1802)

def p1803(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    tmp = [0] * n

    def rec(l, r):
        if r - l <= 1:
            return 0
        mid = (l + r) // 2
        cnt = rec(l, mid) + rec(mid, r)
        i, j, k = l, mid, l
        while i < mid and j < r:
            if a[i] <= a[j]:
                tmp[k] = a[i]; i += 1
            else:
                tmp[k] = a[j]; j += 1
                cnt += mid - i
            k += 1
        while i < mid:
            tmp[k] = a[i]; i += 1; k += 1
        while j < r:
            tmp[k] = a[j]; j += 1; k += 1
        a[l:r] = tmp[l:r]
        return cnt

    return str(rec(0, n))


add(id="p-18-03", chapter=18, label="习题 18-3", title="逆序对（离散化 + 树状数组）",
    difficulty=2,
    statement_md="给定长度为 n 的序列，求逆序对个数，要求 O(n log n)。如果数据范围是 a[i] ≤ 10^9，需要先做什么处理？\n\n本题是第 18 章习题 3。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示逆序对个数。",
    constraints_md="1 ≤ n ≤ 10^5，答案可能达到 n²/2，用 `long long`。",
    hint_md="先把值离散化到 1..n，再从右往左扫，用树状数组统计「已经出现过且比当前小」的个数。",
    tags=["树状数组", "逆序对"],
    cases=["5\n3 1 4 5 2", "1\n7", "4\n4 3 2 1", "5\n1 2 3 4 5", "6\n2 2 1 1 3 3"],
    solve=p1803)

def p1804(t):
    d = t.split()
    p = 0
    n, q = int(d[p]), int(d[p + 1]); p += 2
    a = list(map(int, d[p:p + n])); p += n
    tree = [0] * (4 * n + 5)

    def build(o, l, r):
        if l == r:
            tree[o] = a[l - 1]
            return
        mid = (l + r) // 2
        build(o * 2, l, mid)
        build(o * 2 + 1, mid + 1, r)
        tree[o] = max(tree[o * 2], tree[o * 2 + 1])

    def update(o, l, r, pos, val):
        if l == r:
            tree[o] = val
            return
        mid = (l + r) // 2
        if pos <= mid:
            update(o * 2, l, mid, pos, val)
        else:
            update(o * 2 + 1, mid + 1, r, pos, val)
        tree[o] = max(tree[o * 2], tree[o * 2 + 1])

    def query(o, l, r, ql, qr):
        if ql <= l and r <= qr:
            return tree[o]
        mid = (l + r) // 2
        ans = -10 ** 30
        if ql <= mid:
            ans = max(ans, query(o * 2, l, mid, ql, qr))
        if qr > mid:
            ans = max(ans, query(o * 2 + 1, mid + 1, r, ql, qr))
        return ans

    build(1, 1, n)
    out = []
    for _ in range(q):
        op = int(d[p]); p += 1
        if op == 1:
            x, v = int(d[p]), int(d[p + 1]); p += 2
            update(1, 1, n, x, v)
        else:
            l, r = int(d[p]), int(d[p + 1]); p += 2
            out.append(str(query(1, 1, n, l, r)))
    return "\n".join(out)


add(id="p-18-04", chapter=18, label="习题 18-4", title="线段树：区间最大值",
    difficulty=2,
    statement_md="维护一个数组，支持单点修改和区间最大值查询。请写出 `pushup` 的写法，并说明为什么区间最大值的查询不能像求和那样用两个前缀相减。\n\n本题是第 18 章习题 4。",
    input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。\n接下来 q 行：`1 x v` 把 `a[x]` 改为 v；`2 l r` 询问区间最大值。",
    output_md="对每次 `2 l r` 输出一行，表示区间最大值。",
    constraints_md="1 ≤ n, q ≤ 10^5。",
    hint_md="`pushup(o)` 就是 `tree[o] = max(tree[o*2], tree[o*2+1])`；最大值不可减，所以必须查询整段。",
    tags=["线段树"],
    cases=["5 4\n3 1 4 1 5\n2 1 5\n1 2 9\n2 2 3\n2 1 5", "1 2\n5\n2 1 1\n1 1 3",
           "3 2\n1 2 3\n2 1 3\n1 3 10"],
    solve=p1804)

def p1806(t):
    d = t.split()
    p = 0
    n, m, q = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
    bit = [[0] * (m + 1) for _ in range(n + 1)]

    def add(x, y, v):
        i = x
        while i <= n:
            j = y
            while j <= m:
                bit[i][j] += v
                j += j & -j
            i += i & -i

    def qry(x, y):
        s = 0
        i = x
        while i > 0:
            j = y
            while j > 0:
                s += bit[i][j]
                j -= j & -j
            i -= i & -i
        return s

    out = []
    for _ in range(q):
        op = int(d[p]); p += 1
        if op == 1:
            x, y, v = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
            add(x, y, v)
        else:
            x, y = int(d[p]), int(d[p + 1]); p += 2
            out.append(str(qry(x, y)))
    return "\n".join(out)


add(id="p-18-06", chapter=18, label="习题 18-6", title="二维树状数组",
    difficulty=3,
    statement_md="维护一个 n×m 的矩阵，初始全 0，支持「单点加」和「求左上角到 (x,y) 的子矩阵和」，要求每次操作 O(log n log m)。\n\n本题是第 18 章习题 6：提示外层一个树状数组，每个结点里再放一个树状数组。",
    input_md="第一行三个整数 n、m、q（1 ≤ n, m ≤ 500，1 ≤ q ≤ 10^5）。\n接下来 q 行：`1 x y v` 表示 `a[x][y] += v`；`2 x y` 表示询问左上角到 (x,y) 的和。",
    output_md="对每次询问输出一行，表示子矩阵和。",
    constraints_md="1 ≤ n, m ≤ 500，1 ≤ q ≤ 10^5，1 ≤ v ≤ 10^9，答案用 `long long`。",
    hint_md="二维树状数组：两个维度都按 `i += i&-i` 向上更新，查询时两个维度都向下；前缀和相减可得任意子矩阵。",
    tags=["二维树状数组"],
    cases=["3 3 5\n1 1 1 5\n1 2 2 3\n2 2 2\n2 3 3\n1 3 3 1", "1 1 3\n1 1 1 7\n2 1 1\n2 1 1",
           "2 2 4\n1 1 1 1\n1 2 2 2\n2 2 2\n2 1 2"],
    solve=p1806)
