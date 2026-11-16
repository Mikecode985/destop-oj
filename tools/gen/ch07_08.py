#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 7～8 章可编程习题。"""
import math

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 7 章
def p0701(t):
    d = t.split()
    p = 0
    n, q = int(d[p]), int(d[p + 1]); p += 2
    a = list(map(int, d[p:p + n])); p += n
    out = []
    for _ in range(q):
        x = int(d[p]); p += 1
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] > x:
                hi = mid
            else:
                lo = mid + 1
        out.append(str(lo + 1))
    return "\n".join(out)


add(id="p-07-01", chapter=7, label="习题 7-1", title="第一个大于 x 的位置",
    difficulty=1,
    statement_md="给一个升序数组和 q 次询问，每次输出第一个严格大于 x 的元素位置（位置从 1 开始）；不存在输出 n+1。请先手写二分，再用 `upper_bound` 验证。\n\n本题是第 7 章习题 1。",
    input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 10^5）。\n第二行 n 个非降序排列的整数（1 ≤ a[i] ≤ 10^9）。\n第三行 q 个整数 x（1 ≤ x ≤ 10^9）。",
    output_md="对每次询问输出一行，表示第一个大于 x 的位置；不存在输出 n+1。",
    constraints_md="1 ≤ n, q ≤ 10^5。",
    hint_md="手写时用 `[0, n)` 半开区间，循环结束 `lo` 就是答案；也可以直接 `upper_bound(a, a+n, x) - a + 1`。",
    tags=["二分"],
    cases=["5 3\n1 3 5 7 9\n3 4 10", "1 1\n5\n5", "1 1\n5\n4", "4 2\n2 2 2 2\n1 2",
           "6 4\n1 2 2 5 9 9\n0 2 9 10"],
    solve=p0701)

def p0703(t):
    d = t.split()
    n, m = int(d[0]), int(d[1])
    h = list(map(int, d[2:2 + n]))
    if sum(h) < m:
        return "0"
    lo, hi = 0, max(h)
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if sum(x - mid for x in h if x > mid) >= m:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(ans)


add(id="p-07-03", chapter=7, label="习题 7-3", title="砍树",
    difficulty=2,
    statement_md="有 n 棵树，第 i 棵高 h[i]。把锯片高度设为 H，所有比 H 高的树会被锯掉 H 以上的部分，得到 sum(max(0, h[i]-H)) 米木材。要得到至少 m 米木材，H 最大可以是多少？\n\n本题是第 7 章习题 3。",
    input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^6，1 ≤ m ≤ 10^9）。\n第二行 n 个整数 h[i]（1 ≤ h[i] ≤ 10^9）。",
    output_md="一个整数，表示最大的 H；木材总量不足 m 时输出 0。",
    constraints_md="1 ≤ n ≤ 10^6，1 ≤ m ≤ 10^9，1 ≤ h[i] ≤ 10^9。",
    hint_md="H 越高得到的木材越少，答案有单调性；二分 H，`check(H)` 累加 `max(0, h[i]-H)`，用 `long long`。",
    tags=["二分答案"],
    cases=["4 7\n20 15 10 17", "1 1\n10", "3 100\n1 2 3", "5 0\n5 4 3 2 1",
           "6 20\n10 10 10 10 10 10"],
    solve=p0703)

def p0704(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    w = list(map(int, d[2:2 + n]))
    lo, hi = max(w), sum(w)
    while lo < hi:
        mid = (lo + hi) // 2
        cnt = 1
        cur = 0
        ok = True
        for x in w:
            if cur + x <= mid:
                cur += x
            else:
                cnt += 1
                cur = x
                if cnt > k:
                    ok = False
                    break
        if ok:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


add(id="p-07-04", chapter=7, label="习题 7-4", title="快递装车",
    difficulty=2,
    statement_md="有 n 个包裹，重量为 w[i]。每辆车最多装 W 公斤，并且每辆车装的包裹必须是输入顺序中连续的一段。要用不超过 k 辆车装完所有包裹，W 最小是多少？\n\n本题是第 7 章习题 4：二分 W，`check(W)` 用贪心往后装。",
    input_md="第一行两个整数 n、k（1 ≤ k ≤ n ≤ 10^5）。\n第二行 n 个整数 w[i]（1 ≤ w[i] ≤ 10^9）。",
    output_md="一个整数，表示最小的 W。",
    constraints_md="1 ≤ k ≤ n ≤ 10^5，1 ≤ w[i] ≤ 10^9。",
    hint_md="下界是 `max(w[i])`，上界是总和；`check` 里能装就装，装不下就开新车，数一数车数是否 ≤ k。",
    tags=["二分答案", "贪心"],
    cases=["5 3\n1 2 3 4 5", "1 1\n7", "5 5\n1 2 3 4 5", "4 2\n1 2 3 4",
           "6 2\n10 20 30 40 50 60"],
    solve=p0704)

def p0705(t):
    lo, hi = 1.0, 2.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if mid ** 3 - mid - 1 >= 0:
            hi = mid
        else:
            lo = mid
    return str(int((lo + hi) / 2 * 1000000))


add(id="p-07-05", chapter=7, label="习题 7-5", title="浮点二分求根",
    difficulty=2,
    statement_md="求方程 x³ - x - 1 = 0 在区间 [1, 2] 内的根。要求用二分法循环 100 次，误差不超过 10^-6。\n\n本题是第 7 章习题 5。为了便于评测，请输出一个整数：⌊10^6 × 根⌋。",
    input_md="本题没有输入。",
    output_md="一个整数，表示 ⌊10^6 × 根⌋。",
    constraints_md="根在 [1, 2] 内，函数单调递增。",
    hint_md="二分 100 次后取区间中点；输出时转成 `long long` 并乘以 10^6 再取整（注意先乘后取整）。",
    tags=["浮点二分"],
    cases=[""],
    solve=p0705)

# ================================================================ 第 8 章
def p0801(t):
    n = int(t.split()[0])
    coins = [10, 5, 2, 1]
    cnt = 0
    for c in coins:
        cnt += n // c
        n %= c
    return str(cnt)


add(id="p-08-01", chapter=8, label="习题 8-1", title="找零钱",
    difficulty=1,
    statement_md="面值为 1、2、5、10 元的硬币，要凑出 n 元，求最少的硬币张数。请用「每次拿最大面值」的贪心。\n\n本题是第 8 章习题 1。",
    input_md="一个整数 n（1 ≤ n ≤ 10^9）。",
    output_md="一个整数，表示最少硬币数。",
    constraints_md="1 ≤ n ≤ 10^9。",
    hint_md="面值 1/2/5/10 是「规范」的，贪心一定最优；从大到小整除取商再取余。",
    tags=["贪心"],
    cases=["11", "1", "10", "99", "1000000000"],
    solve=p0801)

def p0802(t):
    d = t.split()
    p = 0
    n, dd = int(d[p]), int(d[p + 1]); p += 2
    seg = []
    for _ in range(n):
        x, y = int(d[p]), int(d[p + 1]); p += 2
        if y > dd:
            return "-1"
        dx = math.sqrt(dd * dd - y * y)
        seg.append((x - dx, x + dx))
    seg.sort(key=lambda s: s[1])
    cnt = 0
    last = -1e18
    for l, r in seg:
        if l > last or cnt == 0:
            cnt += 1
            last = r
    return str(cnt)


add(id="p-08-02", chapter=8, label="习题 8-2", title="雷达覆盖",
    difficulty=2,
    statement_md="海岸线是一条直线（y=0），海上有 n 个小岛，第 i 个岛坐标 (x[i], y[i])，y[i] > 0。要在海岸线上放雷达，每个雷达的覆盖半径是 d，求覆盖所有小岛最少需要几个雷达；有岛覆盖不到输出 -1。\n\n本题是第 8 章习题 2：把每个小岛转化成海岸线上的一段区间，按区间右端点排序后贪心。",
    input_md="第一行两个整数 n、d（1 ≤ n ≤ 1000，1 ≤ d ≤ 10^4）。\n接下来 n 行，每行两个整数 x[i]、y[i]（-10^4 ≤ x[i] ≤ 10^4，1 ≤ y[i] ≤ 10^4）。",
    output_md="一个整数，表示最少雷达数；有岛覆盖不到输出 -1。",
    constraints_md="1 ≤ n ≤ 1000，1 ≤ d ≤ 10^4。",
    hint_md="岛 (x,y) 能被海岸线上的雷达 (a,0) 覆盖，当且仅当 `(x-a)²+y² ≤ d²`，即 a 落在 `[x-sqrt(d²-y²), x+sqrt(d²-y²)]`；按右端点排序，能共用就共用。",
    tags=["贪心", "区间"],
    cases=["3 2\n1 2\n-2 1\n3 1", "1 1\n0 2", "1 5\n0 3", "2 3\n0 3\n0 3",
           "5 2\n1 1\n2 1\n3 1\n4 1\n5 1"],
    solve=p0802)

def p0803(t):
    d = t.split()
    n = int(d[0])
    a = sorted(map(int, d[1:1 + n]))
    b = sorted(map(int, d[1 + n:1 + 2 * n]))
    la, ra, lb, rb = 0, n - 1, 0, n - 1
    money = 0
    while la <= ra:
        if a[ra] > b[rb]:
            money += 200
            ra -= 1
            rb -= 1
        elif a[la] > b[lb]:
            money += 200
            la += 1
            lb += 1
        else:
            if a[la] < b[rb]:
                money -= 200
            la += 1
            rb -= 1
    return str(money)


add(id="p-08-03", chapter=8, label="习题 8-3", title="田忌赛马",
    difficulty=2,
    statement_md="田忌和齐王各有 n 匹马，速度分别已知。每场比赛双方各出一匹，快者赢 200 银，慢者输 200 银，平局不输不赢。请设计贪心策略，使田忌赢的钱最多。\n\n本题是第 8 章习题 3。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数，表示田忌的马速。\n第三行 n 个整数，表示齐王的马速。",
    output_md="一个整数，表示田忌最多能赢的银两（可以是负数）。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ 马速 ≤ 10^9。",
    hint_md="两边都排序，双指针：能赢对方最快的就赢；否则用自己最慢的去消耗对方最快的。",
    tags=["贪心"],
    cases=["3\n92 83 71\n95 87 74", "2\n1 2\n3 4", "3\n1 2 3\n1 2 3",
           "1\n10\n5", "4\n20 30 40 50\n10 20 30 40"],
    solve=p0803)
