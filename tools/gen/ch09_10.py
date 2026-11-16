#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 9～10 章可编程习题。"""
PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 9 章
def p0901(t):
    n = int(t.split()[0])
    r = 1
    for i in range(2, n + 1):
        r *= i
    return str(r)


add(id="p-09-01", chapter=9, label="习题 9-1", title="递归求阶乘",
    difficulty=1,
    statement_md="写一个递归函数求 n 的阶乘（n ≤ 20），并说明终止条件为什么必须是 n == 0 或 n == 1。\n\n本题是第 9 章习题 1。",
    input_md="一个整数 n（0 ≤ n ≤ 20）。",
    output_md="一个整数，表示 n!（规定 0! = 1）。",
    constraints_md="0 ≤ n ≤ 20，20! = 2432902008176640000，在 `long long` 范围内。",
    hint_md="`f(0)=f(1)=1`，否则 `f(n)=n*f(n-1)`。",
    tags=["递归"],
    cases=["0", "1", "5", "10", "20"],
    solve=p0901)

def p0902(t):
    d = t.split()
    a, n = int(d[0]), int(d[1])
    MOD = 1000000007
    return str(pow(a, n, MOD))


add(id="p-09-02", chapter=9, label="习题 9-2", title="递归快速幂",
    difficulty=2,
    statement_md="写一个递归函数求 a^n（快速幂的递归版），要求时间复杂度是 O(log n)，并指出它的递归深度是多少。\n\n本题是第 9 章习题 2。为了便于评测，结果对 10^9+7 取余。",
    input_md="一行两个整数 a、n（0 ≤ a ≤ 10^9，0 ≤ n ≤ 10^18）。",
    output_md="一个整数，表示 a^n mod 10^9+7（规定 0^0 = 1）。",
    constraints_md="0 ≤ a ≤ 10^9，0 ≤ n ≤ 10^18。",
    hint_md="`n` 为偶数时 `a^n = (a^(n/2))²`，为奇数时 `a^n = a * a^(n-1)`；递归深度 O(log n)。",
    tags=["递归", "快速幂"],
    cases=["2 10", "0 0", "3 0", "5 1000000000000000000", "123456789 7"],
    solve=p0902)

def p0903(t):
    d = t.split()
    n = int(d[0])
    a = sorted(map(int, d[1:1 + n]))
    out = []
    used = [False] * n
    cur = []

    def dfs():
        if len(cur) == n:
            out.append(" ".join(map(str, cur)))
            return
        for i in range(n):
            if used[i]:
                continue
            if i > 0 and a[i] == a[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            cur.append(a[i])
            dfs()
            cur.pop()
            used[i] = False

    dfs()
    return "\n".join(out)


add(id="p-09-03", chapter=9, label="习题 9-3", title="全排列",
    difficulty=2,
    statement_md="给 n 个不同的整数，用递归输出它们的所有排列。\n\n本题是第 9 章习题 3：把「已经选了哪些数」当成参数往下传，选满 n 个就输出一组。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 8）。\n第二行 n 个互不相同的整数（1 ≤ a[i] ≤ 100）。",
    output_md="共 n! 行，每行 n 个整数，按字典序升序输出所有排列。",
    constraints_md="1 ≤ n ≤ 8。",
    hint_md="DFS 加一个 `used` 数组；每层按从小到大尝试，得到的顺序天然是字典序。",
    tags=["递归", "DFS"],
    cases=["1\n5", "2\n2 1", "3\n1 2 3", "3\n3 1 2"],
    solve=p0903)

# ================================================================ 第 10 章
def p1001(t):
    d = t.split()
    n, m = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    b = list(map(int, d[2 + n:2 + n + m]))
    i = j = 0
    out = []
    while i < n and j < m:
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return " ".join(map(str, out))


add(id="p-10-01", chapter=10, label="习题 10-1", title="合并两个有序数组",
    difficulty=1,
    statement_md="给两个已经从小到大排好的数组，输出合并后仍然有序的数组。要求用两个指针，时间复杂度 O(n+m)，不要用 `sort`。\n\n本题是第 10 章习题 1。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 10^5）。\n第二行 n 个非降序整数。\n第三行 m 个非降序整数。",
    output_md="一行 n+m 个整数，为合并后的非降序序列，相邻两数用一个空格隔开。",
    constraints_md="1 ≤ n, m ≤ 10^5，1 ≤ 元素 ≤ 10^9。",
    hint_md="两个指针各指一个数组，每次取较小的放进答案；一个数组取完后把另一个剩下的全部接上。",
    tags=["双指针", "归并"],
    cases=["3 4\n1 3 5\n2 4 6 8", "1 1\n1\n2", "3 3\n1 2 3\n1 2 3",
           "2 2\n5 6\n1 2"],
    solve=p1001)

def p1003(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    tmp = [0] * n

    def inv_count(l, r):
        if r - l <= 1:
            return 0
        mid = (l + r) // 2
        cnt = inv_count(l, mid) + inv_count(mid, r)
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

    inv = inv_count(0, n) if n > 0 else 0
    # 相等对
    eq = 0
    b = sorted(a)
    i = 0
    while i < n:
        j = i + 1
        while j < n and b[j] == b[i]:
            j += 1
        c = j - i
        eq += c * (c - 1) // 2
        i = j
    total = n * (n - 1) // 2
    return str(total - inv - eq)


add(id="p-10-03", chapter=10, label="习题 10-3", title="顺序对计数",
    difficulty=2,
    statement_md="求「顺序对」的个数：满足 i < j 且 a[i] < a[j] 的数对。并说明它和逆序对的数量有什么关系。\n\n本题是第 10 章习题 3。提示：所有数对 = 顺序对 + 逆序对 + 相等对。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示顺序对个数。",
    constraints_md="1 ≤ n ≤ 10^5，答案可能超过 `int`，用 `long long`。",
    hint_md="用归并排序求逆序对，再统计相等对，`n*(n-1)/2` 减去这两项就是顺序对。",
    tags=["分治", "逆序对"],
    cases=["5\n1 2 3 4 5", "5\n5 4 3 2 1", "4\n1 1 2 2", "3\n1 2 1",
           "6\n3 1 2 2 4 3"],
    solve=p1003)

def p1004(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    a.sort(reverse=True)
    return str(a[k - 1])


add(id="p-10-04", chapter=10, label="习题 10-4", title="第 k 大",
    difficulty=2,
    statement_md="给 n 个整数，求第 k 大的数。要求用快速选择实现，并说明它和第 k 小之间怎么换算。\n\n本题是第 10 章习题 4。第 k 大指从大到小排第 k 个。",
    input_md="第一行两个整数 n、k（1 ≤ k ≤ n ≤ 10^5）。\n第二行 n 个互不相同的整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示第 k 大的数。",
    constraints_md="1 ≤ k ≤ n ≤ 10^5，元素互不相同。",
    hint_md="快速选择每次只递归含目标下标的那一半，期望 O(n)；第 k 大等于第 `n-k+1` 小。",
    tags=["快速选择", "分治"],
    cases=["5 3\n5 1 4 2 3", "1 1\n7", "5 1\n5 4 3 2 1", "5 5\n5 4 3 2 1",
           "6 2\n10 9 8 7 6 5"],
    solve=p1004)
