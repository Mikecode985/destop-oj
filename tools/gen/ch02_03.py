#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 2～3 章可编程习题。"""

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 2 章
def p0204(t):
    lines = t.strip().splitlines()
    n = int(lines[0])
    items = []
    for idx, ln in enumerate(lines[1:1 + n]):
        name, price = ln.rsplit(" ", 1)
        items.append((int(price), -idx, name, idx))
    # 选择排序思路：每轮选当前价格最高（同价取出现更早）的一个
    chosen = []
    pool = items[:]
    for _ in range(min(3, n)):
        best = 0
        for i in range(1, len(pool)):
            if (pool[i][0], -pool[i][3]) > (pool[best][0], -pool[best][3]):
                best = i
        chosen.append(pool.pop(best))
    return "\n".join("%s %d" % (c[2], c[0]) for c in chosen)


add(id="p-02-04", chapter=2, label="习题 2-4", title="价格最高的三个摊位",
    difficulty=2,
    statement_md="青云市集有 n 个摊位，每个摊位有一个名字和一个单价。请输出价格最高的 3 个摊位（不足 3 个就全部输出），按价格从高到低排列；价格相同时，先出现的摊位排在前面。\n\n本题是第 2 章习题 4：要求不用 `sort`，借用选择排序的思路，每一轮从剩下的摊位里挑出价格最高的一个。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 1000）。\n接下来 n 行，每行「摊位名 单价」，摊位名不含空格。",
    output_md="最多 3 行，每行「摊位名 单价」，按价格从高到低输出。",
    constraints_md="1 ≤ n ≤ 1000，1 ≤ 单价 ≤ 10^9。",
    hint_md="外层循环 3 次，内层在未选过的摊位里找最大；同价时比较出现次序。",
    tags=["选择排序", "结构体"],
    cases=["6\n丝娃娃 18\n肠旺面 12\n烤脑花 25\n恋爱豆腐果 8\n牛肉粉 13\n酸汤鱼 45",
           "2\nA 5\nB 7", "4\nA 10\nB 10\nC 9\nD 10",
           "5\nA 1\nB 1\nC 1\nD 1\nE 1"],
    solve=p0204)

def p0205(t):
    lines = t.strip().splitlines()
    m = int(lines[0])
    items = []
    for ln in lines[1:1 + m]:
        name, price = ln.rsplit(" ", 1)
        items.append((int(price), name))
    items.sort()
    return "\n".join("%s %d" % (nm, pr) for pr, nm in items)


add(id="p-02-05", chapter=2, label="习题 2-5", title="名称带空格的摊位排序",
    difficulty=3,
    statement_md="输入 m 行，每行是「地点名称 单价」，名称中可能含有空格，价格在行末。请按单价升序输出；单价相同时按名称的字典序升序输出。\n\n本题是第 2 章习题 5：练习用 `getline` 读整行，再用 `rfind(' ')` 从后往前找最后一个空格，把价格切出来。",
    input_md="第一行一个整数 m（1 ≤ m ≤ 10^5）。\n接下来 m 行，每行以「名称 空格 单价」的形式给出，名称内可能含空格，单价是行末的整数。",
    output_md="共 m 行，每行「名称 单价」，按题目要求的顺序输出。",
    constraints_md="1 ≤ m ≤ 10^5，1 ≤ 单价 ≤ 10^9；名称长度不超过 100。",
    hint_md="`getline` 读整行，`rfind(' ')` 找最后一个空格，前半段是名称，后半段用 `stoi` 转价格。",
    tags=["字符串", "排序"],
    cases=["4\n喷水池 地铁站 3\n青岩古镇 北门 2\n花溪公园 正门 2\n贵阳北站 1",
           "3\nA B 10\nA A 10\nA 5", "1\nOnly Name 7",
           "5\nx y z 1\nx y 2\nx 1\nx y z 1\nx 0"],
    solve=p0205)

# ================================================================ 第 3 章
def p0301(t):
    d = t.split()
    n = int(d[0])
    a = sorted(set(map(int, d[1:1 + n])))
    return "%d\n%s" % (len(a), " ".join(map(str, a)))


add(id="p-03-01", chapter=3, label="习题 3-1", title="去重后按升序输出",
    difficulty=1,
    statement_md="输入 n 个整数，去重后按升序输出。要求用 `vector` + `sort` + `unique`，不许用 `set`。\n\n本题是第 3 章习题 1。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数（1 ≤ a[i] ≤ 10^9）。",
    output_md="第一行一个整数 k，表示不同数的个数。\n第二行 k 个整数，按升序输出，相邻两数用一个空格隔开。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ a[i] ≤ 10^9。",
    hint_md="`sort` 之后 `unique` 把重复元素挪到末尾，返回新的逻辑尾指针，再 `erase`。",
    tags=["STL", "去重"],
    cases=["6\n5 2 5 1 2 8", "1\n7", "5\n1 1 1 1 1", "4\n4 3 2 1"],
    solve=p0301)

def p0302(t):
    lines = t.strip().splitlines()
    n = int(lines[0])
    mp = {}
    for nm in lines[1:1 + n]:
        nm = nm.strip()
        mp[nm] = mp.get(nm, 0) + 1
    return "\n".join("%s %d" % (k, mp[k]) for k in sorted(mp))


add(id="p-03-02", chapter=3, label="习题 3-2", title="名字出现次数",
    difficulty=1,
    statement_md="输入 n 个名字（不含空格），统计每个名字出现的次数，按名字的字典序输出「名字 次数」。\n\n本题是第 3 章习题 2。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行一个不含空格的名字。",
    output_md="若干行，每行「名字 次数」，按名字字典序升序输出。",
    constraints_md="1 ≤ n ≤ 10^5，名字长度不超过 20。",
    hint_md="`map<string,int>` 计数，遍历 map 时天然按 key 升序。",
    tags=["map"],
    cases=["6\napple\nbanana\napple\ncherry\nbanana\napple", "1\nzz",
           "4\nb\na\nb\na", "3\nZ\na\nA"],
    solve=p0302)

def p0303(t):
    d = t.split()
    p = 0
    n, m = int(d[p]), int(d[p + 1]); p += 2
    out = []
    for _ in range(n):
        row = list(map(int, d[p:p + m])); p += m
        out.append(str(sum(row)))
    return "\n".join(out)


add(id="p-03-03", chapter=3, label="习题 3-3", title="矩阵每行元素之和",
    difficulty=1,
    statement_md="输入一个 n 行 m 列的整数矩阵，用 `vector<vector<int>>` 存起来，输出每一行元素之和。\n\n本题是第 3 章习题 3。",
    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行 m 个整数（|a[i][j]| ≤ 10^9）。",
    output_md="共 n 行，每行一个整数，表示对应行元素之和。",
    constraints_md="1 ≤ n, m ≤ 1000，|a[i][j]| ≤ 10^9，行和可能超过 `int`。",
    hint_md="读入时直接累加该行，注意用 `long long`。",
    tags=["vector", "矩阵"],
    cases=["2 3\n1 2 3\n4 5 6", "1 1\n-1000000000", "3 2\n1000000000 1000000000\n0 0\n-1 -1",
           "2 2\n1 -1\n2 -2"],
    solve=p0303)

def p0305(t):
    lines = t.strip().splitlines()
    m = int(lines[0])
    items = []
    for ln in lines[1:1 + m]:
        name, cat, price = ln.rsplit(" ", 2)
        items.append((cat, int(price), name))
    items.sort()
    return "\n".join("%s %s %d" % (cat, nm, pr) for cat, pr, nm in items)


add(id="p-03-05", chapter=3, label="习题 3-5", title="市集摊位分组排序",
    difficulty=3,
    statement_md="青云市集有 m 个摊位，每个摊位有名称、类别、单价。要求先按类别分组，组内按单价升序、单价相同按名称升序，输出排序后的结果。\n\n本题是第 3 章习题 5：提示用 `map<string, vector<Stall>>` 分组，再对每个 `vector` 排序。",
    input_md="第一行一个整数 m（1 ≤ m ≤ 10^5）。\n接下来 m 行，每行「名称 类别 单价」，名称与类别都不含空格。",
    output_md="共 m 行，每行「类别 名称 单价」，按类别字典序、组内价格升序、同价名称升序输出。",
    constraints_md="1 ≤ m ≤ 10^5，1 ≤ 单价 ≤ 10^9。",
    hint_md="用 `map<string, vector<pair<int,string>>>` 分组，再逐组 `sort`。",
    tags=["map", "分组排序"],
    cases=["5\n丝娃娃 小吃 18\n肠旺面 小吃 12\n烤脑花 烧烤 25\n牛肉粉 小吃 12\n豆腐果 烧烤 8",
           "4\nb B 2\na A 1\nc B 1\nd A 2", "1\nx X 9"],
    solve=p0305)
