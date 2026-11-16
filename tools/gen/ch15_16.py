#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 15～16 章可编程习题。"""
import heapq

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 15 章
def p1501(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    cnt = {}
    for x in a:
        cnt[x] = cnt.get(x, 0) + 1
    for x in a:
        if cnt[x] == 1:
            return str(x)
    return "-1"


add(id="p-15-01", chapter=15, label="习题 15-1", title="第一个只出现一次的数",
    difficulty=1,
    statement_md="给 n 个整数，输出第一个只出现一次的数（按原顺序），没有则输出 -1。请用哈希表写一遍，再想想如果值域只有 1～1000，能不能用数组更快。\n\n本题是第 15 章习题 1。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数：第一个只出现一次的数；不存在输出 -1。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="先用哈希表统计次数，再从左到右找第一个次数为 1 的数。",
    tags=["哈希"],
    cases=["5\n2 3 2 4 3", "3\n1 1 1", "1\n7", "4\n10 20 10 30",
           "6\n5 5 6 7 7 8"],
    solve=p1501)

def p1502(t):
    d = t.split()
    n, target = int(d[0]), int(d[1])
    a = set(map(int, d[2:2 + n]))
    out = []
    for x in sorted(a):
        y = target - x
        if y > x and y in a:
            out.append("%d %d" % (x, y))
    return "\n".join(out) if out else "No"


add(id="p-15-02", chapter=15, label="习题 15-2", title="所有和为 target 的数对",
    difficulty=2,
    statement_md="不要求输出下标，而是要求输出所有「和等于 target」的数对的值，且不能重复。\n\n本题是第 15 章习题 2：说明为什么需要用 `set<pair<int,int>>` 去重，以及为什么不能只存一个数。",
    input_md="第一行两个整数 n、target（2 ≤ n ≤ 10^5，1 ≤ target ≤ 2×10^9）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="每行一个数对「x y」（x < y），按 x 升序输出；没有数对输出 `No`。",
    constraints_md="2 ≤ n ≤ 10^5。",
    hint_md="存入哈希集合，遍历集合中每个 x，检查 `target-x` 是否也在集合里，并且只输出 `x < y` 的组合。",
    tags=["哈希", "数对"],
    cases=["5 9\n2 7 11 15 4", "4 8\n1 7 3 5", "2 4\n2 2", "3 6\n1 2 3",
           "6 10\n1 9 2 8 3 7"],
    solve=p1502)

def p1504(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    vals = sorted(set(a))
    rank = {v: i + 1 for i, v in enumerate(vals)}
    return " ".join(str(rank[x]) for x in a)


add(id="p-15-04", chapter=15, label="习题 15-4", title="离散化",
    difficulty=2,
    statement_md="给一个长度为 n 的数组，值在 -10^9 到 10^9 之间。请写出去重排序、把每个元素替换成排名的过程，并说明替换后数组的哪些性质保持不变、哪些变了。\n\n本题是第 15 章习题 4。排名从 1 开始，相同的值排名相同。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（|a[i]| ≤ 10^9）。",
    output_md="一行 n 个整数，表示每个元素离散化后的排名。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="去重排序后，用 `lower_bound` 或哈希表把原值映射到 1..k 的名次。",
    tags=["离散化", "排序"],
    cases=["5\n1000000000 5 -3 5 0", "1\n7", "4\n4 3 2 1", "3\n-1000000000 0 1000000000",
           "5\n2 2 2 2 2"],
    solve=p1504)

# ================================================================ 第 16 章
def p1601(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[2:2 + n]))
    h = []
    for x in a:
        heapq.heappush(h, x)
        if len(h) > k:
            heapq.heappop(h)
    return str(h[0])


add(id="p-16-01", chapter=16, label="习题 16-1", title="第 k 大（堆做法）",
    difficulty=2,
    statement_md="给 n 个整数，求其中第 k 大的数。请分别用「排序」和「大小为 k 的小根堆」两种写法，比较它们的时间复杂度和适用场合。\n\n本题是第 16 章习题 1。",
    input_md="第一行两个整数 n、k（1 ≤ k ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="一个整数，表示第 k 大的数。",
    constraints_md="1 ≤ k ≤ n ≤ 10^5。",
    hint_md="维护大小为 k 的小根堆：新元素比堆顶大就替换堆顶；最后堆顶就是第 k 大。",
    tags=["堆", "第 k 大"],
    cases=["5 2\n3 1 4 1 5", "1 1\n1", "5 5\n5 4 3 2 1", "6 3\n1 1 1 2 2 2",
           "7 4\n10 9 8 7 6 5 4"],
    solve=p1601)

def p1602(t):
    d = t.split()
    p = 0
    n = int(d[p]); p += 1
    tasks = []
    for _ in range(n):
        tt, dd = int(d[p]), int(d[p + 1]); p += 2
        tasks.append((dd, tt))
    tasks.sort()
    h = []
    total = 0
    for dd, tt in tasks:
        total += tt
        heapq.heappush(h, -tt)
        if total > dd:
            total += heapq.heappop(h)  # 弹出最长的那个（负值）
    return str(len(h))


add(id="p-16-02", chapter=16, label="习题 16-2", title="任务调度",
    difficulty=2,
    statement_md="有 n 个任务，每个任务有执行时间 t[i] 和截止时间 d[i]，一次只能做一个，从 0 时刻开始。问最多有多少个任务能在各自的截止时间前完成。\n\n本题是第 16 章习题 2：说明怎么用优先队列在「可做」的任务里挑一个先做，为什么这样能减少超时任务的数量。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行两个整数 t[i]、d[i]（1 ≤ t[i] ≤ 10^9，1 ≤ d[i] ≤ 10^9）。",
    output_md="一个整数，表示最多能按时完成的任务数。",
    constraints_md="1 ≤ n ≤ 10^5，时间总和可能超过 `int`。",
    hint_md="按截止时间从早到晚排序，依次把任务加进来；如果总耗时超过当前截止时间，就丢掉耗时最长的那个任务。",
    tags=["贪心", "堆"],
    cases=["3\n1 2\n2 4\n3 5", "1\n5 5", "3\n2 2\n2 2\n2 2",
           "4\n1 1\n1 2\n1 3\n1 4", "5\n3 6\n2 8\n1 9\n4 9\n2 10"],
    solve=p1602)

def p1603(t):
    n = int(t.split()[0])
    h = [1]
    seen = {1}
    x = 1
    for _ in range(n):
        x = heapq.heappop(h)
        for m in (2, 3, 5):
            y = x * m
            if y not in seen:
                seen.add(y)
                heapq.heappush(h, y)
    return str(x)


add(id="p-16-03", chapter=16, label="习题 16-3", title="丑数",
    difficulty=2,
    statement_md="丑数是只含质因子 2、3、5 的正整数，1 也是丑数。请设计一个算法，用优先队列从小到大依次生成丑数。\n\n本题是第 16 章习题 3：说明怎么去重、为什么不会漏。求第 n 个丑数。",
    input_md="一个整数 n（1 ≤ n ≤ 1500）。",
    output_md="一个整数，表示第 n 个丑数（1 是第 1 个）。",
    constraints_md="1 ≤ n ≤ 1500。",
    hint_md="小根堆放 1；每次弹出最小值 x，把 x*2、x*3、x*5 入堆，用集合去重。",
    tags=["堆"],
    cases=["1", "2", "10", "20", "1500"],
    solve=p1603)

def p1604(t):
    d = t.split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    low = []   # 大根堆（存负值）
    high = []  # 小根堆
    out = []
    for x in a:
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)
        while len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        while len(low) < len(high):
            heapq.heappush(low, -heapq.heappop(high))
        if (len(low) + len(high)) % 2 == 1:
            out.append(str(-low[0]))
        else:
            out.append(str(high[0]))
    return "\n".join(out)


add(id="p-16-04", chapter=16, label="习题 16-4", title="动态中位数（取较大者）",
    difficulty=3,
    statement_md="读入 n 个整数，每读一个就输出当前已读入数字的中位数；元素个数为偶数时，输出较大的那个中位数。\n\n本题是第 16 章习题 4：把例题 16-3 改成「偶数个时输出较大的中位数」，需要改哪几行？",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="共 n 行，第 i 行表示读完前 i 个数后的中位数。",
    constraints_md="1 ≤ n ≤ 10^5。",
    hint_md="对顶堆：左边大根堆、右边小根堆；保持左堆元素不少于右堆。偶数个时答案是右堆堆顶。",
    tags=["堆", "中位数"],
    cases=["5\n1 3 2 6 5", "1\n7", "4\n1 2 3 4", "5\n5 4 3 2 1", "6\n2 2 2 2 2 2"],
    solve=p1604)
