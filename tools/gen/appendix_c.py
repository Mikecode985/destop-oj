#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""附录 C　贵阳主题练习 40 题：标准题面 + 参考解 + 测试数据。

每个题目包含：id/kind/title/难度/题面/输入输出格式/数据范围/提示/cases；
solve(text) 为参考解，用于生成期望输出。
"""
from bisect import bisect_left, bisect_right
from collections import deque
import heapq
from itertools import combinations

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "appendix")
    kw.setdefault("chapter", 0)
    kw.setdefault("sample_n", 2)
    PROBLEMS.append(kw)


# ---------------------------------------------------------------- C-01
def c01(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    idx = max(range(n), key=lambda i: (a[i], -i))
    return "%d\n%d" % (sum(a), idx + 1)


add(id="c-01", label="C-01", title="贵阳地铁一号线的日客流", difficulty=1,
    statement_md="地铁 1 号线有 n 个站，给出某日各站的进站人次。请算出全线总客流，以及客流最大的是第几号站（从 1 开始编号；若并列最大，输出编号较小的那个）。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 a[1..n]（0 ≤ a[i] ≤ 10^9），依次表示各站进站人次。",
    output_md="第一行一个整数，表示总客流。\n第二行一个整数，表示客流最大站的编号。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ a[i] ≤ 10^9。总客流可达 10^14，需要用 64 位整数。",
    hint_md="总和能到 10^14，用 `long long` 累加；最大值并列时取小编号。",
    tags=["数组", "求和"],
    cases=[
        "5\n120 300 260 410 390",
        "3\n1000000000 1000000000 1000000000",
        "1\n0",
        "10\n5 3 9 9 2 9 1 0 4 7",
        "2\n0 0",
        "100000\n" + " ".join(["1000000000"] * 100000),
    ],
    solve=c01)

# ---------------------------------------------------------------- C-02
def c02(t):
    lines = t.strip().splitlines()
    n = int(lines[0])
    items = []
    for ln in lines[1:1 + n]:
        name, price = ln.rsplit(" ", 1)
        items.append((int(price), name))
    items.sort()
    return "\n".join("%s %d" % (nm, pr) for pr, nm in items)


add(id="c-02", label="C-02", title="青云市集按价格排序", difficulty=2,
    statement_md="青云市集有 n 个摊位，每个摊位有一个名字和一个单价。请按单价从低到高输出摊位；单价相同的，按名字的字典序（ASCII 顺序）从小到大。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行是「摊位名 单价」，摊位名不含空格，单价为整数。",
    output_md="共 n 行，每行「摊位名 单价」，按题目要求的顺序输出。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ 单价 ≤ 10^9；摊位名只含大小写字母和数字。",
    hint_md="结构体（或 pair）加 `sort`，先比价格再比名字。",
    tags=["排序", "结构体"],
    cases=[
        "6\n丝娃娃 18\n肠旺面 12\n烤脑花 25\n恋爱豆腐果 8\n牛肉粉 13\n酸汤鱼 45",
        "3\nB 5\nA 5\nC 1",
        "1\nOnly 100",
        "5\nz 1\ny 1\nx 1\nw 1\nv 1",
        "8\na 1000000000\nb 1\nc 999999999\nd 2\ne 500000000\nf 3\ng 4\nh 5",
    ],
    solve=c02)

# ---------------------------------------------------------------- C-03
def c03(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    mp = {}
    for _ in range(n):
        line, station = d[p], d[p + 1]; p += 2
        mp.setdefault(station, set()).add(line)
    out = []
    for _ in range(m):
        station, line = d[p], d[p + 1]; p += 2
        out.append("Yes" if line in mp.get(station, set()) else "No")
    return "\n".join(out)


add(id="c-03", label="C-03", title="地铁站名速查", difficulty=2,
    statement_md="给出 n 条「线路号 站名」的记录，再给出 m 次询问。每次询问给出一个站名和一条线路号，回答这个站是否在这条线路上。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 10^5）。\n接下来 n 行，每行「线路号 站名」。\n接下来 m 行，每行「站名 线路号」。",
    output_md="对每次询问输出一行：在该线路上输出 `Yes`，否则输出 `No`。",
    constraints_md="1 ≤ n, m ≤ 10^5；线路号与站名均不含空格，长度不超过 20。",
    hint_md="用 `map<string, set<int>>` 记站名到线路集合，询问时查集合。",
    tags=["map", "set"],
    cases=[
        "5 3\n1 喷水池\n1 贵阳北站\n1 北京路\n2 林城西路\n2 龙洞堡机场\n喷水池 1\n龙洞堡机场 1\n林城西路 2",
        "2 2\n1 A\n2 A\nA 1\nA 2",
        "1 1\n7 X\nX 7",
        "4 4\n1 S1\n1 S2\n2 S2\n3 S3\nS2 1\nS2 2\nS2 3\nS9 1",
    ],
    solve=c03)

# ---------------------------------------------------------------- C-04
def c04(t):
    n = int(t.split()[0])
    return str((n * (n + 1) // 2) % 1000000007)


add(id="c-04", label="C-04", title="一步算完的求和", difficulty=1,
    statement_md="求 1 + 2 + … + n 的值对 10^9 + 7 取余的结果。n 很大，循环一遍会超时。",
    input_md="一个整数 n（1 ≤ n ≤ 10^9）。",
    output_md="一个整数，表示 1 到 n 的和对 10^9+7 取余的结果。",
    constraints_md="1 ≤ n ≤ 10^9，时间限制 1 秒。",
    hint_md="用等差数列公式 `n*(n+1)/2`，先乘后除（或先除后乘保证整除），再取模。",
    tags=["数学", "复杂度"],
    cases=["10", "1", "1000000000", "999999999", "2"],
    solve=c04)

# ---------------------------------------------------------------- C-05
def c05(t):
    a = list(map(int, t.split()[:7]))
    days = sum(1 for x in a if x != -1)
    total = sum(x for x in a if x != -1)
    avg = total // days if days else 0
    return "%d\n%d\n%d" % (days, total, avg)


add(id="c-05", label="C-05", title="肠旺面馆的一周营业额", difficulty=1,
    statement_md="老周记下一周七天的营业额，用 -1 表示当天店休。请统计营业天数、总营业额和日均营业额（向下取整）。",
    input_md="一行七个整数，依次表示周一到周日的营业额；-1 表示店休，否则为 0 到 10^6 的整数。",
    output_md="三行，依次为营业天数、总营业额、日均营业额（总营业额除以营业天数，向下取整）。",
    constraints_md="营业额 0 ≤ x ≤ 10^6；一周七天；至少有一天营业。",
    hint_md="店休既不计天数也不计入总和，日均的分母是营业天数。",
    tags=["模拟"],
    cases=["100 200 -1 300 400 -1 500", "0 0 0 0 0 0 0", "1000000 -1 -1 -1 -1 -1 -1",
           "5 5 5 5 5 5 -1", "-1 -1 -1 1 2 3 4"],
    solve=c05)

# ---------------------------------------------------------------- C-06
def c06(t):
    s = int(t.split()[0])
    if s <= 4:
        f = 2
    elif s <= 9:
        f = 3
    elif s <= 15:
        f = 4
    else:
        f = 4 + (s - 15 + 4) // 5
    return str(min(f, 8))


add(id="c-06", label="C-06", title="地铁分段计价", difficulty=2,
    statement_md="某观光线按乘坐站数计价：1～4 站 2 元，5～9 站 3 元，10～15 站 4 元；16 站及以上，在 4 元基础上每满 5 站加 1 元（不足 5 站按 5 站算），最高 8 元。给出乘坐站数，输出票价。",
    input_md="一个整数 s（1 ≤ s ≤ 60），表示乘坐的站数。",
    output_md="一个整数，表示票价（元）。",
    constraints_md="1 ≤ s ≤ 60。",
    hint_md="先列区间到价格的分支表，再单独处理 16 站以上：`4 + ceil((s-15)/5)`，最后与 8 取较小值。",
    tags=["模拟", "分类讨论"],
    cases=["3", "4", "5", "9", "10", "15", "16", "21", "60"],
    solve=c06)

# ---------------------------------------------------------------- C-07
def c07(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    best = 0
    for mask in range(1 << n):
        if bin(mask).count("1") > k:
            continue
        s = 0
        for i in range(n):
            if mask >> i & 1:
                s += a[i]
        best = max(best, s)
    return str(best)


add(id="c-07", label="C-07", title="丝娃娃的配料组合", difficulty=2,
    statement_md="丝娃娃有 n 样菜，第 i 样的满足度是 a[i]。一张皮最多包 k 样菜，每样菜最多选一次。问能得到的最大满足度之和。",
    input_md="第一行两个整数 n、k（1 ≤ n ≤ 20，1 ≤ k ≤ 8）。\n第二行 n 个整数 a[i]（1 ≤ a[i] ≤ 100）。",
    output_md="一个整数，表示最大满足度之和。",
    constraints_md="1 ≤ n ≤ 20，1 ≤ k ≤ 8，1 ≤ a[i] ≤ 100。",
    hint_md="用 1 到 (1<<n)-1 枚举所有子集，数一数选的个数不超过 k 就更新答案。",
    tags=["枚举", "二进制"],
    cases=["5 5\n1 2 3 4 5", "5 2\n1 2 3 4 5", "1 1\n100", "6 3\n10 10 10 10 10 10",
           "20 8\n" + " ".join(str((i * 7) % 100 + 1) for i in range(20))],
    solve=c07)

# ---------------------------------------------------------------- C-08
def c08(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    a = list(map(int, d[p:p + n])); p += n
    out = []
    for _ in range(m):
        x = int(d[p]); p += 1
        i = bisect_right(a, x)
        out.append(str(a[i]) if i < n else "-1")
    return "\n".join(out)


add(id="c-08", label="C-08", title="青岩古镇小吃街的问价", difficulty=2,
    statement_md="小吃街有 n 家店，价格已经按非降序排好。有 m 次询问，每次给一个预算 x，请找出价格严格大于 x 的店中价格最低的一家。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 10^5）。\n第二行 n 个整数，表示非降序排列的价格（1 ≤ 价格 ≤ 10^9）。\n第三行 m 个整数 x，表示每次询问的预算。",
    output_md="对每次询问输出一行：满足条件的最低价格；没有满足条件的店输出 -1。",
    constraints_md="1 ≤ n, m ≤ 10^5，1 ≤ 价格, x ≤ 10^9。",
    hint_md="有序数组上找「第一个大于 x」，就是 `upper_bound`；手写时注意返回 n 表示不存在。",
    tags=["二分", "upper_bound"],
    cases=["5 3\n1 3 5 7 9\n3 4 10", "1 1\n100\n100", "4 2\n2 2 2 2\n1 2",
           "6 4\n1 2 2 5 9 9\n0 2 9 10", "100000 3\n" + " ".join(str(i * 2 + 1) for i in range(100000)) + "\n1 50000 200000"],
    solve=c08)

# ---------------------------------------------------------------- C-09
def c09(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    L = list(map(int, d[2:2 + n]))
    lo, hi, ans = 1, max(L), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if sum(x // mid for x in L) >= k:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(ans)


add(id="c-09", label="C-09", title="花溪公园的木板", difficulty=3,
    statement_md="公园有 n 段木板，第 i 段长 L[i]。现在要切出至少 k 段长度相同的木板（边角料可以丢弃），问每段最长能有多长。切不出来输出 0。",
    input_md="第一行两个整数 n、k（1 ≤ n ≤ 10^5，1 ≤ k ≤ 10^9）。\n第二行 n 个整数 L[i]（1 ≤ L[i] ≤ 10^9）。",
    output_md="一个整数，表示每段的最大长度；一段都切不出输出 0。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ k ≤ 10^9，1 ≤ L[i] ≤ 10^9。",
    hint_md="长度越长越难切够 k 段，答案有单调性：二分长度，`check(len)` 累加各段能切出的段数。",
    tags=["二分答案"],
    cases=["2 10\n6 5", "2 20\n6 5", "1 1\n1", "3 5\n1 1 1", "4 4\n10 10 10 10",
           "5 3\n1 2 3 4 5", "100000 1000000000\n" + " ".join(["1000000000"] * 100000)],
    solve=c09)

# ---------------------------------------------------------------- C-10
def c10(t):
    d = t.split()
    n = int(d[0])
    seg = []
    for i in range(n):
        seg.append((int(d[1 + 2 * i]), int(d[2 + 2 * i])))
    seg.sort(key=lambda x: x[1])
    cnt, last = 0, -1
    for s, e in seg:
        if s >= last:
            cnt += 1
            last = e
    return str(cnt)


add(id="c-10", label="C-10", title="花溪公园的一日活动", difficulty=2,
    statement_md="一天有 n 个活动，第 i 个活动从 s[i] 持续到 t[i]。同一时刻只能参加一个活动，首尾相接（一个结束时间等于下一个开始时间）不算冲突。问最多能参加几个活动。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行两个整数 s[i]、t[i]（0 ≤ s[i] < t[i] ≤ 10^9）。",
    output_md="一个整数，表示最多能参加的活动数。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ s[i] < t[i] ≤ 10^9。",
    hint_md="按结束时间从早到晚排序，能参加就参加。",
    tags=["贪心", "区间调度"],
    cases=["4\n0 3\n2 5\n4 6\n6 8", "1\n0 100", "3\n1 2\n2 3\n3 4",
           "4\n0 10\n1 2\n2 3\n3 4", "5\n5 9\n0 2\n3 4\n6 8\n7 9"],
    solve=c10)

# ---------------------------------------------------------------- C-11
def c11(t):
    n = int(t.split()[0])
    a, b = 1, 2
    if n == 1:
        return "1"
    for _ in range(3, n + 1):
        a, b = b, a + b
    return str(b)


add(id="c-11", label="C-11", title="黔灵山的台阶", difficulty=1,
    statement_md="上黔灵山有 n 级台阶，每步可以迈 1 级或 2 级。问走到第 n 级共有多少种走法。",
    input_md="一个整数 n（1 ≤ n ≤ 40）。",
    output_md="一个整数，表示走法数。",
    constraints_md="1 ≤ n ≤ 40，答案在 64 位整数范围内。",
    hint_md="`f(n) = f(n-1) + f(n-2)`，出口 `f(1)=1`、`f(2)=2`。",
    tags=["递推"],
    cases=["1", "2", "3", "10", "40"],
    solve=c11)

# ---------------------------------------------------------------- C-12
def c12(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    cnt = 0
    for i in range(n):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                cnt += 1
    return str(cnt)


add(id="c-12", label="C-12", title="贵阳房价的涨跌对", difficulty=3,
    statement_md="给出连续 n 天的房价。若 i < j 且第 i 天的价格高于第 j 天，则称 (i, j) 是一个「涨跌对」。求涨跌对的总数。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数，表示每天的价格（1 ≤ 价格 ≤ 10^9）。",
    output_md="一个整数，表示涨跌对总数。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ 价格 ≤ 10^9。答案可能达到 5×10^9，需要用 64 位整数。",
    hint_md="这就是逆序对：归并排序合并时数一数，或树状数组/离散化，答案用 `long long`。",
    tags=["分治", "逆序对"],
    cases=["5\n5 1 4 2 3", "1\n10", "3\n1 2 3", "3\n3 2 1", "6\n6 5 4 3 2 1",
           "8\n1 1 1 1 1 1 1 1", "1000\n" + " ".join(str((i * 37) % 1000) for i in range(1000))],
    solve=c12)

# ---------------------------------------------------------------- C-13
def c13(t):
    lines = t.strip().splitlines()
    n, m = map(int, lines[0].split())
    g = [list(lines[i + 1].strip()) for i in range(n)]
    best = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] != "1":
                continue
            g[i][j] = "0"
            st = [(i, j)]
            size = 0
            while st:
                x, y = st.pop()
                size += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == "1":
                        g[nx][ny] = "0"
                        st.append((nx, ny))
            best = max(best, size)
    return str(best)


add(id="c-13", label="C-13", title="黔灵山猕猴的活动区", difficulty=2,
    statement_md="后山被划成 n 行 m 列的格子，1 表示树林、0 表示空地。猕猴只能在树林间沿上下左右移动。问最大的一片连通树林有多少格。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行 m 个字符（0 或 1），表示这张地图。",
    output_md="一个整数，表示最大连通树林块的格子数；没有树林输出 0。",
    constraints_md="1 ≤ n, m ≤ 1000。",
    hint_md="遇到没访问过的 1 就做一次 DFS/BFS 计数；10^6 格时递归可能爆栈，建议用显式栈。",
    tags=["DFS", "连通块"],
    cases=["3 3\n110\n011\n000", "3 3\n101\n010\n101", "1 1\n0", "2 2\n11\n11",
           "5 5\n11111\n10001\n10101\n10001\n11111",
           "1000 1000\n" + "\n".join(["1" * 1000] * 1000)],
    solve=c13)

# ---------------------------------------------------------------- C-14
def c14(t):
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


add(id="c-14", label="C-14", title="从喷水池到龙洞堡机场", difficulty=2,
    statement_md="地铁有 n 个站、m 对相邻关系，坐一站算一步，双向可走。问从 s 站到 t 站最少要坐几站；走不到输出 -1。",
    input_md="第一行四个整数 n、m、s、t（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 与 v 相邻。",
    output_md="一个整数，表示最少乘坐站数；不连通输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ s, t ≤ n。",
    hint_md="无权图最短路用 BFS，第一次访问到 t 时的层数就是答案。",
    tags=["BFS", "最短路"],
    cases=["6 6 1 6\n1 2\n2 3\n3 4\n4 5\n5 6\n1 6", "3 1 1 3\n1 2", "2 0 1 2",
           "5 4 1 5\n1 2\n2 3\n3 4\n4 5", "8 9 2 7\n1 2\n1 3\n2 4\n3 4\n4 5\n5 6\n6 7\n2 7\n5 8"],
    solve=c14)

# ---------------------------------------------------------------- C-15
def c15(t):
    lines = t.strip().splitlines()
    n, m = map(int, lines[0].split())
    g = [list(lines[i + 1].strip()) for i in range(n)]
    dist = [[-1] * m for _ in range(n)]
    q = deque()
    for i in range(n):
        for j in range(m):
            if g[i][j] == "2":
                dist[i][j] = 0
                q.append((i, j))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and g[nx][ny] != "1" and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    ans = 0
    for i in range(n):
        for j in range(m):
            if g[i][j] == "0":
                if dist[i][j] == -1:
                    return "-1"
                ans = max(ans, dist[i][j])
    return str(ans)


add(id="c-15", label="C-15", title="一场雨之后", difficulty=3,
    statement_md="一场雨后，n 行 m 列的街区里有多处积水（用 2 表示），水每分钟向上下左右漫一格，墙（1）挡水，空地记为 0。求水淹到所有空地的最晚时间；有空地永远淹不到则输出 -1。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行 m 个字符：0 表示空地，1 表示墙，2 表示积水。",
    output_md="一个整数，表示所有空地都被淹到的最晚分钟数；有淹不到的空地输出 -1。",
    constraints_md="1 ≤ n, m ≤ 1000。",
    hint_md="把所有水源先入队，多源 BFS；答案取所有空地距离的最大值。",
    tags=["BFS", "多源"],
    cases=["3 3\n200\n000\n001", "3 3\n210\n000\n000", "1 2\n20", "1 2\n21",
           "3 4\n2002\n0110\n0000"],
    solve=c15)

# ---------------------------------------------------------------- C-16
def c16(t):
    n = int(t.split()[0])
    cnt = 0

    def dfs(row, cols, d1, d2):
        nonlocal cnt
        if row == n:
            cnt += 1
            return
        avail = ((1 << n) - 1) & ~(cols | d1 | d2)
        while avail:
            bit = avail & -avail
            avail -= bit
            dfs(row + 1, cols | bit, (d1 | bit) << 1, (d2 | bit) >> 1)

    dfs(0, 0, 0, 0)
    return str(cnt)


add(id="c-16", label="C-16", title="数博会的志愿者站位", difficulty=3,
    statement_md="在 n×n 的展馆方阵里安排 n 名志愿者，要求任意两人不同行、不同列、也不在同一条斜线上。求一共有多少种安排方案。",
    input_md="一个整数 n（1 ≤ n ≤ 8）。",
    output_md="一个整数，表示方案总数。",
    constraints_md="1 ≤ n ≤ 8。",
    hint_md="一行一行放，用三个标记数组（或三个二进制掩码）记列和两条对角线。",
    tags=["回溯", "n 皇后"],
    cases=["1", "4", "8", "6", "7"],
    solve=c16)

# ---------------------------------------------------------------- C-17
def c17(t):
    s = t.strip()
    st = []
    for ch in s:
        if ch == "(":
            st.append(ch)
        elif ch == ")":
            if not st:
                return "No"
            st.pop()
    return "Yes" if not st else "No"


add(id="c-17", label="C-17", title="肠旺面的碗", difficulty=1,
    statement_md="一串碗上印着 `(` 和 `)`。每个右括号都要和它前面最近的一个未配对的左括号配对，且过程中不能出现多余的右括号。判断这串括号是否合法。",
    input_md="一行一个长度不超过 10^5 的括号串，只含 `(` 和 `)`。",
    output_md="合法输出 `Yes`，否则输出 `No`。",
    constraints_md="1 ≤ 串长 ≤ 10^5。",
    hint_md="遇 `(` 入栈，遇 `)` 弹栈（栈空则不合法），最后栈空才合法。",
    tags=["栈"],
    cases=["{[()]}".replace("{", "(").replace("[", "(").replace("]", ")").replace("}", ")"),
           "(())", "())", ")(", "((()))", "()()()"],
    solve=c17)

# ---------------------------------------------------------------- C-18
def c18(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    ans = [0] * n
    st = []
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] <= a[i]:
            st.pop()
        ans[i] = st[-1] + 1 if st else 0
        st.append(i)
    return " ".join(map(str, ans))


add(id="c-18", label="C-18", title="排队时谁挡了视线", difficulty=2,
    statement_md="排队的人身高互不相同的时候更容易看清，但本题允许相等。对每个人，求他右边第一个比他高的人的位置（从 1 开始编号）；没有则输出 0。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 h[i]（1 ≤ h[i] ≤ 10^9）。",
    output_md="一行 n 个整数，依次表示每个人右边第一个更高者的位置；没有输出 0。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ h[i] ≤ 10^9。",
    hint_md="从右往左扫，维护一个身高单调递减的栈；栈顶就是右边第一个更高的人。",
    tags=["单调栈"],
    cases=["5\n2 1 5 3 4", "3\n3 2 1", "3\n1 2 3", "4\n5 5 5 5", "6\n1 3 2 5 4 6"],
    solve=c18)

# ---------------------------------------------------------------- C-19
def c19(t):
    d = t.split()
    n = int(d[0])
    seen = set()
    for x in d[1:1 + n]:
        if x in seen:
            return x
        seen.add(x)
    return "-1"


add(id="c-19", label="C-19", title="青云市集找重复摊位", difficulty=1,
    statement_md="市集有 n 个摊位，摊位号是 1 到 10^9 之间的整数，其中恰好有一个号出现了两次，其余各出现一次。请找出这个重复的号。",
    input_md="第一行一个整数 n（2 ≤ n ≤ 10^5）。\n第二行 n 个整数，表示各摊位号。",
    output_md="一个整数，表示重复出现的摊位号。",
    constraints_md="2 ≤ n ≤ 10^5，1 ≤ 摊位号 ≤ 10^9。",
    hint_md="边读边塞进 `unordered_set`，插入失败的那个就是答案。",
    tags=["哈希"],
    cases=["5\n1 2 3 2 4", "2\n7 7", "6\n1000000000 1 2 3 1000000000 4",
           "4\n9 8 7 9"],
    solve=c19)

# ---------------------------------------------------------------- C-20
def c20(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    h = []
    for x in a:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return str(h[0])


add(id="c-20", label="C-20", title="贵阳北站的第 k 高等候分", difficulty=2,
    statement_md="候车区有 n 位乘客，每人有一个等候分值。求第 k 高的分值（分值相同的按人数重复计算）。",
    input_md="第一行两个整数 n、k（1 ≤ k ≤ n ≤ 10^5）。\n第二行 n 个整数，表示每位乘客的分值（1 ≤ 分值 ≤ 10^9）。",
    output_md="一个整数，表示第 k 大的分值。",
    constraints_md="1 ≤ k ≤ n ≤ 10^5，1 ≤ 分值 ≤ 10^9。",
    hint_md="维护一个大小为 k 的小根堆，堆顶就是第 k 大。",
    tags=["堆", "第 k 大"],
    cases=["5 2\n3 1 4 1 5", "1 1\n1", "5 5\n5 4 3 2 1", "6 3\n1 1 1 2 2 2",
           "7 4\n10 9 8 7 6 5 4"],
    solve=c20)

# ---------------------------------------------------------------- C-21
def c21(t):
    d = t.split()
    p = 0
    n, m, q = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[ra] = rb

    for _ in range(m):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        union(u, v)
    out = []
    for _ in range(q):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        out.append("Yes" if find(u) == find(v) else "No")
    return "\n".join(out)


add(id="c-21", label="C-21", title="老小区的亲戚", difficulty=2,
    statement_md="老小区有 n 户人家，给出 m 条「两家是亲戚」的关系（亲戚关系可传递），再给出 q 次询问。每次询问两家是不是亲戚。",
    input_md="第一行三个整数 n、m、q（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ q ≤ 10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 与 v 是亲戚。\n接下来 q 行，每行两个整数 u、v，表示一次询问。",
    output_md="对每次询问输出一行：`Yes` 或 `No`。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ q ≤ 10^5。",
    hint_md="合并每条关系；询问时比较两个元素所在集合的根。",
    tags=["并查集"],
    cases=["5 3 4\n1 2\n2 3\n4 5\n1 3\n1 4\n3 2\n4 4", "3 0 2\n1 2\n2 3",
           "2 1 1\n1 2\n1 2", "6 4 3\n1 2\n3 4\n2 3\n5 6\n1 4\n5 6\n2 6"],
    solve=c21)

# ---------------------------------------------------------------- C-22
def c22(t):
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


add(id="c-22", label="C-22", title="地铁客流统计", difficulty=3,
    statement_md="线路上有 n 个站，初始客流都是 0。维护 q 次操作：\n`1 x v`：第 x 站的客流增加 v；\n`2 l r`：询问第 l 到第 r 站的客流之和。",
    input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 2×10^5）。\n接下来 q 行，每行是 `1 x v` 或 `2 l r`。",
    output_md="对每次 `2 l r` 询问输出一行，表示区间客流之和。",
    constraints_md="1 ≤ n, q ≤ 2×10^5；1 ≤ x ≤ n；1 ≤ l ≤ r ≤ n；1 ≤ v ≤ 10^9。",
    hint_md="单点修改 + 区间查询就是树状数组；区间和用两个前缀和相减。",
    tags=["树状数组"],
    cases=["5 4\n1 2 3\n2 1 5\n1 4 10\n2 2 4\n2 1 1", "1 2\n1 1 5\n2 1 1",
           "3 3\n2 1 3\n1 2 1\n2 1 3", "4 5\n1 1 1\n1 2 2\n1 3 3\n2 1 3\n2 2 4"],
    solve=c22)

# ---------------------------------------------------------------- C-23
def c23(t):
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
        if a != b:
            par[a] = b
    return str(len({find(i) for i in range(1, n + 1)}))


add(id="c-23", label="C-23", title="贵阳地铁有几片网", difficulty=2,
    statement_md="把已开通的站和相邻关系看成一个无向图。问这个图分成几个连通块（没有接进线网的孤立站各算一块）。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示 u 与 v 相邻。",
    output_md="一个整数，表示连通块个数。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
    hint_md="对每个没访问的点做一次 DFS/BFS，每开一次新搜索就多一块；也可以用并查集数根。",
    tags=["图", "连通块"],
    cases=["5 3\n1 2\n3 4\n4 5", "5 0", "4 3\n1 2\n2 3\n3 1", "6 2\n1 2\n4 5"],
    solve=c23)

# ---------------------------------------------------------------- C-24
def c24(t):
    d = t.split()
    p = 0
    n, m, s, e = int(d[p]), int(d[p + 1]), int(d[p + 2]), int(d[p + 3]); p += 4
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        dd, u = heapq.heappop(pq)
        if dd != dist[u]:
            continue
        for v, w in adj[u]:
            nd = dd + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return str(dist[e]) if dist[e] < INF else "-1"


add(id="c-24", label="C-24", title="从贵阳北站到青岩古镇", difficulty=3,
    statement_md="有 n 个路口、m 条双向道路，第 i 条道路需要 w[i] 分钟。求从 s 到 t 的最短时间；走不到输出 -1。",
    input_md="第一行四个整数 n、m、s、t（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9），表示一条双向道路。",
    output_md="一个整数，表示最短时间；走不到输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ w[i] ≤ 10^9。",
    hint_md="边权为正，用堆优化 Dijkstra，距离用 `long long`。",
    tags=["Dijkstra", "最短路"],
    cases=["5 6 1 5\n1 2 4\n1 3 2\n3 2 1\n2 4 5\n3 4 8\n4 5 1", "3 1 1 3\n1 2 5",
           "2 0 1 2", "6 8 1 6\n1 2 7\n1 3 9\n1 6 14\n2 3 10\n2 4 15\n3 4 11\n4 5 6\n5 6 9"],
    solve=c24)

# ---------------------------------------------------------------- C-25
def c25(t):
    d = t.split()
    p = 0
    n, m, s, e = int(d[p]), int(d[p + 1]), int(d[p + 2]), int(d[p + 3]); p += 4
    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    INF = float("inf")
    dist = [INF] * (n + 1)
    cnt = [0] * (n + 1)
    dist[s] = 0
    cnt[s] = 1
    pq = [(0, s)]
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
    return str(cnt[e] % MOD) if dist[e] < INF else "0"


add(id="c-25", label="C-25", title="有多少条一样快的路", difficulty=3,
    statement_md="有 n 个路口、m 条双向道路，第 i 条道路需要 w[i] 分钟。问从 s 到 t 有多少条路线用时恰好等于最短时间。答案对 10^9+7 取余。",
    input_md="第一行四个整数 n、m、s、t（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9）。",
    output_md="一个整数，表示最短路条数对 10^9+7 取余的结果；走不到输出 0。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ w[i] ≤ 10^9。",
    hint_md="Dijkstra 松弛时维护方案数：更短就覆盖，相等就累加。",
    tags=["最短路计数", "Dijkstra"],
    cases=["4 4 1 4\n1 2 1\n1 3 1\n2 4 1\n3 4 1", "3 2 1 3\n1 2 2\n2 3 2",
           "2 0 1 2", "5 6 1 5\n1 2 1\n1 3 1\n2 4 2\n3 4 2\n4 5 3\n2 5 4"],
    solve=c25)

# ---------------------------------------------------------------- C-26
def c26(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    edges = []
    for _ in range(m):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        edges.append((w, u, v))
    edges.sort()
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    total = 0
    used = 0
    for w, u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            par[a] = b
            total += w
            used += 1
            if used == n - 1:
                break
    return str(total) if used == n - 1 else "-1"


add(id="c-26", label="C-26", title="把区县都连起来", difficulty=3,
    statement_md="贵阳有 n 个区县要修公路全部连通，给出 m 条候选公路及其造价。求让所有区县连通的最小总造价；连不通输出 -1。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9），表示 u 与 v 之间修路的花费。",
    output_md="一个整数，表示最小总造价；无法连通输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ w ≤ 10^9。",
    hint_md="Kruskal：按造价排序边，用并查集判断成不成环。",
    tags=["最小生成树", "Kruskal"],
    cases=["4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n1 3 5", "3 1\n1 2 1", "2 1\n1 2 1000000000",
           "4 6\n1 2 1\n2 3 2\n3 4 3\n4 1 5\n1 3 4\n2 4 10"],
    solve=c26)

# ---------------------------------------------------------------- C-27
def c27(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        adj[v].append((u, w))

    def farthest(src):
        dist = [-1] * (n + 1)
        dist[src] = 0
        st = [src]
        far = src
        while st:
            u = st.pop()
            if dist[u] > dist[far]:
                far = u
            for v, w in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + w
                    st.append(v)
        return far, dist[far]

    a, _ = farthest(1)
    b, dd = farthest(a)
    return str(dd)


add(id="c-27", label="C-27", title="小区里最远的两栋楼", difficulty=3,
    statement_md="小区的道路网是一棵树：n 栋楼由 n-1 条带长度的小路连起来。求任意两栋楼之间最远的距离（树的直径）。",
    input_md="第一行一个整数 n（2 ≤ n ≤ 10^5）。\n接下来 n-1 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9），表示一条小路。",
    output_md="一个整数，表示最远距离。",
    constraints_md="2 ≤ n ≤ 10^5，1 ≤ w ≤ 10^9。",
    hint_md="从任意点出发找到最远的 A，再从 A 出发找到最远的 B，A 到 B 的距离就是答案。",
    tags=["树", "直径"],
    cases=["4\n1 2 1\n2 3 1\n3 4 1", "2\n1 2 5", "5\n1 2 2\n1 3 3\n2 4 4\n2 5 1",
           "6\n1 2 1\n2 3 1\n3 4 1\n4 5 1\n5 6 1"],
    solve=c27)

# ---------------------------------------------------------------- C-28
def c28(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    a = []
    for i in range(1, n + 1):
        a.append(list(map(int, d[p:p + i]))); p += i
    dp = a[-1][:]
    for i in range(n - 2, -1, -1):
        dp = [a[i][j] + max(dp[j], dp[j + 1]) for j in range(i + 1)]
    return str(dp[0])


add(id="c-28", label="C-28", title="高坡云顶的梯田", difficulty=2,
    statement_md="梯田第 i 行有 i 块，每块有一个收成值。从最上面一块出发，每步只能走到下一行正下方或右下方的块，一直走到最后一行。求能获得的最大收成之和。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 1000）。\n接下来 n 行，第 i 行有 i 个整数（0 ≤ 收成 ≤ 10^4）。",
    output_md="一个整数，表示最大收成之和。",
    constraints_md="1 ≤ n ≤ 1000，0 ≤ 收成 ≤ 10^4。",
    hint_md="从下往上递推：`dp[i][j] = a[i][j] + max(dp[i+1][j], dp[i+1][j+1])`。",
    tags=["动态规划", "数字三角形"],
    cases=["5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5", "1\n5", "2\n1\n2 3",
           "3\n1\n2 3\n4 5 6", "4\n0\n0 0\n0 0 0\n0 0 0 0"],
    solve=c28)

# ---------------------------------------------------------------- C-29
def c29(t):
    d = t.split()
    p = 0
    n, W = int(d[p]), int(d[p + 1]); p += 2
    dp = [0] * (W + 1)
    for _ in range(n):
        w, v = int(d[p]), int(d[p + 1]); p += 2
        for j in range(W, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return str(dp[W])


add(id="c-29", label="C-29", title="行李箱装纪念品", difficulty=2,
    statement_md="要从贵阳带回 n 件纪念品，第 i 件重 w[i] 克、价值 v[i]。行李箱最多装 W 克，每件最多带一件。求能带回的最大总价值。",
    input_md="第一行两个整数 n、W（1 ≤ n ≤ 1000，1 ≤ W ≤ 1000）。\n接下来 n 行，每行两个整数 w[i]、v[i]（1 ≤ w[i] ≤ W，1 ≤ v[i] ≤ 10^4）。",
    output_md="一个整数，表示最大总价值。",
    constraints_md="1 ≤ n ≤ 1000，1 ≤ W ≤ 1000。",
    hint_md="0-1 背包，一维数组要倒序枚举容量。",
    tags=["背包", "动态规划"],
    cases=["3 10\n5 10\n4 40\n6 30", "1 5\n6 100", "3 5\n1 1\n2 2\n3 3",
           "4 10\n2 3\n2 3\n2 3\n2 3", "2 1000\n1000 10000\n999 9999"],
    solve=c29)

# ---------------------------------------------------------------- C-30
def c30(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    coins = list(map(int, d[p:p + n]))
    INF = 10 ** 9
    dp = [INF] * (m + 1)
    dp[0] = 0
    for c in coins:
        for j in range(c, m + 1):
            if dp[j - c] + 1 < dp[j]:
                dp[j] = dp[j - c] + 1
    return str(dp[m]) if dp[m] < INF else "-1"


add(id="c-30", label="C-30", title="公交售票机找零", difficulty=3,
    statement_md="售票机有 n 种面值的硬币，每种面值都有无限多枚。要凑出 m 元，最少需要几枚硬币？凑不出输出 -1。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 100，1 ≤ m ≤ 10^5）。\n第二行 n 个整数，表示每种硬币的面值（1 ≤ 面值 ≤ 10^5）。",
    output_md="一个整数，表示最少硬币数；凑不出输出 -1。",
    constraints_md="1 ≤ n ≤ 100，1 ≤ m ≤ 10^5。",
    hint_md="完全背包求最小值：`dp[0]=0`，其余为无穷大，容量正序枚举。",
    tags=["完全背包"],
    cases=["2 10\n5 2", "3 7\n1 2 5", "2 3\n2 4", "1 100000\n1", "4 27\n2 5 7 11"],
    solve=c30)

# ---------------------------------------------------------------- C-31
def c31(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    INF = 10 ** 18
    dp = [[0] * n for _ in range(n)]
    for L in range(2, n + 1):
        for l in range(0, n - L + 1):
            r = l + L - 1
            best = INF
            s = pre[r + 1] - pre[l]
            for k in range(l, r):
                v = dp[l][k] + dp[k + 1][r]
                if v < best:
                    best = v
            dp[l][r] = best + s
    return str(dp[0][n - 1])


add(id="c-31", label="C-31", title="花溪河边的石头", difficulty=3,
    statement_md="河边有 n 堆石头排成一行，每次可以把相邻两堆合并成一堆，代价是这两堆石头数之和。一直合并到只剩一堆，求最小总代价。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 300）。\n第二行 n 个整数，表示每堆石头数（1 ≤ 每堆 ≤ 10^4）。",
    output_md="一个整数，表示最小总代价。",
    constraints_md="1 ≤ n ≤ 300，1 ≤ 每堆 ≤ 10^4。",
    hint_md="区间 DP：先枚举区间长度，再枚举断点，区间和用前缀和。",
    tags=["区间 DP"],
    cases=["4\n1 3 5 2", "1\n5", "2\n1 1", "5\n1 2 3 4 5", "6\n4 1 2 3 5 6"],
    solve=c31)

# ---------------------------------------------------------------- C-32
def c32(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    tails = []
    for x in a:
        i = bisect_right(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return str(len(tails))


add(id="c-32", label="C-32", title="连续的好天气", difficulty=3,
    statement_md="给出连续 n 天的气温，求最长的不下降子序列长度。子序列不要求连续，只要保持原来的先后顺序；相邻元素允许相等。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数，表示每天的气温（1 ≤ 气温 ≤ 10^9）。",
    output_md="一个整数，表示最长不下降子序列的长度。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ 气温 ≤ 10^9。",
    hint_md="`dp` 记「长度为 i 的不下降子序列结尾的最小值」，用 `upper_bound` 找位置。",
    tags=["LIS", "二分"],
    cases=["6\n1 5 3 4 6 2", "1\n7", "5\n5 4 3 2 1", "5\n1 2 3 4 5", "6\n2 2 2 2 2 2",
           "8\n3 1 2 2 4 3 5 5"],
    solve=c32)

# ---------------------------------------------------------------- C-33
def c33(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    allow = []
    for _ in range(m):
        k = int(d[p]); p += 1
        mask = 0
        for _ in range(k):
            mask |= 1 << (int(d[p]) - 1); p += 1
        allow.append(mask)
    size = 1 << n
    MOD = 1000000007
    dp = [0] * size
    dp[0] = 1
    for v in range(m):
        ndp = dp[:]
        for mask in range(size):
            if dp[mask] == 0:
                continue
            avail = allow[v] & ~mask
            while avail:
                bit = avail & -avail
                avail -= bit
                ndp[mask | bit] = (ndp[mask | bit] + dp[mask]) % MOD
        dp = ndp
    return str(dp[size - 1] % MOD)


add(id="c-33", label="C-33", title="数博会排班", difficulty=3,
    statement_md="数博会有 n 个岗位、m 名志愿者，每名志愿者能胜任其中若干岗位。每个岗位恰好安排 1 人，每名志愿者最多安排 1 个岗位。问一共有多少种排班方案（对 10^9+7 取余）。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ m ≤ 20）。\n接下来 m 行，每行先是一个整数 k，随后 k 个整数，表示这名志愿者能胜任的岗位编号（从 1 开始）。",
    output_md="一个整数，表示方案数对 10^9+7 取余的结果。",
    constraints_md="1 ≤ n ≤ m ≤ 20，0 ≤ k ≤ n。",
    hint_md="用二进制表示「哪些岗位已排满」，`dp[mask]` 表示排满 mask 的方案数，按已用人数转移到下一个人。",
    tags=["状压 DP"],
    cases=["2 2\n1 1\n1 2", "2 3\n2 1 2\n1 1\n1 2", "1 1\n1 1",
           "3 3\n3 1 2 3\n3 1 2 3\n3 1 2 3", "2 2\n1 1\n1 1"],
    solve=c33)

# ---------------------------------------------------------------- C-34
def c34(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    dp = [0] * (n + 1)
    dp[1] = a[0]
    dq = deque([1])
    for i in range(2, n + 1):
        while dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = a[i - 1] + dp[dq[0]]
        while dq and dp[dq[-1]] >= dp[i]:
            dq.pop()
        dq.append(i)
    return str(dp[n])


add(id="c-34", label="C-34", title="检修车跳站", difficulty=3,
    statement_md="检修车从 1 号站开到 n 号站，每次最多向前跳 k 站，每落到一站都要付出该站的检修时间 a[i]（起点和终点也要付）。求最小总时间。",
    input_md="第一行两个整数 n、k（1 ≤ k ≤ n ≤ 10^5）。\n第二行 n 个整数 a[1..n]（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示最小总时间。",
    constraints_md="1 ≤ k ≤ n ≤ 10^5，1 ≤ a[i] ≤ 10^9。",
    hint_md="`dp[i] = a[i] + min(dp[i-k..i-1])`，用单调队列维护窗口最小值。",
    tags=["DP 优化", "单调队列"],
    cases=["5 2\n1 2 3 4 5", "3 3\n5 1 5", "1 1\n7", "6 3\n10 1 1 1 1 10",
           "10 4\n3 1 4 1 5 9 2 6 5 3"],
    solve=c34)

# ---------------------------------------------------------------- C-35
def c35(t):
    lines = t.rstrip("\n").split("\n")
    s = lines[0].strip()
    p = lines[1].strip() if len(lines) > 1 else ""
    if not p:
        return "0"
    nxt = [0] * len(p)
    j = 0
    for i in range(1, len(p)):
        while j and p[i] != p[j]:
            j = nxt[j - 1]
        if p[i] == p[j]:
            j += 1
        nxt[i] = j
    cnt = 0
    j = 0
    for ch in s:
        while j and ch != p[j]:
            j = nxt[j - 1]
        if ch == p[j]:
            j += 1
        if j == len(p):
            cnt += 1
            j = nxt[j - 1]
    return str(cnt)


add(id="c-35", label="C-35", title="贵阳地名检索", difficulty=3,
    statement_md="给出文本 T 和模式串 P，统计 P 在 T 中出现的次数（允许重叠）。",
    input_md="第一行一个字符串 T。\n第二行一个字符串 P。\n两个串都只含小写字母，长度不超过 10^6。",
    output_md="一个整数，表示 P 在 T 中出现的次数（可重叠）。",
    constraints_md="1 ≤ |T|, |P| ≤ 10^6。",
    hint_md="KMP：匹配到末尾后把 j 回退到 `next[j]`，这样重叠也能继续数。",
    tags=["KMP", "字符串"],
    cases=["qianlingshan\nqianling", "aaaaa\naa", "abc\nabc", "abc\nd", "abababa\naba",
           "jiaxiulouhuaxi\nxiu"],
    solve=c35)

# ---------------------------------------------------------------- C-36
def c36(t):
    a, b, p = map(int, t.split()[:3])
    return str(pow(a, b, p) if p > 1 else 0)


add(id="c-36", label="C-36", title="数博会的加密展台", difficulty=2,
    statement_md="计算 a 的 b 次方对 p 取余的结果。约定 0 的 0 次方等于 1。",
    input_md="一行三个整数 a、b、p（0 ≤ a ≤ 10^9，0 ≤ b ≤ 10^18，1 ≤ p ≤ 10^9）。",
    output_md="一个整数，表示 a^b mod p。",
    constraints_md="0 ≤ a ≤ 10^9，0 ≤ b ≤ 10^18，1 ≤ p ≤ 10^9。",
    hint_md="把指数按二进制拆开，底数不断平方；注意 `b=0` 时答案是 1。",
    tags=["快速幂"],
    cases=["2 10 1000", "0 0 7", "3 0 5", "0 5 11", "123456789 1000000000000000000 1000000007",
           "2 62 1000000007"],
    solve=c36)

# ---------------------------------------------------------------- C-37
def c37(t):
    n = int(t.split()[0])
    if n < 2:
        return "0"
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if sieve[i]:
            sieve[i * i::i] = b"\x00" * (((n - i * i) // i) + 1)
        i += 1
    return str(sum(sieve))


add(id="c-37", label="C-37", title="胸牌编号里的素数", difficulty=2,
    statement_md="1 到 n 每名志愿者有一块胸牌，编号从 1 到 n。问编号是素数的胸牌有几块。",
    input_md="一个整数 n（1 ≤ n ≤ 10^7）。",
    output_md="一个整数，表示 1 到 n 中素数的个数。",
    constraints_md="1 ≤ n ≤ 10^7。",
    hint_md="线性筛或埃氏筛预处理到 n，再数标记。",
    tags=["数论", "筛法"],
    cases=["10", "1", "2", "100", "1000000", "10000000"],
    solve=c37)

# ---------------------------------------------------------------- C-38
def c38(t):
    n, m = map(int, t.split()[:2])
    MOD = 1000000007
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    a = fact[n]
    b = pow(fact[m], MOD - 2, MOD)
    c = pow(fact[n - m], MOD - 2, MOD)
    return str(a * b % MOD * c % MOD)


add(id="c-38", label="C-38", title="丝娃娃选菜", difficulty=3,
    statement_md="有 n 样菜，从中选 m 样包进丝娃娃，不计顺序。问有多少种选法，答案对 10^9+7 取余。",
    input_md="一行两个整数 n、m（1 ≤ m ≤ n ≤ 10^6）。",
    output_md="一个整数，表示 C(n, m) 对 10^9+7 取余的结果。",
    constraints_md="1 ≤ m ≤ n ≤ 10^6。",
    hint_md="预处理阶乘和阶乘逆元，逆元用费马小定理。",
    tags=["组合数", "逆元"],
    cases=["5 2", "10 3", "10 7", "1 1", "1000000 500000", "6 0"],
    solve=c38)

# ---------------------------------------------------------------- C-39
def c39(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    x = 0
    ones = 0
    for v in a:
        x ^= v
        ones += bin(v).count("1")
    return "%d\n%d" % (x, ones)


add(id="c-39", label="C-39", title="机房的权限位", difficulty=1,
    statement_md="机房的每个权限用一个不超过 10^18 的整数表示（二进制中为 1 的位表示拥有该权限）。给出 n 个权限整数，输出它们按位异或的结果，以及所有整数二进制中 1 的总个数。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（0 ≤ 整数 ≤ 10^18）。",
    output_md="两行：第一行为异或结果，第二行为所有整数中 1 的总个数。",
    constraints_md="1 ≤ n ≤ 10^5，0 ≤ a[i] ≤ 10^18。",
    hint_md="异或直接累异或；数 1 可以用 `__builtin_popcountll`，或者 `x &= x - 1` 反复消最低位的 1。",
    tags=["位运算"],
    cases=["3\n1 2 4", "1\n0", "4\n7 7 7 7", "4\n12 0 5 9", "2\n1000000000000000000 1"],
    solve=c39)

# ---------------------------------------------------------------- C-40
def c40(t):
    lines = t.strip().splitlines()
    a = int(lines[0])
    b = int(lines[1])
    return str(a + b)


add(id="c-40", label="C-40", title="一百位的胸牌号", difficulty=2,
    statement_md="胸牌号可能很长，要把两个这样的正整数相加。",
    input_md="两行，每行一个不超过 1000 位、没有前导零的十进制正整数。",
    output_md="一行，表示两个数的和（十进制，无前导零）。",
    constraints_md="1 ≤ 位数 ≤ 1000。",
    hint_md="两个数倒着存，从低位往高位逐位相加并处理进位；也可以直接用高精度库。",
    tags=["高精度"],
    cases=["12345678901234567890\n9876543210987654321", "1\n1", "999\n1",
           "1000\n9000", "1" + "0" * 999 + "\n" + "9" * 1000],
    solve=c40)
