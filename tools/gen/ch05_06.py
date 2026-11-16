#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 5～6 章可编程习题。"""
from bisect import bisect_left, bisect_right

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 5 章
def p0501(t):
    d = t.split()
    n = int(d[0])
    floor = 1
    total = 0
    for x in map(int, d[1:1 + n]):
        total += abs(x - floor) + 1
        floor = x
    return "%d %d" % (total, floor)


add(id="p-05-01", chapter=5, label="习题 5-1", title="模拟一部电梯",
    difficulty=1,
    statement_md="一部电梯初始停在 1 楼，依次收到若干个请求楼层。电梯每上下移动一层用 1 秒，每到达一个请求楼层停留 1 秒（请求楼层与当前楼层相同也要停 1 秒）。请输出处理完所有请求后的总用时和最终楼层。\n\n本题是第 5 章习题 1。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 1000）。\n第二行 n 个整数，依次表示请求楼层（1 ≤ 楼层 ≤ 100）。",
    output_md="一行两个整数：总用时、最终楼层，用一个空格隔开。",
    constraints_md="1 ≤ n ≤ 1000，1 ≤ 楼层 ≤ 100。",
    hint_md="维护当前楼层，逐个请求累加 `|目标-当前| + 1`，再更新当前楼层。",
    tags=["模拟"],
    cases=["3\n3 5 2", "1\n1", "4\n1 1 1 1", "5\n100 1 100 1 50"],
    solve=p0501)

def p0502(t):
    t_ = int(t.split()[0])
    r = t_ % 90
    if r < 30:
        return "绿灯"
    if r < 33:
        return "黄灯"
    return "红灯"


add(id="p-05-02", chapter=5, label="习题 5-2", title="路口的红绿灯",
    difficulty=1,
    statement_md="某路口的红绿灯以 90 秒为一个周期：前 30 秒绿灯，中间 3 秒黄灯，剩下 57 秒红灯，循环往复。给定从零时刻起的秒数 t，输出当前是什么灯。\n\n本题是第 5 章习题 2。",
    input_md="一个整数 t（0 ≤ t ≤ 10^9）。",
    output_md="输出 `绿灯`、`黄灯` 或 `红灯`。",
    constraints_md="0 ≤ t ≤ 10^9。",
    hint_md="`t % 90` 落到 0～89，再看落在三个区间的哪一个。",
    tags=["模拟", "周期"],
    cases=["0", "29", "30", "32", "33", "89", "90", "1000000000"],
    solve=p0502)

def p0503(t):
    import datetime
    a = list(map(int, t.split()[:6]))
    d1 = datetime.date(a[0], a[1], a[2])
    d2 = datetime.date(a[3], a[4], a[5])
    return str(abs((d2 - d1).days))


add(id="p-05-03", chapter=5, label="习题 5-3", title="两个日期相差多少天",
    difficulty=2,
    statement_md="输入两个日期，输出它们之间相差多少天（同一天算 0 天）。要求能处理跨年、闰年，以及第二个日期早于第一个日期的情况。\n\n本题是第 5 章习题 3：可以自己写「从公元 1 年 1 月 1 日到今天过了多少天」的函数，也可以逐月累加。",
    input_md="一行六个整数 y1 m1 d1 y2 m2 d2（1 ≤ 年份 ≤ 9999，日期保证合法）。",
    output_md="一个整数，表示两个日期相差的天数（取绝对值）。",
    constraints_md="1 ≤ 年份 ≤ 9999，保证日期合法。",
    hint_md="写 `days(y,m,d)` 把日期换算成「距 1 年 1 月 1 日的天数」，再相减取绝对值；闰年判断是 `(y%4==0 && y%100!=0) || y%400==0`。",
    tags=["模拟", "日期"],
    cases=["2024 2 29 2024 3 1", "2023 1 1 2023 1 1", "2024 12 31 2025 1 1",
           "2020 2 28 2020 3 1", "1900 1 1 2000 1 1"],
    solve=p0503)

def p0504(t):
    n = int(t.split()[0])
    g = [[0] * n for _ in range(n)]
    x = y = 0
    dx, dy = 0, 1
    for k in range(1, n * n + 1):
        g[x][y] = k
        nx, ny = x + dx, y + dy
        if not (0 <= nx < n and 0 <= ny < n and g[nx][ny] == 0):
            dx, dy = dy, -dx
            nx, ny = x + dx, y + dy
        x, y = nx, ny
    return "\n".join(" ".join(map(str, row)) for row in g)


add(id="p-05-04", chapter=5, label="习题 5-4", title="蛇形填数",
    difficulty=2,
    statement_md="把 1 到 n×n 依次填入 n×n 的矩阵：从左上角出发向右走，碰到边界或已经填过的格子就顺时针转弯（右→下→左→上），一圈一圈往里绕。输出填好的矩阵。\n\n本题是第 5 章习题 4。",
    input_md="一个整数 n（1 ≤ n ≤ 100）。",
    output_md="共 n 行，每行 n 个整数，相邻两数用一个空格隔开。",
    constraints_md="1 ≤ n ≤ 100。",
    hint_md="用 `dx/dy` 表示当前方向，走到边界或已填过就右转；每次填一个数。",
    tags=["模拟", "矩阵"],
    cases=["1", "2", "3", "4", "5"],
    solve=p0504)

def p0505(t):
    expr = t.strip()
    tokens = []
    num = ""
    for ch in expr:
        if ch.isdigit():
            num += ch
        elif ch in "+-*/":
            if num:
                tokens.append(int(num))
                num = ""
            tokens.append(ch)
        # 空格忽略
    if num:
        tokens.append(int(num))
    # 第一遍：乘除
    st = [tokens[0]]
    i = 1
    while i < len(tokens):
        op = tokens[i]
        b = tokens[i + 1]
        if op == "*":
            st[-1] = st[-1] * b
        elif op == "/":
            st[-1] = st[-1] // b
        else:
            st.append(op)
            st.append(b)
        i += 2
    ans = st[0]
    i = 1
    while i < len(st):
        if st[i] == "+":
            ans += st[i + 1]
        else:
            ans -= st[i + 1]
        i += 2
    return str(ans)


add(id="p-05-05", chapter=5, label="习题 5-5", title="简易计算器",
    difficulty=3,
    statement_md="输入一行只含非负整数、空格和 `+`、`-`、`*`、`/` 的表达式（没有括号），按先乘除后加减的规则求值。除法向下取整。\n\n本题是第 5 章习题 5：提示先把所有数和运算符读进来，第一遍处理乘除，第二遍处理加减。",
    input_md="一行一个表达式，长度不超过 10^5，数字不超过 10^9，保证不会除以 0。",
    output_md="一个整数，表示表达式的值。",
    constraints_md="1 ≤ 表达式长度 ≤ 10^5；所有中间结果在 64 位整数范围内。",
    hint_md="把表达式切成「数 运算符 数」的序列；第一遍用栈把乘除就地算掉，第二遍从左往右算加减。",
    tags=["模拟", "栈"],
    cases=["1+2*3", "10 - 4 / 2", "2*3+4*5", "100/3/2", "7", "1+2+3+4*5-6/2"],
    solve=p0505)

# ================================================================ 第 6 章
def p0601(t):
    out = []
    cnt = 0
    for x in range(1, 101):
        for y in range(1, 101):
            z = 100 - x - y
            if z < 1:
                continue
            if 5 * x + 3 * y + z / 3 == 100 and z % 3 == 0:
                out.append("%d %d %d" % (x, y, z))
                cnt += 1
    return "\n".join(out + [str(cnt)])


add(id="p-06-01", chapter=6, label="习题 6-1", title="百钱买百鸡",
    difficulty=1,
    statement_md="公鸡 5 元一只，母鸡 3 元一只，小鸡 1 元 3 只。用 100 元买 100 只鸡，每种至少 1 只。输出所有方案，并统计方案数。\n\n本题是第 6 章习题 1：用两层循环枚举公鸡和母鸡，小鸡数量由总数直接算出。",
    input_md="本题没有输入。",
    output_md="若干行，每行三个整数「公鸡数 母鸡数 小鸡数」，按公鸡数升序、母鸡数升序输出；最后一行一个整数，表示方案数。",
    constraints_md="小鸡数必须是 3 的倍数；100 元恰好花完，100 只恰好买够。",
    hint_md="枚举 x（公鸡）与 y（母鸡），`z = 100 - x - y`，判断 `z % 3 == 0` 且 `5x + 3y + z/3 == 100`。",
    tags=["枚举"],
    cases=[""],
    solve=p0601)

def p0602(t):
    d = t.split()
    n, S = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    for mask in range(1 << n):
        s = 0
        for i in range(n):
            if mask >> i & 1:
                s += a[i]
        if s == S:
            return "YES"
    return "NO"


add(id="p-06-02", chapter=6, label="习题 6-2", title="子集和判定",
    difficulty=1,
    statement_md="输入 n 个整数和一个目标 S，判断是否存在一个子集（每样选或不选）的和恰好为 S。n ≤ 20，要求用二进制枚举实现。\n\n本题是第 6 章习题 2。",
    input_md="第一行两个整数 n、S（1 ≤ n ≤ 20，0 ≤ S ≤ 10^9）。\n第二行 n 个整数（0 ≤ a[i] ≤ 10^9）。",
    output_md="存在输出 `YES`，否则输出 `NO`。",
    constraints_md="1 ≤ n ≤ 20，0 ≤ S, a[i] ≤ 10^9。",
    hint_md="枚举 0 到 (1<<n)-1 的每个掩码，把对应元素加起来与 S 比较。",
    tags=["枚举", "二进制"],
    cases=["5 5\n1 2 3 4 5", "3 7\n1 2 4", "1 0\n0", "4 10\n2 2 2 2",
           "20 100\n" + " ".join(["5"] * 20)],
    solve=p0602)

def p0603(t):
    from math import isqrt
    n = int(t.split()[0])
    for a in range(0, isqrt(n) + 1):
        a2 = a * a
        for b in range(a, isqrt(n - a2) + 1):
            b2 = b * b
            for c in range(b, isqrt(n - a2 - b2) + 1):
                rem = n - a2 - b2 - c * c
                if rem < c * c:
                    continue
                d = isqrt(rem)
                if d * d == rem:
                    return "%d %d %d %d" % (a, b, c, d)
    return "-1"


add(id="p-06-03", chapter=6, label="习题 6-3", title="四平方和",
    difficulty=2,
    statement_md="输入一个正整数 n，判断它能否写成四个整数的平方和（允许 0），输出一组解。要求只枚举前三个数，第四个数由等式直接算出。\n\n本题是第 6 章习题 3。为了让答案唯一，规定输出的四个数满足 a ≤ b ≤ c ≤ d，并且取字典序最小的一组。",
    input_md="一个整数 n（1 ≤ n ≤ 10^7）。",
    output_md="一行四个整数 a b c d，满足 a²+b²+c²+d²=n 且 0 ≤ a ≤ b ≤ c ≤ d；无解输出 -1（在本题范围内一定有解）。",
    constraints_md="1 ≤ n ≤ 10^7。",
    hint_md="枚举 a、b、c，第四个数 `d = sqrt(n - a² - b² - c²)`，检查是否为整数，且 d ≥ c。",
    tags=["枚举"],
    cases=["5", "1", "30", "10000000", "9999999"],
    solve=p0603)

def p0604(t):
    n = int(t.split()[0])
    cnt = 0
    for x in range(1, n + 1):
        if sum(map(int, str(x))) % 9 == 0:
            cnt += 1
    return str(cnt)


add(id="p-06-04", chapter=6, label="习题 6-4", title="各位数字之和是 9 的倍数",
    difficulty=2,
    statement_md="统计 1 到 n 之间，各位数字之和是 9 的倍数的数有多少个。n ≤ 10^6，要求只枚举一遍。\n\n本题是第 6 章习题 4。",
    input_md="一个整数 n（1 ≤ n ≤ 10^6）。",
    output_md="一个整数，表示满足条件的数的个数。",
    constraints_md="1 ≤ n ≤ 10^6。",
    hint_md="枚举 1 到 n，对每个数求各位数字之和，判断 `% 9 == 0`；10^6 次枚举在 1 秒内绰绰有余。",
    tags=["枚举", "数位"],
    cases=["1", "9", "10", "100", "1000000"],
    solve=p0604)

def p0605(t):
    d = t.split()
    n, S = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    half = n // 2

    def subset_sums(arr):
        sums = [0]
        for x in arr:
            sums += [s + x for s in sums]
        return sums

    sums = subset_sums(a[half:])
    sums.sort()
    ans = 0
    for s in subset_sums(a[:half]):
        need = S - s
        ans += bisect_right(sums, need) - bisect_left(sums, need)
    return str(ans)


add(id="p-06-05", chapter=6, label="习题 6-5", title="折半枚举数子集",
    difficulty=3,
    statement_md="给 n 个整数（n ≤ 40），问有多少个子集的和恰好等于 S。n = 40 时 2^40 太大，请把数组拆成两半分别枚举：前一半枚举出所有子集和并排序，后一半每枚举出一种和，就去前一半里二分查找补数。\n\n本题是第 6 章习题 5。",
    input_md="第一行两个整数 n、S（1 ≤ n ≤ 40，0 ≤ S ≤ 10^9）。\n第二行 n 个整数（0 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示和为 S 的子集个数（空集也算一个子集）。",
    constraints_md="1 ≤ n ≤ 40，0 ≤ S, a[i] ≤ 10^9，答案在 64 位整数范围内。",
    hint_md="两半各最多 20 个数，2^20 ≈ 10^6；左边子集和排序后，对右边的每个和 `S-sum` 做 `lower_bound/upper_bound` 计数。",
    tags=["折半枚举", "二分"],
    cases=["5 5\n1 2 3 4 5", "3 0\n0 0 0", "1 1\n1", "40 10\n" + " ".join(["1"] * 40),
           "20 0\n" + " ".join(["0"] * 20)],
    solve=p0605)
