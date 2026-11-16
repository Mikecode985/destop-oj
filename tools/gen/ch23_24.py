#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 23～24 章可编程习题。"""
from bisect import bisect_right

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 23 章
def p2301(t):
    n = int(t.split()[0])
    if n == 0:
        return "1"
    a, b, c = 1, 2, 4
    if n == 1:
        return "1"
    if n == 2:
        return "2"
    if n == 3:
        return "4"
    for _ in range(4, n + 1):
        a, b, c = b, c, a + b + c
    return str(c)


add(id="p-23-01", chapter=23, label="习题 23-1", title="一次迈 1、2、3 级台阶",
    difficulty=1,
    statement_md="爬台阶，一次可以迈 1 级、2 级或 3 级，求走到第 n 级的方案数。先写出转移方程，再手算 n = 1 到 6 的值，最后写程序验证（n ≤ 70，用 `long long`）。\n\n本题是第 23 章习题 1。规定站在地面（第 0 级）算 1 种方案。",
    input_md="一个整数 n（0 ≤ n ≤ 70）。",
    output_md="一个整数，表示方案数。",
    constraints_md="0 ≤ n ≤ 70，答案在 `long long` 范围内。",
    hint_md="`f(0)=1`，`f(n)=f(n-1)+f(n-2)+f(n-3)`（负数项按 0 处理）。",
    tags=["递推", "DP"],
    cases=["0", "1", "2", "3", "6", "70"],
    solve=p2301)

def p2302(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    a = []
    for i in range(1, n + 1):
        a.append(list(map(int, d[p:p + i]))); p += i
    f = [0] * n
    f[n - 1] = a[n - 1][:]
    for i in range(n - 2, -1, -1):
        f[i] = [a[i][j] + max(f[i + 1][j], f[i + 1][j + 1]) for j in range(i + 1)]
    path = []
    j = 0
    for i in range(n):
        path.append(j + 1)
        if i == n - 1:
            break
        if f[i + 1][j] >= f[i + 1][j + 1]:
            pass
        else:
            j += 1
    return str(f[0][0]) + "\n" + " ".join(map(str, path))


add(id="p-23-02", chapter=23, label="习题 23-2", title="数字三角形与路径",
    difficulty=2,
    statement_md="数字三角形要求输出最大和，还要输出走过的路径（用一行下标表示每一层选的列号）。提示：多开一个 `from[i][j]` 记录「这一步是从左下还是右下上来的」。\n\n本题是第 23 章习题 2。若有多条最优路径，输出列号字典序最小的一条（每层尽量选左边）。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 1000）。\n接下来 n 行，第 i 行有 i 个整数（0 ≤ 数 ≤ 10^4）。",
    output_md="第一行一个整数，表示最大和；第二行 n 个整数，表示每层选的列号（从 1 开始）。",
    constraints_md="1 ≤ n ≤ 1000。",
    hint_md="从下往上递推；还原时从第一层开始，若左下与右下一样大就优先走左下。",
    tags=["DP", "路径还原"],
    cases=["5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5", "1\n5", "2\n1\n2 3",
           "3\n1\n2 2\n3 3 3"],
    solve=p2302)

def p2303(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    best = a[0]
    cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return str(best)


add(id="p-23-03", chapter=23, label="习题 23-3", title="最大子段和",
    difficulty=2,
    statement_md="给 n 个整数（可以是负数），求连续一段的和的最大值。先想「以 a[i] 结尾的最大子段和」是什么状态，再写转移。\n\n本题是第 23 章习题 3。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（|a[i]| ≤ 10^9）。",
    output_md="一个整数，表示最大子段和（至少取一个数）。",
    constraints_md="1 ≤ n ≤ 10^5，答案用 `long long`。",
    hint_md="`dp[i] = max(a[i], dp[i-1] + a[i])`，答案是所有 dp 的最大值；初始值不能设成 0（全负数会错）。",
    tags=["DP", "最大子段和"],
    cases=["5\n1 -2 3 4 -1", "3\n-5 -2 -9", "1\n-1000000000", "6\n-1 -2 -3 -4 -5 -6",
           "5\n1 2 3 4 5"],
    solve=p2303)

def p2304(t):
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


add(id="p-23-04", chapter=23, label="习题 23-4", title="最长不下降子序列",
    difficulty=2,
    statement_md="把 LIS 的 `a[j] < a[i]` 改成 `a[j] <= a[i]`，其余不变，求最长不下降子序列长度。再想：如果要求输出这个子序列本身（不是长度），该怎么办？\n\n本题是第 23 章习题 4。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示最长不下降子序列长度。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="二分时用 `upper_bound` 而不是 `lower_bound`，就允许相等。",
    tags=["LIS", "二分"],
    cases=["6\n1 5 3 4 6 2", "5\n5 4 3 2 1", "5\n1 2 3 4 5", "6\n2 2 2 2 2 2",
           "8\n3 1 2 2 4 3 5 5"],
    solve=p2304)

def p2305(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))

    def linear(arr, l, r):
        take = 0
        skip = 0
        for i in range(l, r + 1):
            take, skip = skip + arr[i], max(take, skip)
        return max(take, skip)

    if n == 1:
        return str(a[0])
    return str(max(linear(a, 0, n - 2), linear(a, 1, n - 1)))


add(id="p-23-05", chapter=23, label="习题 23-5", title="打家劫舍（环形）",
    difficulty=3,
    statement_md="一排 n 户人家围成一个环，每户有现金 a[i]，不能同时偷相邻的两户（第 1 户和第 n 户也相邻），求最多能偷多少。先写线性版，再把环拆成两个线性问题。\n\n本题是第 23 章习题 5。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 a[i]（0 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示最多能偷到的现金。",
    constraints_md="1 ≤ n ≤ 10^5，答案用 `long long`。",
    hint_md="环拆成「不偷第 n 户」和「不偷第 1 户」两个线性问题，取较大值。",
    tags=["DP", "环形"],
    cases=["4\n1 2 3 1", "1\n5", "3\n2 3 2", "5\n5 5 5 5 5", "6\n1 2 3 4 5 6"],
    solve=p2305)

# ================================================================ 第 24 章
def p2401(t):
    d = t.split()
    n, W = int(d[0]), int(d[1])
    v = list(map(int, d[2:2 + n]))
    dp = [False] * (W + 1)
    dp[0] = True
    for x in v:
        for j in range(W, x - 1, -1):
            if dp[j - x]:
                dp[j] = True
    for j in range(W, -1, -1):
        if dp[j]:
            return str(j)


add(id="p-24-01", chapter=24, label="习题 24-1", title="装箱问题",
    difficulty=1,
    statement_md="n 件物品各有体积，箱子容量为 W，问最多能装多满（不要求价值最大，只求装进去的总体积最大）。提示：把「体积」同时当重量和价值。\n\n本题是第 24 章习题 1。",
    input_md="第一行两个整数 n、W（1 ≤ n ≤ 1000，1 ≤ W ≤ 1000）。\n第二行 n 个整数 v[i]（1 ≤ v[i] ≤ W）。",
    output_md="一个整数，表示能装下的最大总体积。",
    constraints_md="1 ≤ n, W ≤ 1000。",
    hint_md="0-1 背包可行性：`dp[j] |= dp[j-v]`，容量倒序；最后从 W 往下找第一个可达的 j。",
    tags=["背包"],
    cases=["3 10\n5 4 6", "1 5\n6", "4 10\n2 3 4 5", "5 7\n1 2 3 4 5"],
    solve=p2401)

def p2402(t):
    d = t.split()
    n, W = int(d[0]), int(d[1])
    coins = list(map(int, d[2:2 + n]))
    INF = 10 ** 9
    dp = [INF] * (W + 1)
    dp[0] = 0
    for c in coins:
        for j in range(c, W + 1):
            if dp[j - c] + 1 < dp[j]:
                dp[j] = dp[j - c] + 1
    return str(dp[W]) if dp[W] < INF else "-1"


add(id="p-24-02", chapter=24, label="习题 24-2", title="货币系统",
    difficulty=1,
    statement_md="给 n 种面额（每种无限多），问凑出金额 W 最少要几枚硬币；如果凑不出，输出 -1。提示：初值全 +∞，`dp[0] = 0`，转移用 `min`。\n\n本题是第 24 章习题 2。",
    input_md="第一行两个整数 n、W（1 ≤ n ≤ 100，1 ≤ W ≤ 10^5）。\n第二行 n 个整数，表示每种面额（1 ≤ 面额 ≤ 10^5）。",
    output_md="一个整数，表示最少硬币数；凑不出输出 -1。",
    constraints_md="1 ≤ n ≤ 100，1 ≤ W ≤ 10^5。",
    hint_md="完全背包：容量正序枚举，`dp[j] = min(dp[j], dp[j-c]+1)`。",
    tags=["完全背包"],
    cases=["2 10\n5 2", "3 7\n1 2 5", "2 3\n2 4", "1 100000\n1", "4 27\n2 5 7 11"],
    solve=p2402)

def p2403(t):
    d = t.split()
    p = 0
    n, W = int(d[p]), int(d[p + 1]); p += 2
    groups = []
    for _ in range(n):
        k = int(d[p]); p += 1
        items = []
        for _ in range(k):
            w, v = int(d[p]), int(d[p + 1]); p += 2
            items.append((w, v))
        groups.append(items)
    dp = [0] * (W + 1)
    for items in groups:
        ndp = dp[:]
        for w, v in items:
            for j in range(W, w - 1, -1):
                if dp[j - w] + v > ndp[j]:
                    ndp[j] = dp[j - w] + v
        dp = ndp
    return str(max(dp))


add(id="p-24-03", chapter=24, label="习题 24-3", title="分组背包",
    difficulty=2,
    statement_md="n 组物品，每组最多选一件，背包容量为 W，求最大总价值。先用样例验证你的循环顺序，再把「容量在中间、组在最小层」的错误写法跑一遍，看结果错在哪。\n\n本题是第 24 章习题 3。",
    input_md="第一行两个整数 n、W（1 ≤ n ≤ 100，1 ≤ W ≤ 1000）。\n接下来 n 组：每组先一个整数 k，再 k 行「重量 价值」（1 ≤ k ≤ 100，1 ≤ 重量 ≤ W，1 ≤ 价值 ≤ 10^4）。",
    output_md="一个整数，表示最大总价值。",
    constraints_md="1 ≤ n ≤ 100，1 ≤ W ≤ 1000。",
    hint_md="每组单独一层，用上一组的结果更新；同组内不能重复选，所以每组内对每个物品用倒序 0-1 更新。",
    tags=["分组背包"],
    cases=["2 10\n2\n5 10\n4 40\n1\n6 30", "1 5\n3\n1 1\n2 2\n3 3",
           "3 10\n1\n10 100\n1\n9 90\n1\n1 1", "2 6\n2\n2 3\n4 8\n2\n3 4\n5 9"],
    solve=p2403)

def p2404(t):
    d = t.split()
    p = 0
    n, W = int(d[p]), int(d[p + 1]); p += 2
    items = []
    for _ in range(n):
        w, v = int(d[p]), int(d[p + 1]); p += 2
        items.append((w, v))
    NEG = -10 ** 18
    dp = [NEG] * (W + 1)
    dp[0] = 0
    for w, v in items:
        for j in range(W, w - 1, -1):
            if dp[j - w] != NEG and dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
    return str(dp[W]) if dp[W] != NEG else "-1"


add(id="p-24-04", chapter=24, label="习题 24-4", title="恰好装满的 0-1 背包",
    difficulty=2,
    statement_md="n 件物品各有重量和价值，要求总重量恰好为 W，求最大价值；无解输出 -1。再用同一组数据算「不超过 W 的最大价值」，比较两者答案。\n\n本题是第 24 章习题 4。",
    input_md="第一行两个整数 n、W（1 ≤ n ≤ 1000，1 ≤ W ≤ 1000）。\n接下来 n 行，每行两个整数 w[i]、v[i]（1 ≤ w[i] ≤ W，1 ≤ v[i] ≤ 10^4）。",
    output_md="一个整数，表示恰好装满 W 时的最大价值；无解输出 -1。",
    constraints_md="1 ≤ n, W ≤ 1000。",
    hint_md="`dp[0]=0`，其余初始化为负无穷；只有 `dp[j-w]` 可达时才更新，最后 `dp[W]` 仍是负无穷就是无解。",
    tags=["背包"],
    cases=["3 10\n5 10\n4 40\n6 30", "1 5\n6 100", "3 5\n1 1\n2 2\n3 3",
           "4 10\n2 3\n2 3\n2 3\n2 3"],
    solve=p2404)

def p2405(t):
    d = t.split()
    p = 0
    n, W1, W2 = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
    dp = [[0] * (W2 + 1) for _ in range(W1 + 1)]
    for _ in range(n):
        w1, w2, v = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        for i in range(W1, w1 - 1, -1):
            for j in range(W2, w2 - 1, -1):
                if dp[i - w1][j - w2] + v > dp[i][j]:
                    dp[i][j] = dp[i - w1][j - w2] + v
    return str(dp[W1][W2])


add(id="p-24-05", chapter=24, label="习题 24-5", title="二维费用背包",
    difficulty=3,
    statement_md="物品有重量和体积两个代价，背包有重量上限 W1 和体积上限 W2，每件最多拿一次，求最大价值。状态应该是几维？空间怎么用滚动数组压到 O(W1×W2)？\n\n本题是第 24 章习题 5。",
    input_md="第一行三个整数 n、W1、W2（1 ≤ n ≤ 100，1 ≤ W1, W2 ≤ 500）。\n接下来 n 行，每行三个整数 w1、w2、v（1 ≤ w1 ≤ W1，1 ≤ w2 ≤ W2，1 ≤ v ≤ 10^4）。",
    output_md="一个整数，表示最大价值。",
    constraints_md="1 ≤ n ≤ 100，1 ≤ W1, W2 ≤ 500。",
    hint_md="二维 0-1 背包，两个容量都倒序枚举；一维数组压不掉，但每层只依赖上一层，可以原地更新。",
    tags=["二维背包"],
    cases=["3 5 5\n2 2 3\n3 3 4\n1 4 2", "1 5 5\n6 1 10", "3 10 10\n5 5 10\n5 5 10\n5 5 10",
           "4 8 7\n2 3 5\n3 2 6\n4 4 9\n1 1 2"],
    solve=p2405)

def p2406(t):
    d = t.split()
    p = 0
    n, B, T = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
    dp = [[0] * (T + 1) for _ in range(B + 1)]
    for _ in range(n):
        cost, tm, joy = int(d[p]), int(d[p + 1]), int(d[p + 2]); p += 3
        for i in range(B, cost - 1, -1):
            for j in range(T, tm - 1, -1):
                if dp[i - cost][j - tm] + joy > dp[i][j]:
                    dp[i][j] = dp[i - cost][j - tm] + joy
    return str(dp[B][T])


add(id="p-24-06", chapter=24, label="习题 24-6", title="贵阳一日游预算",
    difficulty=3,
    statement_md="有 n 个景点，每个景点有门票价格、游玩时长和「开心值」。总预算 B 元、总时间 T 小时，每个景点最多去一次，求最大开心值。\n\n本题是第 24 章习题 6：先想清楚这是几维背包，再写代码。",
    input_md="第一行三个整数 n、B、T（1 ≤ n ≤ 100，1 ≤ B ≤ 500，1 ≤ T ≤ 500）。\n接下来 n 行，每行三个整数 价格、时长、开心值（1 ≤ 价格 ≤ B，1 ≤ 时长 ≤ T，1 ≤ 开心值 ≤ 10^4）。",
    output_md="一个整数，表示最大开心值。",
    constraints_md="1 ≤ n ≤ 100，1 ≤ B, T ≤ 500。",
    hint_md="价格和时间是两个费用，标准的二维 0-1 背包；两个维度都倒序枚举。",
    tags=["二维背包", "DP"],
    cases=["3 10 8\n5 4 10\n4 3 8\n6 5 12", "1 5 5\n6 1 10", "3 10 10\n5 5 10\n5 5 10\n5 5 10",
           "4 8 7\n2 3 5\n3 2 6\n4 4 9\n1 1 2"],
    solve=p2406)
