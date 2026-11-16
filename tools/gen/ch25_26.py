#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 25～26 章可编程习题。"""
PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 25 章
def p2501(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    INF = 10 ** 18
    f = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = INF
            for k in range(i, j):
                v = f[i][k] + f[k + 1][j]
                if v < best:
                    best = v
            f[i][j] = best + pre[j + 1] - pre[i]
    return str(f[0][n - 1])


add(id="p-25-01", chapter=25, label="习题 25-1", title="石子合并（最小代价）",
    difficulty=2,
    statement_md="n 堆石子排成一排，每次只能把相邻两堆合并，代价是这两堆石子数之和。把所有石子合并成一堆，求最小总代价。\n\n本题是第 25 章习题 1：区间 DP，`f[i][j]` 表示把 i..j 合并成一堆的最小代价。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 300）。\n第二行 n 个整数（1 ≤ 石子数 ≤ 10^5）。",
    output_md="一个整数，表示最小总代价。",
    constraints_md="1 ≤ n ≤ 300，答案用 `long long`。",
    hint_md="`f[i][j] = min(f[i][k] + f[k+1][j]) + sum(i..j)`，按区间长度从小到大递推；前缀和算区间和。",
    tags=["区间 DP"],
    cases=["4\n1 3 5 2", "1\n7", "3\n1 2 3", "5\n4 1 3 2 6"],
    solve=p2501)

def p2502(t):
    s = t.strip()
    n = len(s)
    ans = 1
    for center in range(n):
        l, r = center, center
        while l >= 0 and r < n and s[l] == s[r]:
            ans = max(ans, r - l + 1)
            l -= 1
            r += 1
        l, r = center, center + 1
        while l >= 0 and r < n and s[l] == s[r]:
            ans = max(ans, r - l + 1)
            l -= 1
            r += 1
    return str(ans)


add(id="p-25-02", chapter=25, label="习题 25-2", title="最长回文子串",
    difficulty=2,
    statement_md="给定一个只含小写字母的字符串，求最长回文子串的长度。先写 O(n²) 的中心扩展，再查一下 Manacher 是怎么把复杂度降到 O(n) 的。\n\n本题是第 25 章习题 2。",
    input_md="一行一个字符串，长度不超过 2000，只含小写字母。",
    output_md="一个整数，表示最长回文子串长度。",
    constraints_md="1 ≤ 长度 ≤ 2000。",
    hint_md="回文中心有两种：一个字符（奇数长度）和两个字符之间（偶数长度），两种都要试。",
    tags=["字符串", "回文"],
    cases=["abacaba", "a", "abba", "abcde", "aaaa"],
    solve=p2502)

def p2503(t):
    s = t.strip()
    n = len(s)
    f = [[0] * n for _ in range(n)]
    for i in range(n):
        f[i][i] = 1
    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            best = f[i + 1][j] + 1
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    v = (f[i + 1][k - 1] if k - 1 >= i + 1 else 0) + f[k][j]
                    if v < best:
                        best = v
            f[i][j] = best
    return str(f[0][n - 1])


add(id="p-25-03", chapter=25, label="习题 25-3", title="涂色（区间覆盖问题）",
    difficulty=3,
    statement_md="有一排 n 个格子，初始都是空白。每次操作可以把一段连续格子涂成同一个颜色（后涂的会覆盖前面的）。给定目标花色序列，问最少几步能涂成目标。\n\n本题是第 25 章习题 3（书上叫「涂色」）。注意：如果 s[i] == s[j]，说明 i 和 j 可以一起涂，`f[i][j] = f[i+1][j]`。",
    input_md="一行一个字符串，长度不超过 200，只含大写字母。",
    output_md="一个整数，表示最少涂色次数。",
    constraints_md="1 ≤ 长度 ≤ 200。",
    hint_md="`f[i][j]` 表示涂好 i..j 的最少步数；先特判 `s[i]==s[j]`，再枚举断点 k。",
    tags=["区间 DP"],
    cases=["AAABBB", "A", "ABA", "ABCBA", "ABCD"],
    solve=p2503)

def p2504(t):
    s = t.strip()
    st = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == "(":
            st.append(i)
        else:
            st.pop()
            if not st:
                st.append(i)
            else:
                best = max(best, i - st[-1])
    return str(best)


add(id="p-25-04", chapter=25, label="习题 25-4", title="最长有效括号子串",
    difficulty=2,
    statement_md="给定一个只含 `(` 和 `)` 的字符串，求最长的「括号匹配」子串长度（子串里每个左括号都有对应的右括号，且嵌套正确）。\n\n本题是第 25 章习题 4。",
    input_md="一行一个字符串，长度不超过 10^5。",
    output_md="一个整数，表示最长有效括号子串的长度。",
    constraints_md="1 ≤ 长度 ≤ 10^5。",
    hint_md="用栈存下标，栈底先放 -1：遇 `(` 压栈；遇 `)` 先弹栈，若栈空就把当前下标压入作为新的左边界，否则用 `i - 栈顶` 更新答案。",
    tags=["字符串", "栈"],
    cases=["(()", ")()())", ")(", "()(()", "((()))"],
    solve=p2504)

def p2505(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    a2 = a + a
    pre = [0] * (2 * n + 1)
    for i in range(2 * n):
        pre[i + 1] = pre[i] + a2[i]
    INF = 10 ** 18
    ans = INF
    f = [[0] * (2 * n) for _ in range(2 * n)]
    for length in range(2, n + 1):
        for i in range(0, 2 * n - length + 1):
            j = i + length - 1
            best = INF
            for k in range(i, j):
                v = f[i][k] + f[k + 1][j]
                if v < best:
                    best = v
            f[i][j] = best + pre[j + 1] - pre[i]
    for i in range(n):
        ans = min(ans, f[i][i + n - 1])
    return str(ans)


add(id="p-25-05", chapter=25, label="习题 25-5", title="环形石子合并",
    difficulty=3,
    statement_md="把第 25 章习题 1 的石子改成围成一圈：每次只能合并相邻两堆（首尾也算相邻），求合并成一堆的最小总代价。提示：把数组复制一份接在后面，就变成在长度 2n 的链上求长度为 n 的区间。\n\n本题是第 25 章习题 5。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 100）。\n第二行 n 个整数（1 ≤ 石子数 ≤ 10^5）。",
    output_md="一个整数，表示最小总代价。",
    constraints_md="1 ≤ n ≤ 100。",
    hint_md="断环成链：`a2 = a + a`，答案是所有 `f[i][i+n-1]`（i = 0..n-1）中的最小值。",
    tags=["区间 DP", "环形"],
    cases=["4\n1 3 5 2", "1\n7", "3\n1 2 3", "5\n4 1 3 2 6"],
    solve=p2505)

# ================================================================ 第 26 章
def p2601(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    val = [0] * (n + 1)
    for i in range(1, n + 1):
        val[i] = int(d[p]); p += 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = int(d[p]), int(d[p + 1]); p += 2
        adj[u].append(v)
        adj[v].append(u)
    par = [0] * (n + 1)
    order = [1]
    for u in order:
        for v in adj[u]:
            if v != par[u]:
                par[v] = u
                order.append(v)
    dp0 = [0] * (n + 1)
    dp1 = [0] * (n + 1)
    for u in reversed(order):
        dp1[u] = val[u]
        for v in adj[u]:
            if par[v] == u:
                dp1[u] += dp0[v]
                dp0[u] += max(dp0[v], dp1[v])
    return str(dp1[1])


add(id="p-26-01", chapter=26, label="习题 26-1", title="树上独立集（根必须选）",
    difficulty=2,
    statement_md="把例题 26-1 改成「必须选大老板（根结点）参加」，其余条件不变（相邻的两点不能同时选，每个点有一个开心值，求最大总开心值）。\n\n本题是第 26 章习题 1。先想：如果根必须选，儿子们的状态只剩下「不选」一种，代码哪一行可以省掉？",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数，表示每个点的开心值（1 ≤ 值 ≤ 10^4）。\n接下来 n-1 行，每行两个整数 u、v，表示一条边，1 号点是根。",
    output_md="一个整数，表示最大总开心值（根必须被选）。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="`dp1[u] = a[u] + Σ dp0[v]`；因为根必须选，答案直接取 `dp1[1]`（不是 max）。",
    tags=["树形 DP"],
    cases=["5\n1 2 3 4 5\n1 2\n1 3\n2 4\n2 5", "1\n10", "4\n5 5 5 5\n1 2\n2 3\n3 4",
           "6\n3 1 4 1 5 9\n1 2\n1 3\n3 4\n3 5\n5 6"],
    solve=p2601)

def p2602(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v, w = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    par = [0] * (n + 1)
    order = [1]
    for u in order:
        for v, w in adj[u]:
            if v != par[u]:
                par[v] = u
                order.append(v)
    down1 = [0] * (n + 1)
    down2 = [0] * (n + 1)
    ans = 0
    for u in reversed(order):
        for v, w in adj[u]:
            if par[v] == u:
                cand = down1[v] + w
                if cand > down1[u]:
                    down2[u] = down1[u]
                    down1[u] = cand
                elif cand > down2[u]:
                    down2[u] = cand
        ans = max(ans, down1[u] + down2[u])
    return str(ans)


add(id="p-26-02", chapter=26, label="习题 26-2", title="树的直径（树形 DP 版）",
    difficulty=2,
    statement_md="用树形 DP 求带权树的直径：对每个点维护「往子树里走的最长链 down1」和「第二长链 down2」，答案取所有点 `down1 + down2` 的最大值。写完跟第 22 章的两次遍历版本对拍。\n\n本题是第 26 章习题 2。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n-1 行，每行三个整数 u、v、w（1 ≤ w ≤ 10^9），表示一条带权边。",
    output_md="一个整数，表示树的直径（最长路径的边权和）。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ w ≤ 10^9，答案用 `long long`。",
    hint_md="自底向上：儿子返回 `down1[v]+w`，用它更新父亲的 down1/down2；每个点处用 down1+down2 更新全局答案。",
    tags=["树形 DP", "直径"],
    cases=["5\n1 2 3\n2 3 4\n2 4 5\n4 5 6", "1", "2\n1 2 10", "6\n1 2 1\n2 3 2\n3 4 3\n4 5 4\n5 6 5"],
    solve=p2602)

def p2603(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    par = [0] * (n + 1)
    credit = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        par[i] = int(d[p]); credit[i] = int(d[p + 1]); p += 2
        children[par[i]].append(i)

    NEG = -10 ** 18
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    sz = [0] * (n + 1)
    order = [0]
    for u in order:
        for v in children[u]:
            order.append(v)

    for u in reversed(order):
        dp[u][0] = 0
        if u != 0:
            dp[u][1] = credit[u]
            sz[u] = 1
        for v in children[u]:
            ndp = [NEG] * (m + 1)
            for i in range(0, min(sz[u], m) + 1):
                if dp[u][i] == NEG:
                    continue
                for j in range(0, min(sz[v], m - i) + 1):
                    if dp[v][j] == NEG:
                        continue
                    if dp[u][i] + dp[v][j] > ndp[i + j]:
                        ndp[i + j] = dp[u][i] + dp[v][j]
            dp[u] = ndp
            sz[u] = min(m, sz[u] + sz[v])

    return str(dp[0][m])


add(id="p-26-03", chapter=26, label="习题 26-3", title="选课（树上背包）",
    difficulty=3,
    statement_md="n 门课，每门课有学分，每门课最多有一门先修课，先修关系是一棵树（森林加一个虚拟 0 号根）。要选 m 门课，且选了某门课就必须选它的先修课，求最大学分。\n\n本题是第 26 章习题 3：`dp[u][j]` 表示「u 的子树里选 j 门且 u 必选」的最大收益。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 100，1 ≤ m ≤ n）。\n接下来 n 行，第 i 行两个整数 p、w：p 是 i 的先修课（0 表示没有），w 是 i 的学分（1 ≤ w ≤ 10^4）。",
    output_md="一个整数，表示选 m 门课能得到的最大总学分。",
    constraints_md="1 ≤ n ≤ 100，1 ≤ m ≤ n。",
    hint_md="`dp[u][0]=0` 表示子树里一个都不选，`dp[u][1]=credit[u]` 表示选 u；把儿子的 dp 按大小限制合并成树上背包，答案取 `dp[0][m]`（0 是虚拟根）。",
    tags=["树形 DP", "树上背包"],
    cases=["3 2\n0 1\n1 2\n1 3", "3 1\n0 5\n0 6\n0 7", "5 3\n0 2\n1 3\n1 4\n2 5\n2 6",
           "4 4\n0 1\n1 2\n2 3\n3 4"],
    solve=p2603)

def p2604(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    allowed = []
    for _ in range(n):
        k = int(d[p]); p += 1
        mask = 0
        for _ in range(k):
            mask |= 1 << (int(d[p]) - 1)
            p += 1
        allowed.append(mask)
    NEG = -10 ** 9
    dp = [NEG] * (1 << m)
    dp[0] = 0
    for mask_allowed in allowed:
        ndp = dp[:]
        for used in range(1 << m):
            if dp[used] == NEG:
                continue
            free = mask_allowed & ~used
            sub = free
            while True:
                v = dp[used] + bin(sub).count("1")
                if v > ndp[used | sub]:
                    ndp[used | sub] = v
                if sub == 0:
                    break
                sub = (sub - 1) & free
        dp = ndp
    return str(max(dp))


add(id="p-26-04", chapter=26, label="习题 26-4", title="除草（状压 DP）",
    difficulty=3,
    statement_md="一块 n 行 m 列的草地，有 n 个工人，第 i 个工人负责第 i 行，他能除哪些列的草是给定的。要求任何一列不能有两个人同时除，问最多能除多少列。\n\n本题是第 26 章习题 4：把「已经用掉哪些列」压成一个 mask，逐行转移，下一行的选择必须是本行可用列的子集、且与已用列不重叠。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10，1 ≤ m ≤ 10）。\n接下来 n 行，每行先一个整数 k，再 k 个整数表示这一行工人能除的列（1 ≤ 列 ≤ m）。",
    output_md="一个整数，表示最多能除的列数。",
    constraints_md="1 ≤ n ≤ 10，1 ≤ m ≤ 10。",
    hint_md="`dp[mask]` 表示已除列集合为 mask 时的最大列数；枚举行内可用的子集时用 `sub = (sub-1) & free` 快速枚举。",
    tags=["状压 DP"],
    cases=["2 3\n2 1 2\n2 2 3", "1 2\n2 1 2", "3 2\n1 1\n1 2\n2 1 2", "2 4\n3 1 2 3\n2 2 4"],
    solve=p2604)

def p2605(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    dist = []
    for _ in range(n):
        dist.append(list(map(int, d[p:p + n])))
        p += n
    INF = 10 ** 18
    full = 1 << n
    dp = [[INF] * n for _ in range(full)]
    dp[1][0] = 0
    for mask in range(full):
        for i in range(n):
            cur = dp[mask][i]
            if cur == INF or not (mask >> i) & 1:
                continue
            for j in range(n):
                if not (mask >> j) & 1:
                    nm = mask | (1 << j)
                    v = cur + dist[i][j]
                    if v < dp[nm][j]:
                        dp[nm][j] = v
    return str(min(dp[full - 1][i] + dist[i][0] for i in range(n)))


add(id="p-26-05", chapter=26, label="习题 26-5", title="数博会巡场（TSP）",
    difficulty=3,
    statement_md="n 个展馆和一个距离矩阵，从 0 号展馆出发，把所有展馆都走一遍，最后回到 0 号，求最短总路程。\n\n本题是第 26 章习题 5：`dp[mask][i]` 表示「已经走过 mask 这些展馆、最后停在 i」的最短路程；若还要输出路线，就再开一个 `pre[mask][i]` 记录从哪来。本题只要求输出长度。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 15）。\n接下来 n 行，每行 n 个整数，表示距离矩阵（对角线为 0，其余 1 ≤ 距离 ≤ 10^6）。",
    output_md="一个整数，表示最短回路总路程。",
    constraints_md="1 ≤ n ≤ 15。",
    hint_md="从 `mask = 1、停在 0` 出发，枚举下一个没走过的点转移；答案是 `min(dp[全集][i] + d[i][0])`。",
    tags=["状压 DP", "TSP"],
    cases=["3\n0 2 9\n2 0 5\n9 5 0", "1\n0", "2\n0 7\n7 0",
           "4\n0 1 9 8\n1 0 3 7\n9 3 0 2\n8 7 2 0"],
    solve=p2605)
