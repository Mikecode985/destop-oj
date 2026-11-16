#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""贵阳生活 100 题（v2）：100 道题各自有独立的问法与输入输出。

设计原则：
- 每个题族 5 道题，但 5 道题问的东西不同（求和 / 计数 / 排序 / 查询 / 方案数……），
  不是把同一道题换个地名；
- 题材来自贵阳真实的地点、食物、交通与生活细节，题面里写清楚情境和规则；
- 每题给出标准输入输出、样例、6 组测试、分层提示、C++17 参考解；
- 参考解统一 #include <bits/stdc++.h>。
"""
import math
import random

PROBLEMS = []
SOL = {}

LABELS = {1: "入门", 2: "基础", 3: "提高", 4: "进阶", 5: "挑战"}


def _lines(t):
    return [x.strip() for x in str(t).replace("\r", "").split("\n") if x.strip()]


def V(task, inp, outp, cons, tags, diff, h1, h2, h3=""):
    hints = [h for h in (h1, h2, h3) if h]
    return {
        "task": task, "input": inp, "output": outp, "cons": cons,
        "tags": tags, "diff": diff, "hints": hints,
    }


def fam(key, stories, variants, cpp, solve, rand):
    assert len(stories) == 5 and len(variants) == 5
    FAMILIES.append({
        "key": key, "stories": stories, "variants": variants,
        "cpp": cpp, "solve": solve, "rand": rand,
    })


FAMILIES = []

# ======================================================================
# 每个题族用 rand(v, rng) 生成输入；solve(v, text) 生成期望输出。
# C++ 参考解里用 @MODE@ 标记变体编号。
# ======================================================================

# 1. 数组账本：5 道题分别问总和/正负、加权、平方和、交错和
SUM_STORIES = [
    ("青云路夜市的摊位账本",
     "青云路夜市收摊后，管理员老周把 30 多个摊位的营业额按摊位号记在本子上：有的摊位卖丝娃娃，有的卖烤脑花，也有的只摆了两小时。"),
    ("贵阳北站夜间接驳的流水",
     "夜里十一点，贵阳北站的网约车调度室还在算账。调度员把每个小时的接单量记成一串数，想看看夜间接驳到底是赚是亏。"),
    ("修文猕猴桃分筐过秤",
     "修文县谷堡镇的果农把刚摘的猕猴桃按筐过秤。每筐重量不一样，装箱前要先算清楚总重量和平均水平。"),
    ("花果园快递柜的格口账本",
     "花果园半山小镇的快递柜分成很多格口，物业按格口号记录了当天每个格口的取件次数。格口越多，越要算清楚整体使用情况。"),
    ("地铁 1 号线的早高峰客流",
     "贵阳地铁 1 号线从窦官到小孟工业园一共 25 站。早高峰结束后，每站都报来了上车人数，调度中心想从中看出全线客流的节奏。"),
]


def rand_sum(v, rng):
    n = rng.randint(5, 12)
    if v == 1:
        a = [rng.randint(-20, 80) for _ in range(n)]
    elif v == 4:
        a = [rng.randint(0, 60) for _ in range(n)]
    else:
        a = [rng.randint(0, 100) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_sum(v, t):
    d = list(map(int, t.split()))
    n = d[0]
    a = d[1:1 + n]
    if v == 0:
        return "%d\n%d" % (sum(a), a.index(max(a)) + 1)
    if v == 1:
        return "%d\n%d" % (sum(x for x in a if x > 0), sum(1 for x in a if x <= 0))
    if v == 2:
        return str(sum(x * (i + 1) for i, x in enumerate(a)))
    if v == 3:
        return str(sum(x * x for x in a))
    return str(sum(x if i % 2 == 0 else -x for i, x in enumerate(a)))


SUM_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n; cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    if (MODE == 0) {
        long long s = 0, best = a[0]; int pos = 1;
        for (int i = 0; i < n; i++) {
            s += a[i];
            if (a[i] > best) { best = a[i]; pos = i + 1; }
        }
        cout << s << "\n" << pos << "\n";
    } else if (MODE == 1) {
        long long pos = 0, non = 0;
        for (long long x : a) { if (x > 0) pos += x; else non++; }
        cout << pos << "\n" << non << "\n";
    } else if (MODE == 2) {
        long long s = 0;
        for (int i = 0; i < n; i++) s += a[i] * (i + 1);
        cout << s << "\n";
    } else if (MODE == 3) {
        long long s = 0;
        for (long long x : a) s += x * x;
        cout << s << "\n";
    } else {
        long long s = 0;
        for (int i = 0; i < n; i++) s += (i % 2 == 0 ? a[i] : -a[i]);
        cout << s << "\n";
    }
    return 0;
}
"""

fam("sum", SUM_STORIES, [
    V("求今晚营业额总和，以及营业额最高的第一个摊位号。",
      "第一行一个整数 n（5 ≤ n ≤ 12），第二行 n 个整数，依次是每个摊位的营业额。",
      "第一行一个整数表示总和，第二行一个整数表示第一个最大值的摊位号（从 1 开始）。",
      "5 ≤ n ≤ 12，0 ≤ 营业额 ≤ 100；总和不超过 1200。",
      ["求和", "模拟"], 1,
      "边读边累加，同时记录目前最大的值和它的位置。",
      "最大值有并列时，保留最先出现的那个位置。"),
    V("分别算出夜间正营收的总额，以及没有产生正营收的小时数。",
      "第一行一个整数 n，第二行 n 个整数，可能是负数（表示退单多于接单）。",
      "第一行输出所有正数之和，第二行输出小于等于 0 的小时数。",
      "5 ≤ n ≤ 12，-20 ≤ 数值 ≤ 80。",
      ["求和", "计数"], 1,
      "正负要分开处理，小于等于 0 都算“没有正营收”。",
      "用两个变量：一个累加正数，一个数非正数。"),
    V("按筐号给每筐猕猴桃加权：第 i 筐的重量乘以 i，再全部相加，得到装箱调度用的加权总量。",
      "第一行一个整数 n，第二行 n 个整数，第 i 个数是第 i 筐的重量（单位：斤）。",
      "输出一个整数，表示 Σ(第 i 筐重量 × i)。",
      "5 ≤ n ≤ 12，0 ≤ 每筐重量 ≤ 100。",
      ["求和", "模拟"], 1,
      "第 i 筐的权重就是 i，从 1 开始编号。",
      "边读边乘，不要先把所有乘积存下来。"),
    V("物业想评估格口负载是否均衡，请算出每个格口取件次数的平方和。",
      "第一行一个整数 n，第二行 n 个整数，表示每个格口的取件次数。",
      "输出一个整数，表示所有取件次数的平方和。",
      "5 ≤ n ≤ 12，0 ≤ 次数 ≤ 100。",
      ["求和", "模拟"], 1,
      "平方和就是每个数自己乘自己，再全部相加。",
      "结果最大约 12×100²，用 long long 更稳妥。"),
    V("地铁客流有“进站多、出站少”的波动，调度员用交错和 a1-a2+a3-a4+… 描述这种节奏，请算出差值。",
      "第一行一个整数 n，第二行 n 个整数，表示各站上车人数。",
      "输出一个整数，表示 a1 - a2 + a3 - a4 + … 的结果（奇数位取正，偶数位取负）。",
      "5 ≤ n ≤ 12，0 ≤ 人数 ≤ 60。",
      ["求和", "模拟"], 1,
      "从 1 开始编号，奇数位加、偶数位减。",
      "结果可能是负数，直接输出即可。"),
], SUM_CPP, solve_sum, rand_sum)

# 2. 计数：阈值、区间、尾号、去重、恰好命中
COUNT_STORIES = [
    ("贵阳的雨到底下了几天",
     "贵阳人说“天无三日晴”。气象站把连续 n 天的降雨量记在本子上，只有达到 k 毫米才算一场有效降雨。"),
    ("黔灵山猕猴的体重普查",
     "黔灵山公园的饲养员给一群猕猴称体重。猴子们挤在秤边抢花生，记录下来的体重高高低低。"),
    ("数博会入口的尾号分流",
     "数博会开幕当天，入口按预约号尾号分流。工作人员发现，尾号相同的观众走同一个通道，队伍长短差别很大。"),
    ("观山湖晨跑团的花名册",
     "观山湖公园北门有一支晨跑团，每天打卡的人不一样。团长想把坚持打卡的人和偶尔来的人分开统计。"),
    ("青岩古镇客栈的满房日",
     "青岩古镇一家客栈记录了连续 n 天的入住房间数。老板想知道，刚好住满 k 间的日子有几天，以及第一次出现在哪天。"),
]


def rand_count(v, rng):
    n = rng.randint(5, 14)
    a = [rng.randint(0, 60) for _ in range(n)]
    if v == 0:
        k = rng.randint(10, 50)
        return "%d %d\n%s" % (n, k, " ".join(map(str, a)))
    if v == 1:
        l = rng.randint(0, 25); r = rng.randint(l, 55)
        return "%d %d %d\n%s" % (n, l, r, " ".join(map(str, a)))
    if v == 2:
        d = rng.randint(0, 9)
        return "%d %d\n%s" % (n, d, " ".join(map(str, a)))
    if v == 4:
        k = rng.choice(a)
        return "%d %d\n%s" % (n, k, " ".join(map(str, a)))
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_count(v, t):
    d = list(map(int, t.split()))
    n = d[0]
    if v == 0:
        k = d[1]; a = d[2:2 + n]
        return str(sum(1 for x in a if x >= k))
    if v == 1:
        l, r = d[1], d[2]; a = d[3:3 + n]
        return str(sum(1 for x in a if l <= x <= r))
    if v == 2:
        q = d[1]; a = d[2:2 + n]
        return str(sum(1 for x in a if abs(x) % 10 == q))
    if v == 3:
        a = d[1:1 + n]
        return str(len(set(a)))
    a = d[2:2 + n]; k = d[1]
    pos = next((i + 1 for i, x in enumerate(a) if x == k), 0)
    return "%d\n%d" % (a.count(k), pos)


COUNT_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n; cin >> n;
    if (MODE == 0) {
        int k, cnt = 0; cin >> k;
        for (int i = 0; i < n; i++) { int x; cin >> x; if (x >= k) cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 1) {
        int l, r, cnt = 0; cin >> l >> r;
        for (int i = 0; i < n; i++) { int x; cin >> x; if (l <= x && x <= r) cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 2) {
        int d, cnt = 0; cin >> d;
        for (int i = 0; i < n; i++) { int x; cin >> x; if (abs(x) % 10 == d) cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 3) {
        set<int> s;
        for (int i = 0; i < n; i++) { int x; cin >> x; s.insert(x); }
        cout << s.size() << "\n";
    } else {
        int k, cnt = 0, first = 0;
        cin >> k;
        for (int i = 1; i <= n; i++) {
            int x; cin >> x;
            if (x == k) { cnt++; if (!first) first = i; }
        }
        cout << cnt << "\n" << first << "\n";
    }
    return 0;
}
"""

fam("count", COUNT_STORIES, [
    V("统计降雨量达到 k 毫米的有效雨天数。",
      "第一行两个整数 n 和 k，第二行 n 个整数表示每天的降雨量。",
      "输出一个整数，表示降雨量 ≥ k 的天数。",
      "5 ≤ n ≤ 14，0 ≤ 降雨量 ≤ 60。",
      ["计数", "枚举"], 1,
      "逐个判断，达到 k 就加一。",
      "注意是“大于等于”，等于 k 也算。"),
    V("统计体重落在 [L, R] 千克范围内的猕猴数量。",
      "第一行三个整数 n、L、R，第二行 n 个整数表示每只猴子的体重。",
      "输出一个整数，表示体重在闭区间 [L, R] 内的猴子数。",
      "5 ≤ n ≤ 14，0 ≤ L ≤ R ≤ 55。",
      ["计数", "枚举"], 1,
      "闭区间两端都算，条件写成 L <= x && x <= R。",
      "不要先排序，直接扫一遍即可。"),
    V("统计预约号尾号为 d 的观众人数。",
      "第一行两个整数 n 和 d（0 ≤ d ≤ 9），第二行 n 个非负整数表示预约号。",
      "输出一个整数，表示个位数字等于 d 的预约号数量。",
      "5 ≤ n ≤ 14，0 ≤ 预约号 ≤ 60。",
      ["计数", "取余"], 1,
      "一个数的个位就是它除以 10 的余数。",
      "0 的个位是 0，也要参与统计。"),
    V("统计晨跑团里有多少个不同的打卡人数（同一天来多少人算一个值）。",
      "第一行一个整数 n，第二行 n 个整数表示每天的打卡人数。",
      "输出一个整数，表示不同人数值的个数。",
      "5 ≤ n ≤ 14，0 ≤ 人数 ≤ 60。",
      ["计数", "去重"], 1,
      "把数放进 set，最后看 set 的大小。",
      "重复出现只算一次。"),
    V("统计客栈刚好住满 k 间的天数，以及第一次满房是第几天。",
      "第一行两个整数 n 和 k，第二行 n 个整数表示每天入住的房间数。",
      "第一行输出刚好等于 k 的天数，第二行输出第一次出现的天号（从 1 开始）；没有则输出 0。",
      "5 ≤ n ≤ 14，0 ≤ 入住数 ≤ 60，k 一定在数据中出现过。",
      ["计数", "模拟"], 1,
      "等于 k 才计数，第一次出现时记下天号。",
      "用 0 表示还没出现过。"),
], COUNT_CPP, solve_count, rand_count)

# 3. 排序：多关键字、前三名、中位数、第 k 小、最接近
SORT_STORIES = [
    ("青云路小吃的价目表",
     "青云路夜市的小吃摊一家挨着一家：丝娃娃、烤脑花、豆腐圆子、洋芋粑。管理员要把摊名和价格整理成一张价目表。"),
    ("花溪大学城食堂窗口评分",
     "花溪大学城食堂有十几个窗口，学生们给每个窗口打了分。食堂想先公布评分最高的三个窗口。"),
    ("青岩古镇伴手礼的价格中位数",
     "青岩古镇的伴手礼店把玫瑰糖、鸡辣角、状元蹄摆了一排。店长想用一个“中间价”判断整条街的价格水平。"),
    ("地铁沿线二手房的第 k 低价",
     "房产中介整理了一批地铁沿线小区，每个小区有一个挂牌总价。买家只关心第 k 便宜的房源大概是什么价位。"),
    ("数博会展位的最近面积",
     "数博会展馆里，各参展商报来的展位面积大小不一。工作人员要找一个面积最接近目标值 T 的展位，方便统一搭建。"),
]


def rand_sort(v, rng):
    names = ["changwang", "siwawa", "kaoluo", "doumi", "lusi", "yangyu", "bingjiang", "suanfen", "naohua", "doufu"]
    if v in (0, 1, 4):
        n = rng.randint(4, 8)
        pick = rng.sample(names, n)
        if v == 0:
            return "%d\n%s" % (n, "\n".join("%s %d" % (x, rng.randint(1, 99)) for x in pick))
        if v == 1:
            return "%d\n%s" % (n, "\n".join("%s %d" % (x, rng.randint(50, 100)) for x in pick))
        target = rng.randint(20, 80)
        return "%d %d\n%s" % (target, n, "\n".join("%s %d" % (x, rng.randint(1, 99)) for x in pick))
    n = rng.randint(5, 12)
    a = [rng.randint(0, 100) for _ in range(n)]
    if v == 3:
        return "%d %d\n%s" % (n, rng.randint(1, n), " ".join(map(str, a)))
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_sort(v, t):
    lines = _lines(t)
    if v == 0:
        n = int(lines[0]); rows = [x.split() for x in lines[1:1 + n]]
        rows = sorted((int(b), a) for a, b in rows)
        return "\n".join("%s %d" % (name, val) for val, name in rows)
    if v == 1:
        n = int(lines[0]); rows = [x.split() for x in lines[1:1 + n]]
        rows = sorted(((int(b), a) for a, b in rows), key=lambda x: (-x[0], x[1]))[:3]
        return "\n".join("%s %d" % (name, val) for val, name in rows)
    if v == 4:
        target, n = map(int, lines[0].split())
        rows = [x.split() for x in lines[1:1 + n]]
        rows = [(a, int(b)) for a, b in rows]
        best = min(rows, key=lambda x: (abs(x[1] - target), x[0]))
        return "%s %d" % (best[0], abs(best[1] - target))
    if v == 2:
        n = int(lines[0]); a = list(map(int, lines[1].split()))
        a.sort()
        return str(a[(n - 1) // 2])
    n, k = map(int, lines[0].split())
    a = list(map(int, lines[1].split()))
    a.sort()
    return str(a[k - 1])


SORT_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    if (MODE == 0) {
        int n; cin >> n;
        vector<pair<int, string>> v;
        for (int i = 0; i < n; i++) { string s; int x; cin >> s >> x; v.push_back({x, s}); }
        sort(v.begin(), v.end());
        for (auto &p : v) cout << p.second << " " << p.first << "\n";
    } else if (MODE == 1) {
        int n; cin >> n;
        vector<pair<int, string>> v;
        for (int i = 0; i < n; i++) { string s; int x; cin >> s >> x; v.push_back({-x, s}); }
        sort(v.begin(), v.end());
        for (int i = 0; i < min(3, n); i++) cout << v[i].second << " " << -v[i].first << "\n";
    } else if (MODE == 2) {
        int n; cin >> n; vector<int> a(n);
        for (int &x : a) cin >> x;
        sort(a.begin(), a.end());
        cout << a[(n - 1) / 2] << "\n";
    } else if (MODE == 3) {
        int n, k; cin >> n >> k; vector<int> a(n);
        for (int &x : a) cin >> x;
        sort(a.begin(), a.end());
        cout << a[k - 1] << "\n";
    } else {
        int t, n; cin >> t >> n;
        string bests; int bestd = INT_MAX; int bestv = 0;
        for (int i = 0; i < n; i++) {
            string s; int x; cin >> s >> x;
            int d = abs(x - t);
            if (d < bestd || (d == bestd && s < bests)) { bestd = d; bests = s; bestv = x; }
        }
        cout << bests << " " << bestd << "\n";
    }
    return 0;
}
"""

fam("sort", SORT_STORIES, [
    V("把摊名和价格按价格从低到高输出；价格相同的，按摊名（拼音）从 A 到 Z。",
      "第一行一个整数 n，接下来 n 行，每行一个拼音摊名和一个整数价格。",
      "输出 n 行，每行“摊名 价格”，按价格升序、同价按摊名升序。",
      "4 ≤ n ≤ 8，摊名为小写字母，1 ≤ 价格 ≤ 99。",
      ["排序", "多关键字"], 1,
      "把 (价格, 摊名) 组成 pair，直接 sort。",
      "pair 默认先比第一个，再比第二个正好符合要求。"),
    V("公布评分最高的 3 个窗口，按评分从高到低；同分按窗口名从 A 到 Z。",
      "第一行一个整数 n，接下来 n 行，每行一个窗口名和一个整数评分。",
      "输出不超过 3 行，每行“窗口名 评分”。",
      "4 ≤ n ≤ 8，评分 50～100。",
      ["排序", "多关键字"], 1,
      "按 (-评分, 窗口名) 排序，取前 3 个。",
      "不足 3 个窗口时全部输出。"),
    V("求所有伴手礼价格的下中位数（排序后第 ⌊(n-1)/2⌋ 个，下标从 0 开始）。",
      "第一行一个整数 n，第二行 n 个整数表示价格。",
      "输出一个整数，表示下中位数。",
      "5 ≤ n ≤ 12，0 ≤ 价格 ≤ 100。",
      ["排序", "中位数"], 1,
      "先排序，再取下标 (n-1)/2 的元素。",
      "偶数个时取偏小的那个，不是两个数的平均。"),
    V("求所有挂牌价中第 k 便宜的价格。",
      "第一行两个整数 n 和 k，第二行 n 个整数表示挂牌价。",
      "输出一个整数，表示第 k 小的价格（1 ≤ k ≤ n）。",
      "5 ≤ n ≤ 12，0 ≤ 价格 ≤ 100。",
      ["排序", "第 k 小"], 1,
      "排序后直接取 a[k-1]。",
      "注意 k 从 1 开始，数组下标从 0 开始。"),
    V("找面积最接近目标 T 的展位；距离相同取名称字典序更小的。输出名称和面积差。",
      "第一行两个整数 T 和 n，接下来 n 行，每行一个展位名和一个整数面积。",
      "输出一行“展位名 面积差”。",
      "1 ≤ T ≤ 100，4 ≤ n ≤ 8，面积 1～99。",
      ["排序", "枚举"], 2,
      "逐个算 |面积-T|，同时维护最小差值和对应名称。",
      "差值相同时比较名称字符串，不要只比较面积。"),
], SORT_CPP, solve_sort, rand_sort)



# 4. 区间查询：和、最大、最小、平均、异或
RANGE_STORIES = [
    ("南明河分段水质监测",
     "南明河从城市中间穿过，监测站把河道分成 n 段，每段取一个水质指标。巡河员常要问某一段连续河道的总指标。"),
    ("地铁 1 号线区间客流",
     "地铁 1 号线的相邻站点之间是一段段区间。调度中心把每段区间的客流记下来，想快速知道任意连续几段的最大客流。"),
    ("观山湖跑道分段计时",
     "观山湖公园的跑道被分成若干段，每段有一个计时点。教练要找出某一段连续跑道里用时最少的一段。"),
    ("黔灵山台阶的平均爬升",
     "黔灵山的一条登山步道被分成 n 段，每段有固定爬升高度。游客问“从第 l 段到第 r 段，平均每段要爬多少”。"),
    ("花果园楼栋的公摊电费异或核对",
     "花果园一栋楼的各层公摊电费录入系统后，物业用“区间异或”做快速核对：把一段连续楼层的数值异或起来，看是否和账单吻合。"),
]


def rand_range(v, rng):
    n = rng.randint(5, 12)
    q = rng.randint(3, 7)
    a = [rng.randint(0, 60) for _ in range(n)]
    qs = []
    for _ in range(q):
        l = rng.randint(1, n); r = rng.randint(l, n)
        qs.append((l, r))
    return "%d %d\n%s\n%s" % (n, q, " ".join(map(str, a)),
                              "\n".join("%d %d" % x for x in qs))


def solve_range(v, t):
    d = list(map(int, t.split()))
    n, q = d[0], d[1]
    a = d[2:2 + n]
    out = []
    idx = 2 + n
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    px = [0]
    for x in a:
        px.append(px[-1] ^ x)
    for _ in range(q):
        l, r = d[idx], d[idx + 1]; idx += 2
        seg = a[l - 1:r]
        if v == 0:
            out.append(str(pre[r] - pre[l - 1]))
        elif v == 1:
            out.append(str(max(seg)))
        elif v == 2:
            out.append(str(min(seg)))
        elif v == 3:
            out.append(str((pre[r] - pre[l - 1]) // (r - l + 1)))
        else:
            out.append(str(px[r] ^ px[l - 1]))
    return "\n".join(out)


RANGE_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, q; cin >> n >> q;
    vector<long long> a(n + 1), pre(n + 1, 0), px(n + 1, 0);
    for (int i = 1; i <= n; i++) { cin >> a[i]; pre[i] = pre[i - 1] + a[i]; px[i] = px[i - 1] ^ a[i]; }
    while (q--) {
        int l, r; cin >> l >> r;
        if (MODE == 0) cout << pre[r] - pre[l - 1] << "\n";
        else if (MODE == 1) {
            long long mx = a[l];
            for (int i = l; i <= r; i++) mx = max(mx, a[i]);
            cout << mx << "\n";
        } else if (MODE == 2) {
            long long mn = a[l];
            for (int i = l; i <= r; i++) mn = min(mn, a[i]);
            cout << mn << "\n";
        } else if (MODE == 3) {
            cout << (pre[r] - pre[l - 1]) / (r - l + 1) << "\n";
        } else {
            cout << (px[r] ^ px[l - 1]) << "\n";
        }
    }
    return 0;
}
"""

fam("range", RANGE_STORIES, [
    V("回答每次询问：第 l 段到第 r 段的总指标是多少。",
      "第一行两个整数 n 和 q；第二行 n 个整数；接下来 q 行每行 l r。",
      "对每次询问输出一行一个整数，表示区间和。",
      "5 ≤ n ≤ 12，1 ≤ q ≤ 7，0 ≤ 指标 ≤ 60。",
      ["前缀和", "区间查询"], 2,
      "用前缀和 pre[i]=a[1]+…+a[i]，区间和就是 pre[r]-pre[l-1]。",
      "下标从 1 开始，pre[0]=0。"),
    V("回答每次询问：第 l 段到第 r 段的最大客流是多少。",
      "第一行两个整数 n 和 q；第二行 n 个整数；接下来 q 行每行 l r。",
      "对每次询问输出一行一个整数，表示区间最大值。",
      "5 ≤ n ≤ 12，1 ≤ q ≤ 7，0 ≤ 客流 ≤ 60。",
      ["区间查询", "枚举"], 2,
      "数据很小，直接在这段里扫一遍找最大值即可。",
      "也可以先想 ST 表，但这题 O(nq) 足够。"),
    V("回答每次询问：第 l 段到第 r 段的用时最少是多少。",
      "第一行两个整数 n 和 q；第二行 n 个整数；接下来 q 行每行 l r。",
      "对每次询问输出一行一个整数，表示区间最小值。",
      "5 ≤ n ≤ 12，1 ≤ q ≤ 7，0 ≤ 计时 ≤ 60。",
      ["区间查询", "枚举"], 2,
      "和区间最大值相反，初值设成很大，再逐个取 min。",
      "注意区间只有一段时也要正确输出该元素。"),
    V("回答每次询问：第 l 段到第 r 段平均每段爬升多少（向下取整）。",
      "第一行两个整数 n 和 q；第二行 n 个整数；接下来 q 行每行 l r。",
      "对每次询问输出一行一个整数，表示区间和除以区间长度的整数结果。",
      "5 ≤ n ≤ 12，1 ≤ q ≤ 7，0 ≤ 爬升 ≤ 60。",
      ["前缀和", "整除"], 2,
      "先算区间和，再除以 (r-l+1)。",
      "C++ 的整数除法天然向下取整。"),
    V("回答每次询问：第 l 段到第 r 段所有指标异或起来是多少。",
      "第一行两个整数 n 和 q；第二行 n 个整数；接下来 q 行每行 l r。",
      "对每次询问输出一行一个整数，表示区间异或和。",
      "5 ≤ n ≤ 12，1 ≤ q ≤ 7，0 ≤ 指标 ≤ 60。",
      ["前缀异或", "区间查询"], 2,
      "异或的前缀和满足 px[r]^px[l-1] 等于区间异或。",
      "不要用加法前缀和代替，异或没有减法逆运算。"),
], RANGE_CPP, solve_range, rand_range)

# 5. 区间加：最大总和、最终数组、达标个数、最值、单点
RANGEADD_STORIES = [
    ("观山湖灯会的临时摊位",
     "观山湖灯会沿湖设了 n 个点位。每来一批临时摊位，就会让 [l, r] 连续点位的预计人流增加 x 人。灯会结束后要报最大人流和总人流。"),
    ("南明河清淤的分段施工",
     "南明河清淤按段施工。每次施工让 [l, r] 段的浑浊度增加 x，全部完工后要公布每一段的最终浑浊度。"),
    ("地铁站出入口的活动叠加",
     "地铁站有 n 个出入口。活动期间，一批批乘客从 [l, r] 连续出入口进入，每个出入口增加 x 人。安保组要知道最终有多少个出入口超过警戒值 T。"),
    ("老小区加装电梯的补贴",
     "某街道有 n 个单元申请加装电梯。每批批复给 [l, r] 单元每户增加 x 元补贴。全部批复后，要报单户补贴的最低和最高值。"),
    ("青云路夜市的油烟监测",
     "青云路夜市有 n 个摊位。每次集中烹饪会让 [l, r] 摊位的油烟值增加 x。环保员只想查其中一个摊位的最终油烟值。"),
]


def rand_rangeadd(v, rng):
    n = rng.randint(5, 12)
    m = rng.randint(3, 7)
    a = [rng.randint(0, 30) for _ in range(n)]
    ops = []
    for _ in range(m):
        l = rng.randint(1, n); r = rng.randint(l, n)
        ops.append((l, r, rng.randint(1, 15)))
    first = "%d %d" % (n, m)
    if v in (2, 4):
        first += " %d" % (rng.randint(5, 40) if v == 2 else rng.randint(1, n))
    return "%s\n%s\n%s" % (first, " ".join(map(str, a)),
                           "\n".join("%d %d %d" % x for x in ops))


def solve_rangeadd(v, t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    p = d[2] if v in (2, 4) else None
    a = d[3:3 + n] if p is not None else d[2:2 + n]
    base = 3 + n if p is not None else 2 + n
    diff = [0] * (n + 2)
    for i in range(m):
        l, r, x = d[base + 3 * i], d[base + 3 * i + 1], d[base + 3 * i + 2]
        diff[l] += x; diff[r + 1] -= x
    cur = 0; vals = []
    for i in range(1, n + 1):
        cur += diff[i]; vals.append(a[i - 1] + cur)
    if v == 0:
        return "%d %d" % (max(vals), sum(vals))
    if v == 1:
        return " ".join(map(str, vals))
    if v == 2:
        return str(sum(1 for x in vals if x >= p))
    if v == 3:
        return "%d %d" % (min(vals), max(vals))
    return str(vals[p - 1])


RANGEADD_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, m; cin >> n >> m;
    int p = 0;
    if (MODE == 2 || MODE == 4) cin >> p;
    vector<long long> a(n + 1), d(n + 2, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 0; i < m; i++) {
        int l, r, x; cin >> l >> r >> x;
        d[l] += x; d[r + 1] -= x;
    }
    for (int i = 1; i <= n; i++) d[i] += d[i - 1], a[i] += d[i];
    if (MODE == 0) {
        long long mx = a[1], s = 0;
        for (int i = 1; i <= n; i++) { mx = max(mx, a[i]); s += a[i]; }
        cout << mx << " " << s << "\n";
    } else if (MODE == 1) {
        for (int i = 1; i <= n; i++) cout << a[i] << (i == n ? "\n" : " ");
    } else if (MODE == 2) {
        int cnt = 0;
        for (int i = 1; i <= n; i++) if (a[i] >= p) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 3) {
        cout << *min_element(a.begin() + 1, a.end()) << " " << *max_element(a.begin() + 1, a.end()) << "\n";
    } else {
        cout << a[p] << "\n";
    }
    return 0;
}
"""

fam("rangeadd", RANGEADD_STORIES, [
    V("求所有活动结束后的最大点位人流量和全点位人流总和。",
      "第一行两个整数 n、m；第二行 n 个整数表示初始人流；接下来 m 行，每行 l r x，表示 [l, r] 每个点位增加 x。",
      "输出一行两个整数：最大人流和总人流。",
      "5 ≤ n ≤ 12，3 ≤ m ≤ 7，0 ≤ 初始值 ≤ 30，1 ≤ x ≤ 15。",
      ["差分", "区间加"], 2,
      "用差分数组：d[l]+=x，d[r+1]-=x，最后求前缀和还原。",
      "还原后先加初始值，再统计最大与总和。"),
    V("输出全部施工结束后的每一段浑浊度。",
      "第一行两个整数 n、m；第二行 n 个整数；接下来 m 行 l r x。",
      "输出一行 n 个整数，表示最终每一段的值。",
      "5 ≤ n ≤ 12，3 ≤ m ≤ 7，0 ≤ 初始值 ≤ 30，1 ≤ x ≤ 15。",
      ["差分", "还原数组"], 2,
      "差分数组求一遍前缀和就是每段的累计增量。",
      "把增量和原数组逐项相加。"),
    V("统计最终人流达到警戒值 T 的出入口个数。",
      "第一行三个整数 n、m、T；第二行 n 个整数；接下来 m 行 l r x。",
      "输出一个整数，表示最终值 ≥ T 的位置个数。",
      "5 ≤ n ≤ 12，3 ≤ m ≤ 7，1 ≤ T ≤ 40。",
      ["差分", "计数"], 2,
      "先还原最终数组，再逐个和 T 比较。",
      "等于 T 也要计数。"),
    V("求最终每户补贴的最小值和最大值。",
      "第一行两个整数 n、m；第二行 n 个整数；接下来 m 行 l r x。",
      "输出一行两个整数：最小值和最大值。",
      "5 ≤ n ≤ 12，3 ≤ m ≤ 7。",
      ["差分", "最值"], 2,
      "差分还原后扫一遍同时维护 min 和 max。",
      "不要把初始值漏掉。"),
    V("只查第 p 个摊位的最终油烟值。",
      "第一行三个整数 n、m、p；第二行 n 个整数；接下来 m 行 l r x。",
      "输出一个整数，表示第 p 个位置的最终值。",
      "5 ≤ n ≤ 12，3 ≤ m ≤ 7，1 ≤ p ≤ n。",
      ["差分", "单点查询"], 2,
      "可以只维护差分，最后累加到 p 位置。",
      "也可以完整还原数组后输出 a[p]。"),
], RANGEADD_CPP, solve_rangeadd, rand_rangeadd)

# 6. 区间调度：最多场次、覆盖长度、最少删除、合并、最大重叠
INTERVAL_STORIES = [
    ("青云路夜市的过道排班",
     "青云路夜市只有一条公共过道，每个摊位申请一个 [开始, 结束) 的使用时段。同一时刻过道只能给一个摊位用。"),
    ("地铁志愿者的服务时段",
     "贵阳地铁招募志愿者，每人报了一个 [开始, 结束) 的服务时段。车站想把所有报名的服务时间合并成一张总表。"),
    ("青岩古镇讲解员的预约冲突",
     "青岩古镇的讲解员收到一批预约，每个预约占用一个 [开始, 结束) 时段。经理想删掉最少的预约，让剩下的互不冲突。"),
    ("观山湖公园充电桩的占用",
     "观山湖公园的充电桩收到一批占用申请。管理员要把重叠的申请合并成若干段连续占用区间，方便计费。"),
    ("花果园电梯维修的撞车",
     "花果园一栋楼的电梯收到多项维修申请，每项占用一个 [开始, 结束) 时段。物业想知道同一时刻最多有几项维修在同时进行。"),
]


def rand_interval(v, rng):
    n = rng.randint(4, 9)
    seg = []
    for _ in range(n):
        l = rng.randint(0, 18)
        r = l + rng.randint(1, 6)
        seg.append((l, r))
    return "%d\n%s" % (n, "\n".join("%d %d" % x for x in seg))


def solve_interval(v, t):
    lines = _lines(t)
    n = int(lines[0])
    seg = [tuple(map(int, x.split())) for x in lines[1:1 + n]]
    seg.sort(key=lambda x: (x[1], x[0]))
    cnt = 0; last = -10**18
    for l, r in seg:
        if l >= last:
            cnt += 1; last = r
    if v == 0:
        return str(cnt)
    if v == 2:
        return str(n - cnt)
    if v == 1:
        events = []
        for l, r in seg:
            events.append((l, 1)); events.append((r, -1))
        events.sort(key=lambda x: (x[0], x[1]))
        total = 0; cur = 0; prev = events[0][0]
        for x, d in events:
            if cur > 0: total += x - prev
            cur += d; prev = x
        return str(total)
    if v == 3:
        merged = []
        for l, r in sorted(seg):
            if merged and l <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], r)
            else:
                merged.append([l, r])
        return "%d\n%s" % (len(merged), "\n".join("%d %d" % (l, r) for l, r in merged))
    ev = []
    for l, r in seg:
        ev.append((l, 1)); ev.append((r, -1))
    ev.sort(key=lambda x: (x[0], x[1]))
    cur = 0; best = 0
    for _, d in ev:
        cur += d; best = max(best, cur)
    return str(best)


INTERVAL_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n; cin >> n;
    vector<pair<int,int>> s(n);
    for (auto &p : s) cin >> p.first >> p.second;
    if (MODE == 0 || MODE == 2) {
        sort(s.begin(), s.end(), [](auto &a, auto &b) { return a.second < b.second; });
        int cnt = 0, last = INT_MIN;
        for (auto &p : s) if (p.first >= last) { cnt++; last = p.second; }
        cout << (MODE == 0 ? cnt : n - cnt) << "\n";
    } else if (MODE == 1) {
        vector<pair<int,int>> ev;
        for (auto &p : s) { ev.push_back({p.first, 1}); ev.push_back({p.second, -1}); }
        sort(ev.begin(), ev.end());
        long long total = 0; int cur = 0, prev = ev[0].first;
        for (auto &e : ev) {
            if (cur > 0) total += e.first - prev;
            cur += e.second; prev = e.first;
        }
        cout << total << "\n";
    } else if (MODE == 3) {
        sort(s.begin(), s.end());
        vector<pair<int,int>> m;
        for (auto &p : s) {
            if (!m.empty() && p.first <= m.back().second) m.back().second = max(m.back().second, p.second);
            else m.push_back(p);
        }
        cout << m.size() << "\n";
        for (auto &p : m) cout << p.first << " " << p.second << "\n";
    } else {
        vector<pair<int,int>> ev;
        for (auto &p : s) { ev.push_back({p.first, 1}); ev.push_back({p.second, -1}); }
        sort(ev.begin(), ev.end());
        int cur = 0, best = 0;
        for (auto &e : ev) { cur += e.second; best = max(best, cur); }
        cout << best << "\n";
    }
    return 0;
}
"""

fam("interval", INTERVAL_STORIES, [
    V("最多能安排多少个互不冲突的摊位申请？",
      "第一行一个整数 n，接下来 n 行每行 l r，表示占用 [l, r)。",
      "输出一个整数，表示最多能安排的申请数。",
      "4 ≤ n ≤ 9，0 ≤ l < r ≤ 24。",
      ["贪心", "区间调度"], 3,
      "按结束时间从早到晚排序，能接就接。",
      "当前区间的开始时间 >= 上一个选中的结束时间才算不冲突。"),
    V("把所有志愿者的服务时段合并，求一共覆盖了多少单位时间。",
      "第一行一个整数 n，接下来 n 行每行 l r。",
      "输出一个整数，表示所有区间的并集长度（重叠只算一次）。",
      "4 ≤ n ≤ 9，0 ≤ l < r ≤ 24。",
      ["区间合并", "扫描线"], 3,
      "把起点记为 +1、终点记为 -1，按位置扫描。",
      "只有当前覆盖数 > 0 时，这一段才计入总长度。"),
    V("最少删掉多少个预约，才能让剩下的预约互不冲突？",
      "第一行一个整数 n，接下来 n 行每行 l r。",
      "输出一个整数，表示最少删除的预约数。",
      "4 ≤ n ≤ 9，0 ≤ l < r ≤ 24。",
      ["贪心", "区间调度"], 3,
      "先求最多能留下多少个互不冲突的预约。",
      "答案 = n - 最多能留下的数量。"),
    V("把重叠或相接的占用申请合并，输出合并后的区间数量和每个区间。",
      "第一行一个整数 n，接下来 n 行每行 l r。",
      "第一行输出合并后的区间数 k，接下来 k 行每行 l r，按 l 升序。",
      "4 ≤ n ≤ 9，0 ≤ l < r ≤ 24。",
      ["区间合并", "排序"], 3,
      "先按起点排序，再依次判断能否接到上一段末尾。",
      "l <= 上一段 r 时合并，右端点取两者较大值。"),
    V("同一时刻最多有几项电梯维修在同时进行？",
      "第一行一个整数 n，接下来 n 行每行 l r。",
      "输出一个整数，表示最大重叠数。",
      "4 ≤ n ≤ 9，0 ≤ l < r ≤ 24。",
      ["扫描线", "差分"], 3,
      "把每个区间拆成 l 处 +1、r 处 -1。",
      "按位置排序后累加，过程中出现的最大值就是答案。"),
], INTERVAL_CPP, solve_interval, rand_interval)

# 7. 01 背包的五个不同问法
KNAP01_STORIES = [
    ("回贵阳的行李箱",
     "在外地上学的小黔要回贵阳，行李箱最多装 W 千克。他给家里人带了几样特产，每样只有一件。"),
    ("龙洞堡机场的托运行李",
     "龙洞堡机场的免费托运额度是 W 千克。小黔有 n 件行李，每件有重量和价值，每件只能托运一次，而且妈妈要求“必须正好挑 k 件”。"),
    ("花果园搬家的纸箱",
     "花果园搬家时只有一辆能装 W 千克的小推车。n 个纸箱各有重量，师傅想一次尽量多推几个箱子。"),
    ("青岩古镇的伴手礼组合",
     "青岩古镇的伴手礼店有 n 种商品，每种只有一件。小黔的背包最多承受 W 千克，他想知道一共有多少种挑选组合不超重。"),
    ("高坡云顶的露营装备",
     "去高坡云顶露营，背包承重 W 千克。n 件装备各有重量和保暖价值，每件只能带一次，且最多只能带 k 件。"),
]


def rand_knap01(v, rng):
    n = rng.randint(4, 8)
    W = rng.randint(10, 28)
    rows = [(rng.randint(1, 12), rng.randint(1, 50)) for _ in range(n)]
    body = "\n".join("%d %d" % x for x in rows)
    if v in (1, 4):
        K = rng.randint(1, min(3, n))
        return "%d %d %d\n%s" % (n, W, K, body)
    return "%d %d\n%s" % (n, W, body)


def solve_knap01(v, t):
    d = list(map(int, t.split()))
    n, W = d[0], d[1]
    off = 2
    K = d[2] if v in (1, 4) else None
    if v in (1, 4):
        off = 3
    rows = [(d[off + 2 * i], d[off + 2 * i + 1]) for i in range(n)]
    if v == 2:
        ws = sorted(w for w, _ in rows)
        s = 0; cnt = 0
        for w in ws:
            if s + w <= W:
                s += w; cnt += 1
        return str(cnt)
    if v == 3:
        cnt = 0
        for mask in range(1 << n):
            if sum(rows[i][0] for i in range(n) if mask >> i & 1) <= W:
                cnt += 1
        return str(cnt)
    if v == 1:
        dp = [[-1] * (W + 1) for _ in range(K + 1)]
        dp[0][0] = 0
        for w, val in rows:
            for k in range(K - 1, -1, -1):
                for x in range(W - w, -1, -1):
                    if dp[k][x] >= 0:
                        dp[k + 1][x + w] = max(dp[k + 1][x + w], dp[k][x] + val)
        return str(max(0, max(dp[K])))
    if v == 4:
        dp = [[0] * (W + 1) for _ in range(K + 1)]
        for w, val in rows:
            for k in range(K - 1, -1, -1):
                for x in range(W, w - 1, -1):
                    dp[k + 1][x] = max(dp[k + 1][x], dp[k][x - w] + val)
        return str(max(dp[k][x] for k in range(K + 1) for x in range(W + 1)))
    dp = [0] * (W + 1)
    for w, val in rows:
        for x in range(W, w - 1, -1):
            dp[x] = max(dp[x], dp[x - w] + val)
    return str(max(dp))


KNAP01_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, W, K = 0; cin >> n >> W;
    if (MODE == 1 || MODE == 4) cin >> K;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    if (MODE == 0) {
        vector<long long> dp(W + 1, 0);
        for (int i = 0; i < n; i++)
            for (int x = W; x >= w[i]; x--) dp[x] = max(dp[x], dp[x - w[i]] + v[i]);
        cout << *max_element(dp.begin(), dp.end()) << "\n";
    } else if (MODE == 1) {
        vector<vector<long long>> dp(K + 1, vector<long long>(W + 1, -1));
        dp[0][0] = 0;
        for (int i = 0; i < n; i++)
            for (int k = K - 1; k >= 0; k--)
                for (int x = 0; x + w[i] <= W; x++)
                    if (dp[k][x] >= 0) dp[k + 1][x + w[i]] = max(dp[k + 1][x + w[i]], dp[k][x] + v[i]);
        cout << max(0LL, *max_element(dp[K].begin(), dp[K].end())) << "\n";
    } else if (MODE == 2) {
        sort(w.begin(), w.end());
        long long s = 0; int cnt = 0;
        for (int x : w) if (s + x <= W) { s += x; cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 3) {
        long long cnt = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int s = 0;
            for (int i = 0; i < n; i++) if (mask >> i & 1) s += w[i];
            if (s <= W) cnt++;
        }
        cout << cnt << "\n";
    } else {
        vector<vector<long long>> dp(K + 1, vector<long long>(W + 1, 0));
        for (int i = 0; i < n; i++)
            for (int k = K - 1; k >= 0; k--)
                for (int x = W; x >= w[i]; x--)
                    dp[k + 1][x] = max(dp[k + 1][x], dp[k][x - w[i]] + v[i]);
        long long ans = 0;
        for (int k = 0; k <= K; k++) for (int x = 0; x <= W; x++) ans = max(ans, dp[k][x]);
        cout << ans << "\n";
    }
    return 0;
}
"""

fam("knap01", KNAP01_STORIES, [
    V("每样特产最多带一件，求不超过 W 千克时能带走的最高总价值。",
      "第一行两个整数 n、W；接下来 n 行每行 w v，表示重量和价值。",
      "输出一个整数，表示最大总价值。",
      "4 ≤ n ≤ 8，10 ≤ W ≤ 28，1 ≤ w ≤ 12，1 ≤ v ≤ 50。",
      ["01 背包", "动态规划"], 3,
      "dp[x] 表示容量 x 时的最大价值，倒序更新。",
      "每件物品只能选一次，所以容量要从大到小循环。"),
    V("必须正好挑 K 件行李，求不超重时的最大总价值；无法凑够 K 件输出 0。",
      "第一行三个整数 n、W、K；接下来 n 行每行 w v。",
      "输出一个整数，表示正好 K 件的最大价值。",
      "4 ≤ n ≤ 8，10 ≤ W ≤ 28，1 ≤ K ≤ 3。",
      ["01 背包", "二维 DP"], 4,
      "用 dp[k][x] 表示选 k 件、总重 x 的最大价值，初值 -1。",
      "先枚举件数再枚举容量，避免同一件被重复选。"),
    V("纸箱不能拆，师傅最多能一次推走多少个纸箱？",
      "第一行两个整数 n、W；接下来 n 行每行 w v（v 在本问中不用）。",
      "输出一个整数，表示最多能推走的纸箱数。",
      "4 ≤ n ≤ 8，10 ≤ W ≤ 28，1 ≤ w ≤ 12。",
      ["贪心", "排序"], 2,
      "想让数量最多，就优先拿最轻的箱子。",
      "把重量排序，从小到大能装就装。"),
    V("背包不超重的前提下，一共有多少种挑选商品的组合？",
      "第一行两个整数 n、W；接下来 n 行每行 w v（v 在本问中不用）。",
      "输出一个整数，表示总重量 ≤ W 的组合数（空组合也算一种）。",
      "4 ≤ n ≤ 8，10 ≤ W ≤ 28，1 ≤ w ≤ 12。",
      ["计数", "子集枚举"], 2,
      "n 很小，可以枚举 0 到 2^n-1 的每个子集。",
      "空集也要算一种，不要漏掉 mask=0。"),
    V("最多只能带 K 件装备，求不超过 W 时的最大保暖价值。",
      "第一行三个整数 n、W、K；接下来 n 行每行 w v。",
      "输出一个整数，表示最多 K 件的最大总价值。",
      "4 ≤ n ≤ 8，10 ≤ W ≤ 28，1 ≤ K ≤ 3。",
      ["01 背包", "二维 DP"], 4,
      "dp[k][x] 表示不超过 k 件、总重不超过 x 的最大价值。",
      "最后答案是所有 k ≤ K、x ≤ W 的状态里的最大值。"),
], KNAP01_CPP, solve_knap01, rand_knap01)

# 8. 完全背包的五个不同问法
KNAPFULL_STORIES = [
    ("丝娃娃的配菜可以重复拿",
     "吃丝娃娃时，一张皮最多卷 W 克的配菜。配菜台上每种菜有重量和美味值，同一种可以反复拿。"),
    ("烙锅点菜要凑够一锅",
     "贵阳烙锅按重量点菜，锅最多放 W 克。每种菜可以重复点，老板想知道最少点几盘才能正好凑够 W 克。"),
    ("肠旺面加料的组合数",
     "一碗肠旺面最多加 W 克的料。每种加料可以重复加，小黔想知道一共有多少种加料方案能正好加到 W 克。"),
    ("酸汤鱼配菜的数量",
     "一锅酸汤鱼最多放 W 克配菜。每种配菜可以重复放，小黔想尽量多放几样菜，让锅看起来更丰盛。"),
    ("豆米火锅自助台",
     "豆米火锅自助台最多装 W 克。每种配菜可以重复取，小黔想知道能不能正好装满 W 克，不剩一点空间。"),
]


def rand_knapfull(v, rng):
    n = rng.randint(3, 7)
    W = rng.randint(6, 24)
    rows = [(rng.randint(1, 8), rng.randint(1, 40)) for _ in range(n)]
    return "%d %d\n%s" % (n, W, "\n".join("%d %d" % x for x in rows))


def solve_knapfull(v, t):
    d = list(map(int, t.split()))
    n, W = d[0], d[1]
    rows = [(d[2 + 2 * i], d[3 + 2 * i]) for i in range(n)]
    ws = [w for w, _ in rows]
    if v == 0:
        dp = [0] * (W + 1)
        for w, val in rows:
            for x in range(w, W + 1):
                dp[x] = max(dp[x], dp[x - w] + val)
        return str(max(dp))
    if v == 1:
        dp = [10**9] * (W + 1); dp[0] = 0
        for x in range(1, W + 1):
            for w in ws:
                if x >= w: dp[x] = min(dp[x], dp[x - w] + 1)
        return str(-1 if dp[W] >= 10**9 else dp[W])
    if v == 2:
        dp = [0] * (W + 1); dp[0] = 1
        for x in range(1, W + 1):
            for w in ws:
                if x >= w: dp[x] += dp[x - w]
        return str(dp[W])
    if v == 3:
        return str(W // min(ws))
    dp = [False] * (W + 1); dp[0] = True
    for x in range(1, W + 1):
        for w in ws:
            if x >= w and dp[x - w]: dp[x] = True
    return "YES" if dp[W] else "NO"


KNAPFULL_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, W; cin >> n >> W;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    if (MODE == 0) {
        vector<long long> dp(W + 1, 0);
        for (int i = 0; i < n; i++)
            for (int x = w[i]; x <= W; x++) dp[x] = max(dp[x], dp[x - w[i]] + v[i]);
        cout << *max_element(dp.begin(), dp.end()) << "\n";
    } else if (MODE == 1) {
        vector<int> dp(W + 1, 1e9); dp[0] = 0;
        for (int x = 1; x <= W; x++)
            for (int i = 0; i < n; i++)
                if (x >= w[i]) dp[x] = min(dp[x], dp[x - w[i]] + 1);
        cout << (dp[W] >= 1e9 ? -1 : dp[W]) << "\n";
    } else if (MODE == 2) {
        vector<long long> dp(W + 1, 0); dp[0] = 1;
        for (int x = 1; x <= W; x++)
            for (int i = 0; i < n; i++)
                if (x >= w[i]) dp[x] += dp[x - w[i]];
        cout << dp[W] << "\n";
    } else if (MODE == 3) {
        cout << W / *min_element(w.begin(), w.end()) << "\n";
    } else {
        vector<bool> dp(W + 1, false); dp[0] = true;
        for (int x = 1; x <= W; x++)
            for (int i = 0; i < n; i++)
                if (x >= w[i] && dp[x - w[i]]) dp[x] = true;
        cout << (dp[W] ? "YES" : "NO") << "\n";
    }
    return 0;
}
"""

fam("knapfull", KNAPFULL_STORIES, [
    V("每种配菜可以重复拿，求一张皮能卷出的最大美味值。",
      "第一行两个整数 n、W；接下来 n 行每行 w v。",
      "输出一个整数，表示最大美味值。",
      "3 ≤ n ≤ 7，6 ≤ W ≤ 24，1 ≤ w ≤ 8，1 ≤ v ≤ 40。",
      ["完全背包", "动态规划"], 3,
      "和 01 背包相反，容量从小到大循环，允许同一件重复选。",
      "dp[x] 表示容量 x 的最大价值。"),
    V("每种菜可以重复点，最少点几盘才能正好凑够 W 克？凑不出输出 -1。",
      "第一行两个整数 n、W；接下来 n 行每行 w v（v 在本问中不用）。",
      "输出一个整数，表示最少盘数；凑不出输出 -1。",
      "3 ≤ n ≤ 7，6 ≤ W ≤ 24，1 ≤ w ≤ 8。",
      ["完全背包", "最少件数"], 4,
      "dp[x] 表示凑出 x 克的最少盘数，初值设成无穷大。",
      "最后如果 dp[W] 还是无穷大，输出 -1。"),
    V("每种加料可以重复加，求正好加到 W 克的方案数。",
      "第一行两个整数 n、W；接下来 n 行每行 w v（v 在本问中不用）。",
      "输出一个整数，表示方案数。",
      "3 ≤ n ≤ 7，6 ≤ W ≤ 24，1 ≤ w ≤ 8。",
      ["完全背包", "计数 DP"], 4,
      "dp[x] 表示凑出 x 克的方案数，dp[0]=1。",
      "按容量从小到大累加，同一种加料可以反复用。"),
    V("每种配菜可以重复放，最多能放多少盘菜（总重不超过 W）？",
      "第一行两个整数 n、W；接下来 n 行每行 w v。",
      "输出一个整数，表示最多盘数。",
      "3 ≤ n ≤ 7，6 ≤ W ≤ 24，1 ≤ w ≤ 8。",
      ["贪心", "完全背包"], 2,
      "要盘数最多，就反复选最轻的那一种配菜。",
      "答案就是 W 除以最小重量，向下取整。"),
    V("每种配菜可以重复取，判断能不能正好装满 W 克。",
      "第一行两个整数 n、W；接下来 n 行每行 w v。",
      "能正好装满输出 YES，否则输出 NO。",
      "3 ≤ n ≤ 7，6 ≤ W ≤ 24，1 ≤ w ≤ 8。",
      ["完全背包", "可达性"], 3,
      "dp[x] 表示 x 克是否能凑出，dp[0]=true。",
      "每种菜可以重复用，所以容量正序循环。"),
], KNAPFULL_CPP, solve_knapfull, rand_knapfull)



# 9. 递增序列：LIS、LDS、最长不下降、连续上升、LIS 方案数
LIS_STORIES = [
    ("观山湖泵站的水位记录",
     "观山湖泵站按天记录水位。小黔想按时间顺序挑出若干天，让水位一天比一天高，看看这轮降雨最长能延续多少天。"),
    ("黔灵山猕猴的排队身高",
     "黔灵山的猕猴按到达顺序排成一列，饲养员记录每只猴子的身高。他想按原顺序挑出一组身高越来越矮的猴子。"),
    ("花果园电梯的停靠楼层",
     "花果园一栋超高层电梯一天里按顺序停靠了很多楼层。物业想找出“楼层不下降”的最长一段停靠序列。"),
    ("数博会入场编号的连续段",
     "数博会入口按顺序发放参观编号。工作人员想找一段连续发放的编号，要求后一个编号严格比前一个大。"),
    ("贵阳逐日气温的升温方案数",
     "气象站记录了连续 n 天的最高气温。小黔想知道：最长严格升温日序列有多少种不同的选法（只按位置区分）。"),
]


def rand_lis(v, rng):
    n = rng.randint(6, 14)
    a = [rng.randint(0, 30) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_lis(v, t):
    d = list(map(int, t.split()))
    n = d[0]; a = d[1:1 + n]
    if v == 3:
        best = 1; cur = 1
        for i in range(1, n):
            if a[i] > a[i - 1]: cur += 1
            else: cur = 1
            best = max(best, cur)
        return str(best)
    if v == 4:
        best = 0; cnt = 0
        for mask in range(1 << n):
            seq = [a[i] for i in range(n) if mask >> i & 1]
            if all(seq[i] < seq[i + 1] for i in range(len(seq) - 1)):
                if len(seq) > best: best = len(seq); cnt = 1
                elif len(seq) == best: cnt += 1
        return str(cnt % 1000000007)
    def lis(arr, strict=True):
        dp = [1] * len(arr)
        for i in range(len(arr)):
            for j in range(i):
                if (arr[j] < arr[i]) if strict else (arr[j] <= arr[i]):
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
    if v == 0: return str(lis(a, True))
    if v == 2: return str(lis(a, False))
    return str(lis([-x for x in a], True))


LIS_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    if (MODE == 0 || MODE == 1 || MODE == 2) {
        vector<int> b = a;
        if (MODE == 1) for (int &x : b) x = -x;
        vector<int> dp(n, 1);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < i; j++) {
                bool ok = (MODE == 2 ? b[j] <= b[i] : b[j] < b[i]);
                if (ok) dp[i] = max(dp[i], dp[j] + 1);
            }
        cout << *max_element(dp.begin(), dp.end()) << "\n";
    } else if (MODE == 3) {
        int best = 1, cur = 1;
        for (int i = 1; i < n; i++) {
            if (a[i] > a[i - 1]) cur++; else cur = 1;
            best = max(best, cur);
        }
        cout << best << "\n";
    } else {
        int best = 0; long long cnt = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            vector<int> s;
            for (int i = 0; i < n; i++) if (mask >> i & 1) s.push_back(a[i]);
            bool ok = true;
            for (size_t i = 1; i < s.size(); i++) if (s[i - 1] >= s[i]) ok = false;
            if (!ok) continue;
            if ((int)s.size() > best) { best = s.size(); cnt = 1; }
            else if ((int)s.size() == best) cnt++;
        }
        cout << cnt % 1000000007 << "\n";
    }
    return 0;
}
"""

fam("lis", LIS_STORIES, [
    V("求按时间顺序选出的严格递增水位序列，最多能选多少天。",
      "第一行一个整数 n，第二行 n 个整数表示每天水位。",
      "输出一个整数，表示最长严格递增子序列的长度。",
      "6 ≤ n ≤ 14，0 ≤ 水位 ≤ 30。",
      ["LIS", "动态规划"], 3,
      "dp[i] 表示以第 i 天结尾的最长递增序列长度。",
      "枚举前一个 j，若 a[j] < a[i] 就可以接上。"),
    V("求按到达顺序选出的严格递减身高序列，最多能选多少只猴子。",
      "第一行一个整数 n，第二行 n 个整数表示身高。",
      "输出一个整数，表示最长严格递减子序列的长度。",
      "6 ≤ n ≤ 14，0 ≤ 身高 ≤ 30。",
      ["LDS", "动态规划"], 3,
      "把每个数取相反数，严格递减就变成严格递增。",
      "对 -a 求一遍 LIS 即可。"),
    V("求楼层“不下降”（允许相等）的最长停靠子序列长度。",
      "第一行一个整数 n，第二行 n 个整数表示停靠楼层。",
      "输出一个整数，表示最长不下降子序列长度。",
      "6 ≤ n ≤ 14，0 ≤ 楼层 ≤ 30。",
      ["LIS", "动态规划"], 3,
      "和 LIS 只差一个等号：a[j] <= a[i] 也能接。",
      "不要漏掉相等楼层的情况。"),
    V("求连续发放的编号里，严格递增的最长一段有多少个编号。",
      "第一行一个整数 n，第二行 n 个整数表示编号。",
      "输出一个整数，表示最长连续严格上升段的长度。",
      "6 ≤ n ≤ 14，0 ≤ 编号 ≤ 30。",
      ["连续子段", "模拟"], 2,
      "这题要求“连续”，不能跳过中间的元素。",
      "遇到不上升就把当前长度重置为 1。"),
    V("求最长严格升温日序列的不同选法有多少种（对 10^9+7 取模）。",
      "第一行一个整数 n，第二行 n 个整数表示气温。",
      "输出一个整数，表示最长严格递增子序列的方案数。",
      "6 ≤ n ≤ 14，0 ≤ 气温 ≤ 30。",
      ["LIS", "计数", "子集枚举"], 4,
      "n 很小，可以枚举每个子集，判断是否严格递增。",
      "先记最长长度，再统计达到这个长度的方案数。"),
], LIS_CPP, solve_lis, rand_lis)

# 10. 网格 BFS 的五种问法
BFS_STORIES = [
    ("花果园地下车库找车位",
     "花果园地下车库被画成 n×m 的格子，1 表示墙或已占车位，0 表示还能走。小黔从左上角进库，要走到右下角的空位。"),
    ("青岩古镇石板巷的可达范围",
     "青岩古镇的石板巷像一张网格，1 是封闭院落，0 是巷道。游客从北门进入，想知究竟能逛到多少条巷子。"),
    ("黔灵山迷宫步道的斜穿",
     "黔灵山公园有一段迷宫步道，游客可以上下左右走，也可以沿对角线斜穿一个格子。求从入口到出口的最少步数。"),
    ("地铁站厅的换乘耗时",
     "地铁站厅被分成 n×m 个区域，每个格子里的数字表示穿过它的耗时（0～9）。换乘时只能上下左右走，求从入口到出口的最短总耗时。"),
    ("数博会展位的最短路线数",
     "数博会展馆的展位排成网格，1 是展台不能走，0 是通道。工作人员从左上角走到右下角，想知道最短路线一共有多少条。"),
]


def rand_bfs(v, rng):
    n = rng.randint(4, 7); m = rng.randint(4, 7)
    if v == 3:
        rows = ["".join(str(rng.randint(0, 9)) for _ in range(m)) for _ in range(n)]
        return "%d %d\n%s" % (n, m, "\n".join(rows))
    rows = ["".join("1" if rng.random() < 0.2 else "0" for _ in range(m)) for _ in range(n)]
    rows[0] = "0" + rows[0][1:]
    rows[-1] = rows[-1][:-1] + "0"
    return "%d %d\n%s" % (n, m, "\n".join(rows))


def solve_bfs(v, t):
    lines = _lines(t)
    n, m = map(int, lines[0].split())
    g = lines[1:1 + n]
    if v == 3:
        INF = 10**9
        dist = [[INF] * m for _ in range(n)]
        dist[0][0] = int(g[0][0])
        import heapq
        pq = [(dist[0][0], 0, 0)]
        while pq:
            d, x, y = heapq.heappop(pq)
            if d != dist[x][y]: continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < m:
                    nd = d + int(g[nx][ny])
                    if nd < dist[nx][ny]:
                        dist[nx][ny] = nd; heapq.heappush(pq, (nd, nx, ny))
        return str(dist[n - 1][m - 1])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    if v == 2:
        dirs = tuple((dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)
    if g[0][0] == "1":
        return "0" if v == 1 else "-1"
    dist = [[-1] * m for _ in range(n)]
    ways = [[0] * m for _ in range(n)]
    dist[0][0] = 0; ways[0][0] = 1
    q = [(0, 0)]; h = 0
    while h < len(q):
        x, y = q[h]; h += 1
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == "0":
                if dist[nx][ny] < 0:
                    dist[nx][ny] = dist[x][y] + 1
                    ways[nx][ny] = ways[x][y]
                    q.append((nx, ny))
                elif dist[nx][ny] == dist[x][y] + 1:
                    ways[nx][ny] = (ways[nx][ny] + ways[x][y]) % 1000000007
    if v == 1:
        return str(sum(1 for i in range(n) for j in range(m) if dist[i][j] >= 0))
    if v == 4:
        return str(ways[n - 1][m - 1]) if dist[n - 1][m - 1] >= 0 else "0"
    return str(dist[n - 1][m - 1])


BFS_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, m; cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    if (MODE == 3) {
        vector<vector<int>> d(n, vector<int>(m, 1e9));
        d[0][0] = g[0][0] - '0';
        priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;
        pq.push({d[0][0], 0, 0});
        int dx[4] = {1,-1,0,0}, dy[4] = {0,0,1,-1};
        while (!pq.empty()) {
            auto [du, x, y] = pq.top(); pq.pop();
            if (du != d[x][y]) continue;
            for (int k = 0; k < 4; k++) {
                int nx = x + dx[k], ny = y + dy[k];
                if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
                int nd = du + (g[nx][ny] - '0');
                if (nd < d[nx][ny]) { d[nx][ny] = nd; pq.push({nd, nx, ny}); }
            }
        }
        cout << d[n-1][m-1] << "\n";
        return 0;
    }
    if (g[0][0] == '1') { cout << (MODE == 1 ? "0\n" : "-1\n"); return 0; }
    vector<vector<int>> d(n, vector<int>(m, -1)), w(n, vector<int>(m, 0));
    d[0][0] = 0; w[0][0] = 1;
    queue<pair<int,int>> q; q.push({0,0});
    int dx8[8] = {1,-1,0,0,1,1,-1,-1}, dy8[8] = {0,0,1,-1,1,-1,1,-1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        int dirs = (MODE == 2 ? 8 : 4);
        for (int k = 0; k < dirs; k++) {
            int nx = x + (MODE == 2 ? dx8[k] : dx8[k]), ny = y + (MODE == 2 ? dy8[k] : dy8[k]);
            if (nx < 0 || nx >= n || ny < 0 || ny >= m || g[nx][ny] == '1') continue;
            if (d[nx][ny] < 0) {
                d[nx][ny] = d[x][y] + 1; w[nx][ny] = w[x][y]; q.push({nx, ny});
            } else if (d[nx][ny] == d[x][y] + 1) {
                w[nx][ny] = (w[nx][ny] + w[x][y]) % 1000000007;
            }
        }
    }
    if (MODE == 1) {
        int cnt = 0;
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (d[i][j] >= 0) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 4) {
        cout << (d[n-1][m-1] < 0 ? 0 : w[n-1][m-1]) << "\n";
    } else {
        cout << d[n-1][m-1] << "\n";
    }
    return 0;
}
"""

fam("bfs", BFS_STORIES, [
    V("从左上角走到右下角的最少步数；走不到输出 -1。",
      "第一行两个整数 n、m；接下来 n 行，每行一个长度为 m 的 01 串，0 可走、1 不可走。",
      "输出一个整数，表示最少步数；无法到达输出 -1。",
      "4 ≤ n, m ≤ 7，入口和出口保证为 0。",
      ["BFS", "最短路"], 3,
      "边权都是 1，用 BFS 一层层扩展。",
      "第一次到达某个格子时的距离就是最短距离。"),
    V("从左上角出发，一共有多少个格子是可达的（包括起点）？",
      "第一行两个整数 n、m；接下来 n 行 01 串。",
      "输出一个整数，表示可达格子数。",
      "4 ≤ n, m ≤ 7。",
      ["BFS", "连通块"], 3,
      "从起点开始 BFS/DFS，数一数访问到多少个格子。",
      "遇到 1 就停下，不要越界。"),
    V("允许上下左右和斜对角移动，求从左上角到右下角的最少步数。",
      "第一行两个整数 n、m；接下来 n 行 01 串。",
      "输出一个整数，表示最少步数；无法到达输出 -1。",
      "4 ≤ n, m ≤ 7。",
      ["BFS", "八方向"], 3,
      "方向数组从 4 个扩展到 8 个。",
      "斜着走一步也只算一步，仍然是边权为 1 的 BFS。"),
    V("每个格子有一个 0～9 的耗时，求从左上角到右下角的最短总耗时。",
      "第一行两个整数 n、m；接下来 n 行，每行 m 个数字字符。",
      "输出一个整数，表示最短总耗时（包含起点和终点的耗时）。",
      "4 ≤ n, m ≤ 7。",
      ["Dijkstra", "最短路"], 4,
      "边权不再是 1，用优先队列做 Dijkstra。",
      "进入一个格子的代价是那个格子上的数字，起点也要算。"),
    V("求从左上角到右下角的最短路线条数（对 10^9+7 取模）。",
      "第一行两个整数 n、m；接下来 n 行 01 串。",
      "输出一个整数，表示最短路线数；无法到达输出 0。",
      "4 ≤ n, m ≤ 7。",
      ["BFS", "计数"], 4,
      "BFS 时同时记 dist 和 ways。",
      "第一次到达时继承方案数；同样最短时累加。"),
], BFS_CPP, solve_bfs, rand_bfs)

# 11. 无权图：最短路、连通块、最大度、可达数、直径
GRAPH_STORIES = [
    ("地铁换乘要坐几站",
     "贵阳地铁 1、2、3 号线和 S1 线交织成一张网。小黔把换乘关系抽象成一张无权图，想知道从 1 号站到 n 号站最少坐几站。"),
    ("花果园楼栋之间的小路",
     "花果园的楼栋之间有一些内部小路。物业把楼栋和小路记成一张图，想知道整个小区被分成几个互不相通的片区。"),
    ("青岩古镇公交的枢纽站",
     "青岩古镇周边的公交线路连成一张图。交通员想知道哪个站点连接的车站最多，好安排换乘指引。"),
    ("观山湖绿道的可逛范围",
     "观山湖绿道有一些入口和连接段。游客从 1 号入口进园，想知道顺着绿道一共能走到多少个入口/节点。"),
    ("贵阳北站到机场的大巴网",
     "贵阳北站、龙洞堡机场和市区站点之间有多条大巴线路。调度员想知道这张网里最远的两站之间要换几趟车。"),
]


def rand_graph(v, rng):
    n = rng.randint(5, 8)
    edges = []
    for _ in range(rng.randint(3, 9)):
        u = rng.randint(1, n); w = rng.randint(1, n)
        if u != w: edges.append((u, w))
    edges = list(dict.fromkeys(tuple(sorted(e)) for e in edges))
    return "%d %d\n%s" % (n, len(edges), "\n".join("%d %d" % e for e in edges))


def solve_graph(v, t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, w = d[2 + 2 * i], d[3 + 2 * i]
        adj[u].append(w); adj[w].append(u)
    def bfs(s):
        dist = [-1] * (n + 1); dist[s] = 0; q = [s]; h = 0
        while h < len(q):
            u = q[h]; h += 1
            for x in adj[u]:
                if dist[x] < 0:
                    dist[x] = dist[u] + 1; q.append(x)
        return dist
    if v == 0:
        return str(bfs(1)[n])
    if v == 1:
        seen = [False] * (n + 1); cnt = 0
        for i in range(1, n + 1):
            if not seen[i]:
                cnt += 1; seen[i] = True; q = [i]; h = 0
                while h < len(q):
                    u = q[h]; h += 1
                    for x in adj[u]:
                        if not seen[x]: seen[x] = True; q.append(x)
        return str(cnt)
    if v == 2:
        deg = [len(adj[i]) for i in range(1, n + 1)]
        best = max(deg); idx = deg.index(best) + 1
        return "%d %d" % (idx, best)
    if v == 3:
        return str(sum(1 for x in bfs(1) if x >= 0))
    best = 0
    for i in range(1, n + 1):
        dist = bfs(i)
        best = max(best, max(dist))
    return str(best)


GRAPH_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) { int u, v; cin >> u >> v; g[u].push_back(v); g[v].push_back(u); }
    auto bfs = [&](int s) {
        vector<int> d(n + 1, -1); d[s] = 0; queue<int> q; q.push(s);
        while (!q.empty()) { int u = q.front(); q.pop(); for (int v : g[u]) if (d[v] < 0) { d[v] = d[u] + 1; q.push(v); } }
        return d;
    };
    if (MODE == 0) {
        cout << bfs(1)[n] << "\n";
    } else if (MODE == 1) {
        vector<int> seen(n + 1, 0); int cnt = 0;
        for (int i = 1; i <= n; i++) if (!seen[i]) {
            cnt++; seen[i] = 1; queue<int> q; q.push(i);
            while (!q.empty()) { int u = q.front(); q.pop(); for (int v : g[u]) if (!seen[v]) { seen[v] = 1; q.push(v); } }
        }
        cout << cnt << "\n";
    } else if (MODE == 2) {
        int best = -1, id = 0;
        for (int i = 1; i <= n; i++) if ((int)g[i].size() > best) { best = g[i].size(); id = i; }
        cout << id << " " << best << "\n";
    } else if (MODE == 3) {
        auto d = bfs(1); int cnt = 0;
        for (int i = 1; i <= n; i++) if (d[i] >= 0) cnt++;
        cout << cnt << "\n";
    } else {
        int best = 0;
        for (int i = 1; i <= n; i++) { auto d = bfs(i); for (int j = 1; j <= n; j++) best = max(best, d[j]); }
        cout << best << "\n";
    }
    return 0;
}
"""

fam("graph", GRAPH_STORIES, [
    V("求从 1 号站到 n 号站最少经过几条边；走不到输出 -1。",
      "第一行两个整数 n、m；接下来 m 行每行 u v，表示一条无向边。",
      "输出一个整数，表示最少边数；不连通输出 -1。",
      "4 ≤ n ≤ 8，m ≤ 12。",
      ["BFS", "无权图最短路"], 3,
      "无权图最短路就是 BFS 的层数。",
      "dist 初值设 -1，起点为 0。"),
    V("求这张无向图一共有几个连通块。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一个整数，表示连通块数量。",
      "4 ≤ n ≤ 8，m ≤ 12。",
      ["连通块", "BFS"], 3,
      "枚举每个未访问的点，做一次 BFS 就是一个连通块。",
      "孤立点也算一个连通块。"),
    V("求度数最大的站点编号；度数相同取编号最小的。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一行两个整数：站点编号和它的度数。",
      "4 ≤ n ≤ 8，m ≤ 12。",
      ["图论", "度数"], 2,
      "每读一条边，两端的度数都加一。",
      "从 1 到 n 扫描，只有严格大于当前最大值时才替换。"),
    V("从 1 号入口出发，一共能到达多少个节点（包括 1 号）？",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一个整数，表示可达节点数。",
      "4 ≤ n ≤ 8，m ≤ 12。",
      ["BFS", "可达性"], 3,
      "从 1 开始 BFS，统计 dist >= 0 的点。",
      "不要只数直接相邻的点，要一整片都算。"),
    V("求这张网里最远的两个节点之间最少要经过几条边（图的直径）。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一个整数，表示所有可达点对中的最大最短路。",
      "4 ≤ n ≤ 8，m ≤ 12。",
      ["BFS", "图的直径"], 4,
      "n 很小，对每个点做一次 BFS，取所有距离的最大值。",
      "不连通时只考虑能互相到达的点对。"),
], GRAPH_CPP, solve_graph, rand_graph)

# 12. 并查集：连通块数、最大块、是否连通、冗余边、同块点对
DSU_STORIES = [
    ("小区团购群的分组",
     "花果园几个小区按团购群拉人，群里的人互相认识就算一组。物业想知道一共有几个互不相干的团购群。"),
    ("老院落的院落合并",
     "贵阳老城区的一些院落共用一条巷子，巷子把院落连成片。街道办想知道最大的一片有多少个院落。"),
    ("大学城社团的跨校联系",
     "花溪大学城几个社团之间有合作。小黔想知道 1 号社团和 n 号社团是不是通过合作链连在一起。"),
    ("数博会参展商的合作圈",
     "数博会的参展商两两签了合作协议。工作人员发现有些协议是多余的——去掉它，合作圈仍然连通。"),
    ("公园健身小组的熟人對",
     "观山湖公园的健身小组里，同一个小组的人互相都算熟人。教练想知道一共有多少对熟人。"),
]


def rand_dsu(v, rng):
    n = rng.randint(5, 8)
    edges = []
    for _ in range(rng.randint(2, 7)):
        u = rng.randint(1, n); w = rng.randint(1, n)
        if u != w: edges.append((u, w))
    edges = list(dict.fromkeys(tuple(sorted(e)) for e in edges))
    return "%d %d\n%s" % (n, len(edges), "\n".join("%d %d" % e for e in edges))


def solve_dsu(v, t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    par = list(range(n + 1))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    red = 0
    for i in range(m):
        a, b = d[2 + 2 * i], d[3 + 2 * i]
        ra, rb = find(a), find(b)
        if ra == rb: red += 1
        else: par[ra] = rb
    roots = {}
    for i in range(1, n + 1): roots[find(i)] = roots.get(find(i), 0) + 1
    if v == 0: return str(len(roots))
    if v == 1: return str(max(roots.values()))
    if v == 2: return "YES" if find(1) == find(n) else "NO"
    if v == 3: return str(red)
    return str(sum(sz * (sz - 1) // 2 for sz in roots.values()))


DSU_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int par[20];
int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n, m; cin >> n >> m;
    for (int i = 1; i <= n; i++) par[i] = i;
    int red = 0;
    for (int i = 0; i < m; i++) {
        int a, b; cin >> a >> b;
        int ra = find(a), rb = find(b);
        if (ra == rb) red++; else par[ra] = rb;
    }
    map<int,int> sz;
    for (int i = 1; i <= n; i++) sz[find(i)]++;
    if (MODE == 0) cout << sz.size() << "\n";
    else if (MODE == 1) { int best = 0; for (auto &p : sz) best = max(best, p.second); cout << best << "\n"; }
    else if (MODE == 2) cout << (find(1) == find(n) ? "YES" : "NO") << "\n";
    else if (MODE == 3) cout << red << "\n";
    else {
        long long ans = 0;
        for (auto &p : sz) ans += 1LL * p.second * (p.second - 1) / 2;
        cout << ans << "\n";
    }
    return 0;
}
"""

fam("dsu", DSU_STORIES, [
    V("求互不相干的团购群一共有几个。",
      "第一行两个整数 n、m；接下来 m 行每行 u v，表示 u 和 v 在同一个群。",
      "输出一个整数，表示连通块数量。",
      "4 ≤ n ≤ 8，m ≤ 10。",
      ["并查集", "连通块"], 3,
      "把每条边两端的点合并，最后数不同根节点。",
      "路径压缩可以写 find(x) = x == par[x] ? x : find(par[x])。"),
    V("求最大的一片院落包含多少个院落。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一个整数，表示最大连通块大小。",
      "4 ≤ n ≤ 8，m ≤ 10。",
      ["并查集", "连通块"], 3,
      "合并后统计每个根节点下面挂了几个点。",
      "取统计结果的最大值。"),
    V("判断 1 号社团和 n 号社团是否连通，输出 YES 或 NO。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出 YES 或 NO。",
      "4 ≤ n ≤ 8，m ≤ 10。",
      ["并查集", "连通性"], 3,
      "所有边合并完后，比较 find(1) 和 find(n)。",
      "路径压缩后比较根节点即可。"),
    V("求有几条协议是多余的（删掉后合作圈仍然连通）。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一个整数，表示冗余边数。",
      "4 ≤ n ≤ 8，m ≤ 10。",
      ["并查集", "环"], 4,
      "按顺序加边，如果两端已经同根，这条边就是多余的。",
      "答案等于 m 减去成功合并的次数。"),
    V("同一个健身小组里任意两人都算一对熟人，求总熟人对数。",
      "第一行两个整数 n、m；接下来 m 行每行 u v。",
      "输出一个整数，表示同组点对数。",
      "4 ≤ n ≤ 8，m ≤ 10。",
      ["并查集", "组合计数"], 3,
      "每个大小为 s 的连通块贡献 C(s,2)=s(s-1)/2 对。",
      "把所有连通块的贡献相加。"),
], DSU_CPP, solve_dsu, rand_dsu)

# 13. 数论：GCD、LCM、两两 GCD、互质对、约分
GCD_STORIES = [
    ("分丝娃娃薄饼",
     "丝娃娃的薄饼要切成一样大的小片。小黔有几种不同大小的薄饼，想把它们都切成同样大小且不浪费。"),
    ("分烙锅土豆",
     "烙锅店把几筐土豆按袋分装。老板想让每种分装袋数都刚好用完，且每袋尽量大。"),
    ("分玫瑰糖",
     "青岩古镇的玫瑰糖要分成小包。店员把几种包装规格两两比较，想知道每对规格最多能平均分成多少克。"),
    ("分停车位",
     "花果园车库把车位按编号分组。物业想知道有多少对编号是互质的，方便安排轮换。"),
    ("分肠旺面",
     "肠旺面的红油和清汤按比例调配。小黔想把 a:b 化成最简整数比。"),
]


def rand_gcd(v, rng):
    if v == 4:
        a = rng.randint(2, 60); b = rng.randint(2, 60)
        return "%d %d" % (a, b)
    if v == 1:
        n = rng.randint(3, 5)
        a = [rng.randint(1, 12) for _ in range(n)]
    else:
        n = rng.randint(4, 8)
        a = [rng.randint(1, 30) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_gcd(v, t):
    if v == 4:
        a, b = map(int, t.split())
        g = math.gcd(a, b)
        return "%d %d" % (a // g, b // g)
    d = list(map(int, t.split()))
    a = d[1:1 + d[0]]
    if v == 0:
        g = 0
        for x in a: g = math.gcd(g, x)
        return str(g)
    if v == 1:
        l = 1
        for x in a: l = l * x // math.gcd(l, x)
        return str(l)
    if v == 2:
        return str(sum(math.gcd(a[i], a[j]) for i in range(len(a)) for j in range(i + 1, len(a))))
    return str(sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if math.gcd(a[i], a[j]) == 1))


GCD_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    if (MODE == 4) {
        long long a, b; cin >> a >> b;
        long long g = gcd(a, b);
        cout << a / g << " " << b / g << "\n";
        return 0;
    }
    int n; cin >> n; vector<int> a(n);
    for (int &x : a) cin >> x;
    if (MODE == 0) { int g = 0; for (int x : a) g = gcd(g, x); cout << g << "\n"; }
    else if (MODE == 1) { long long l = 1; for (int x : a) l = l * x / gcd(l, x); cout << l << "\n"; }
    else if (MODE == 2) {
        long long s = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) s += gcd(a[i], a[j]);
        cout << s << "\n";
    } else {
        int cnt = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (gcd(a[i], a[j]) == 1) cnt++;
        cout << cnt << "\n";
    }
    return 0;
}
"""

fam("gcd", GCD_STORIES, [
    V("求所有薄饼大小的最大公约数。",
      "第一行一个整数 n，第二行 n 个整数表示薄饼大小。",
      "输出一个整数，表示所有数的 GCD。",
      "4 ≤ n ≤ 8，1 ≤ 大小 ≤ 30。",
      ["GCD", "数论"], 2,
      "从 g=0 开始，依次 g=gcd(g,a[i])。",
      "gcd(0,x)=x，所以初值 0 很方便。"),
    V("求所有土豆筐重量的最小公倍数。",
      "第一行一个整数 n（3～5），第二行 n 个整数。",
      "输出一个整数，表示所有数的最小公倍数。",
      "3 ≤ n ≤ 5，1 ≤ 重量 ≤ 12。",
      ["LCM", "数论"], 3,
      "lcm(a,b)=a/gcd(a,b)*b，先除后乘防溢出。",
      "从 1 开始依次和每个数求 lcm。"),
    V("求所有包装规格两两的 GCD 之和。",
      "第一行一个整数 n，第二行 n 个整数。",
      "输出一个整数，表示 Σ gcd(a[i],a[j])（i<j）。",
      "4 ≤ n ≤ 8，1 ≤ 规格 ≤ 30。",
      ["GCD", "枚举"], 3,
      "枚举所有 (i,j) 点对，累加 gcd。",
      "只算 i<j，不要重复算两次。"),
    V("求有多少对车位编号是互质的。",
      "第一行一个整数 n，第二行 n 个整数表示编号。",
      "输出一个整数，表示 gcd=1 的点对数。",
      "4 ≤ n ≤ 8，1 ≤ 编号 ≤ 30。",
      ["GCD", "计数"], 3,
      "枚举点对，判断 gcd(a[i],a[j])==1。",
      "1 和任何数都互质。"),
    V("把 a:b 化成最简整数比。",
      "一行两个整数 a、b。",
      "输出一行两个整数，表示最简比。",
      "2 ≤ a,b ≤ 60。",
      ["GCD", "约分"], 2,
      "同时除以 gcd(a,b)。",
      "输出顺序保持原来的 a:b。"),
], GCD_CPP, solve_gcd, rand_gcd)

# 14. 质数：计数、第 n 个、分解、哥德巴赫、下一个
PRIME_STORIES = [
    ("数博会门票编号里的质数",
     "数博会门票按编号发放。工作人员想统计 1 到 n 号里有多少个编号是质数，好安排抽奖。"),
    ("甲秀楼石栏的编号",
     "甲秀楼重修时给石栏编号。工匠说第 n 个质数号要刻特殊纹样，请你找出这个编号。"),
    ("公交线路的质因数",
     "贵阳一条公交线路的配车数是 n。调度员想把 n 分解成质因数，看看能不能平均分成若干组。"),
    ("修文猕猴桃装箱的偶数拆分",
     "修文猕猴桃按个数装箱，箱数总是偶数。店员想把箱数拆成两个质数之和，看有多少种拆法。"),
    ("南明河桥墩的下一个质数",
     "南明河桥墩按质数编号。现在排到 n 号，下一个质数号应该是多少？"),
]


def rand_prime(v, rng):
    if v == 1:
        return str(rng.randint(1, 30))
    if v == 3:
        return str(rng.randint(5, 50) * 2)
    return str(rng.randint(20, 200))


def _sieve(n):
    if n < 2: return []
    p = [True] * (n + 1); p[0] = p[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if p[i]:
            for j in range(i * i, n + 1, i): p[j] = False
    return [i for i in range(2, n + 1) if p[i]]


def solve_prime(v, t):
    n = int(t.strip())
    if v == 0:
        return str(len(_sieve(n)))
    if v == 1:
        return str(_sieve(300)[n - 1])
    if v == 2:
        x = n; out = []
        for p in range(2, int(x ** 0.5) + 1):
            if x % p == 0:
                e = 0
                while x % p == 0: x //= p; e += 1
                out.append("%d^%d" % (p, e))
        if x > 1: out.append("%d^1" % x)
        return " ".join(out)
    if v == 3:
        ps = _sieve(n)
        return str(sum(1 for p in ps if p <= n - p and (n - p) in set(ps)))
    ps = _sieve(max(n + 300, 500))
    return str(next(p for p in ps if p >= n))


PRIME_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
const int N = 200000;
vector<int> primes;
bool comp[N + 1];
void init() {
    for (int i = 2; i <= N; i++) {
        if (!comp[i]) {
            primes.push_back(i);
            for (long long j = 1LL * i * i; j <= N; j += i) comp[j] = true;
        }
    }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    init();
    const int MODE = @MODE@;
    int n; cin >> n;
    if (MODE == 0) {
        cout << upper_bound(primes.begin(), primes.end(), n) - primes.begin() << "\n";
    } else if (MODE == 1) {
        cout << primes[n - 1] << "\n";
    } else if (MODE == 2) {
        int x = n; bool first = true;
        for (int p = 2; 1LL * p * p <= x; p++) if (x % p == 0) {
            int e = 0; while (x % p == 0) { x /= p; e++; }
            if (!first) cout << " "; cout << p << "^" << e; first = false;
        }
        if (x > 1) { if (!first) cout << " "; cout << x << "^1"; }
        cout << "\n";
    } else if (MODE == 3) {
        int cnt = 0;
        for (int p : primes) {
            if (p > n - p) break;
            int q = n - p;
            if (!comp[q]) cnt++;
        }
        cout << cnt << "\n";
    } else {
        cout << *lower_bound(primes.begin(), primes.end(), n) << "\n";
    }
    return 0;
}
"""

fam("prime", PRIME_STORIES, [
    V("统计 1 到 n 之间有多少个质数。",
      "一行一个整数 n。",
      "输出一个整数，表示质数个数。",
      "20 ≤ n ≤ 200。",
      ["质数", "埃氏筛"], 3,
      "用埃氏筛把 2 到 n 的合数全部标记掉。",
      "1 不是质数，2 是最小的质数。"),
    V("求第 n 个质数（第 1 个质数是 2）。",
      "一行一个整数 n。",
      "输出一个整数，表示第 n 个质数。",
      "1 ≤ n ≤ 30。",
      ["质数", "枚举"], 2,
      "从 2 开始逐个判断质数，数到第 n 个为止。",
      "判断 x 是否为质数，只需试除到 sqrt(x)。"),
    V("把 n 分解成质因数，按底数从小到大输出 p^e。",
      "一行一个整数 n。",
      "输出一行，形如“p1^e1 p2^e2 …”，指数为 1 也要写 ^1。",
      "12 ≤ n ≤ 200。",
      ["质因数分解", "数论"], 3,
      "从 2 开始试除，能除尽就统计指数。",
      "除完后如果剩下 x>1，它本身就是一个质因子。"),
    V("把偶数 n 拆成两个质数之和，求有序拆法数（p≤q）。",
      "一行一个偶数 n。",
      "输出一个整数，表示拆法数。",
      "10 ≤ n ≤ 100，n 为偶数。",
      ["质数", "枚举"], 3,
      "枚举 p 从 2 到 n/2，判断 p 和 n-p 是否都为质数。",
      "只枚举 p≤q，避免同一种拆法算两次。"),
    V("求大于等于 n 的最小质数。",
      "一行一个整数 n。",
      "输出一个整数，表示下一个质数。",
      "20 ≤ n ≤ 200。",
      ["质数", "枚举"], 2,
      "从 n 开始往上逐个判断，遇到质数就停。",
      "n 本身是质数时答案就是 n。"),
], PRIME_CPP, solve_prime, rand_prime)

# 15. 字符串：元音、辅音、众数、回文、游程编码
VOWEL_STORIES = [
    ("肠旺面招牌的拼音",
     "贵阳街头“chang wang mian”的拼音招牌被做成了一串字母。小黔想数一数里面有多少个元音字母。"),
    ("丝娃娃菜单的辅音",
     "丝娃娃菜单上的英文名是一串小写字母。店员想把元音去掉，只统计辅音个数。"),
    ("甲秀楼导览词的高频字母",
     "甲秀楼导览词的英文缩写是一串小写字母。讲解员想知道哪个字母出现最多。"),
    ("观山湖路牌的英文名",
     "观山湖公园的路牌上有一串英文名。小黔想判断它正着读和反着读是不是一样。"),
    ("青岩古镇门票的缩写",
     "青岩古镇门票上印着一串字母缩写。印刷员想把它压缩成“字母+出现次数”的形式。"),
]


def rand_vowel(v, rng):
    letters = "abcdefghijklmnopqrstuvw"
    n = rng.randint(5, 12)
    s = "".join(rng.choice(letters) for _ in range(n))
    if v == 3 and rng.random() < 0.5:
        half = "".join(rng.choice("abcd") for _ in range(n // 2))
        s = half + (half[-1] if n % 2 else "") + half[::-1]
    return s


def solve_vowel(v, t):
    s = t.strip()
    if v == 0:
        return str(sum(1 for c in s if c in "aeiou"))
    if v == 1:
        return str(sum(1 for c in s if c.isalpha() and c not in "aeiou"))
    if v == 2:
        best = min(s)
        for c in sorted(set(s)):
            if s.count(c) > s.count(best):
                best = c
        return best
    if v == 3:
        return "YES" if s == s[::-1] else "NO"
    out = []
    for c in s:
        if out and out[-1][0] == c: out[-1][1] += 1
        else: out.append([c, 1])
    return "".join("%s%d" % (c, k) for c, k in out)


VOWEL_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    string s; cin >> s;
    if (MODE == 0) {
        int cnt = 0;
        for (char c : s) if (string("aeiou").find(c) != string::npos) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 1) {
        int cnt = 0;
        for (char c : s) if (isalpha(c) && string("aeiou").find(c) == string::npos) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 2) {
        int cnt[26] = {0};
        for (char c : s) cnt[c - 'a']++;
        int best = 0;
        for (int i = 1; i < 26; i++) if (cnt[i] > cnt[best]) best = i;
        cout << char('a' + best) << "\n";
    } else if (MODE == 3) {
        string r = s; reverse(r.begin(), r.end());
        cout << (s == r ? "YES" : "NO") << "\n";
    } else {
        for (int i = 0; i < (int)s.size(); ) {
            int j = i;
            while (j < (int)s.size() && s[j] == s[i]) j++;
            cout << s[i] << j - i;
            i = j;
        }
        cout << "\n";
    }
    return 0;
}
"""

fam("vowel", VOWEL_STORIES, [
    V("统计字符串里元音字母 a、e、i、o、u 的个数。",
      "一行一个由小写字母组成的字符串 s。",
      "输出一个整数，表示元音个数。",
      "5 ≤ |s| ≤ 12，只含小写字母。",
      ["字符串", "计数"], 1,
      "逐个字符判断是否属于 aeiou。",
      "y 不算元音，不要多算。"),
    V("统计字符串里辅音字母（非 aeiou）的个数。",
      "一行一个由小写字母组成的字符串 s。",
      "输出一个整数，表示辅音个数。",
      "5 ≤ |s| ≤ 12，只含小写字母。",
      ["字符串", "计数"], 1,
      "不是元音的小写字母就是辅音。",
      "总数减去元音数也可以。"),
    V("求出现次数最多的字母；次数相同输出字典序最小的。",
      "一行一个由小写字母组成的字符串 s。",
      "输出一个字符，表示众数字母。",
      "5 ≤ |s| ≤ 12，只含小写字母。",
      ["字符串", "频率"], 2,
      "统计 26 个字母的出现次数。",
      "并列时取字母序更小的，不要取先出现的。"),
    V("判断字符串是不是回文串，输出 YES 或 NO。",
      "一行一个由小写字母组成的字符串 s。",
      "输出 YES 或 NO。",
      "5 ≤ |s| ≤ 12。",
      ["字符串", "回文"], 2,
      "双指针从两头向中间比较。",
      "长度为奇数的中心字符不用比较。"),
    V("把字符串做游程编码：连续相同字母写成“字母+次数”。",
      "一行一个由小写字母组成的字符串 s。",
      "输出一行编码结果，例如 aabbb 编码为 a2b3。",
      "5 ≤ |s| ≤ 12。",
      ["字符串", "游程编码"], 2,
      "从左到右数连续相同字符的长度。",
      "次数为 1 也要写出来，例如 a1。"),
], VOWEL_CPP, solve_vowel, rand_vowel)

# 16. 机器人移动：终点、最远距离、不同格子、回到原点、包围盒
ROBOT_STORIES = [
    ("黔灵山猕猴的散步",
     "黔灵山的一只猕猴从公园门口出发，按饲养员的口令上下左右走。小黔想知道它最后停在哪里。"),
    ("花果园快递机器人的最远距离",
     "花果园的快递机器人从驿站出发，沿楼道来回送货。物业想知道它离出发点最远时有多远。"),
    ("数博会巡检机器人的足迹",
     "数博会展馆的巡检机器人按固定路线走格子。工作人员想知道它一共踏过多少个不同的格子。"),
    ("南明河保洁船的回港",
     "南明河的保洁船从码头出发，按指令在河面上移动。它想沿原路回到码头，最少第几步能回来？"),
    ("青岩古镇导览车的活动范围",
     "青岩古镇的导览车在广场上按指令移动。管理员想知道它走过的路线围成的矩形有多大。"),
]


def rand_robot(v, rng):
    n = rng.randint(8, 16)
    s = "".join(rng.choice("UDLR") for _ in range(n))
    if v == 3 and rng.random() < 0.45:
        half = s[:n // 2]
        inv = {"U": "D", "D": "U", "L": "R", "R": "L"}
        s = half + "".join(inv[c] for c in reversed(half))
    return s


def solve_robot(v, t):
    s = t.strip()
    x = y = 0
    seen = {(0, 0)}
    maxd = 0
    first_back = -1
    xs = [0]; ys = [0]
    for i, c in enumerate(s, 1):
        if c == "U": y += 1
        elif c == "D": y -= 1
        elif c == "L": x -= 1
        else: x += 1
        seen.add((x, y)); xs.append(x); ys.append(y)
        maxd = max(maxd, abs(x) + abs(y))
        if first_back < 0 and (x, y) == (0, 0): first_back = i
    if v == 0: return "%d %d" % (x, y)
    if v == 1: return str(maxd)
    if v == 2: return str(len(seen))
    if v == 3: return str(first_back)
    return str((max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1))


ROBOT_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    string s; cin >> s;
    int x = 0, y = 0, maxd = 0, first = -1;
    set<pair<int,int>> seen; seen.insert({0,0});
    int minx = 0, maxx = 0, miny = 0, maxy = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == 'U') y++;
        else if (s[i] == 'D') y--;
        else if (s[i] == 'L') x--;
        else x++;
        seen.insert({x, y});
        maxd = max(maxd, abs(x) + abs(y));
        minx = min(minx, x); maxx = max(maxx, x);
        miny = min(miny, y); maxy = max(maxy, y);
        if (first < 0 && x == 0 && y == 0) first = i + 1;
    }
    if (MODE == 0) cout << x << " " << y << "\n";
    else if (MODE == 1) cout << maxd << "\n";
    else if (MODE == 2) cout << seen.size() << "\n";
    else if (MODE == 3) cout << first << "\n";
    else cout << 1LL * (maxx - minx + 1) * (maxy - miny + 1) << "\n";
    return 0;
}
"""

fam("robot", ROBOT_STORIES, [
    V("按 U/D/L/R 指令移动后，输出最终坐标（向右为 x 正方向）。",
      "一行一个由 U、D、L、R 组成的指令串。",
      "输出一行两个整数 x y。",
      "8 ≤ |s| ≤ 16。",
      ["模拟", "坐标"], 2,
      "U 让 y+1，D 让 y-1，L 让 x-1，R 让 x+1。",
      "起点是 (0,0)。"),
    V("求移动过程中离出发点最远的曼哈顿距离。",
      "一行一个指令串。",
      "输出一个整数，表示 max(|x|+|y|)。",
      "8 ≤ |s| ≤ 16。",
      ["模拟", "最值"], 2,
      "每走一步就算一次 |x|+|y|，更新最大值。",
      "起点距离为 0，也要参与。"),
    V("求机器人一共踏过多少个不同的格子（包括起点）。",
      "一行一个指令串。",
      "输出一个整数，表示不同格子数。",
      "8 ≤ |s| ≤ 16。",
      ["模拟", "集合"], 2,
      "把每个经过的 (x,y) 放进 set。",
      "重复经过的格子只算一次。"),
    V("求机器人第一次回到原点的步数；回不来输出 -1。",
      "一行一个指令串。",
      "输出一个整数，表示第一次回到原点的步数。",
      "8 ≤ |s| ≤ 16。",
      ["模拟", "首次返回"], 2,
      "每走一步判断是否回到 (0,0)。",
      "先记下第一次，后面的返回不用管。"),
    V("求机器人到过的所有格子围成的最小矩形面积（包含边界格）。",
      "一行一个指令串。",
      "输出一个整数，表示矩形面积。",
      "8 ≤ |s| ≤ 16。",
      ["模拟", "包围盒"], 2,
      "维护 x 的最小值、最大值和 y 的最小值、最大值。",
      "面积 = (maxx-minx+1)*(maxy-miny+1)。"),
], ROBOT_CPP, solve_robot, rand_robot)

# 17. 第 k 大、中位数、前 k 和、第 k 个不同值、众数
KTH_STORIES = [
    ("花果园二手房的第 k 高挂牌价",
     "花果园的二手房挂牌价高低不一。中介想知道第 k 高的挂牌价，好给客户一个参考。"),
    ("贵阳中考录取分的中位数",
     "贵阳中考成绩出来后，学校想看看录取分数的中位数，判断整体水平。"),
    ("青云路营业额的前 k 名",
     "青云路夜市一天结束后，管理员想把营业额最高的 k 个摊位加起来，看看头部摊位的贡献。"),
    ("观山湖马拉松的第 k 个不同成绩",
     "观山湖马拉松记录了一批完赛成绩，很多人成绩相同。裁判想知道第 k 个不同的成绩是多少。"),
    ("数博会预约时段的众数",
     "数博会预约系统按小时记录预约人数。工作人员想知道哪个时段最热门；并列时取较早的时段。"),
]


def rand_kth(v, rng):
    n = rng.randint(5, 12)
    a = [rng.randint(0, 50) for _ in range(n)]
    if v == 0:
        return "%d %d\n%s" % (n, rng.randint(1, n), " ".join(map(str, a)))
    if v == 1 or v == 4:
        return "%d\n%s" % (n, " ".join(map(str, a)))
    if v == 2:
        return "%d %d\n%s" % (n, rng.randint(1, n), " ".join(map(str, a)))
    k = rng.randint(1, len(set(a)))
    return "%d %d\n%s" % (n, k, " ".join(map(str, a)))


def solve_kth(v, t):
    lines = _lines(t)
    if v in (0, 2, 3):
        n, k = map(int, lines[0].split())
    else:
        n = int(lines[0]); k = None
    a = list(map(int, lines[1].split()))
    a.sort()
    if v == 0: return str(a[n - k])
    if v == 1: return str(a[(n - 1) // 2])
    if v == 2: return str(sum(a[n - k:]))
    if v == 3:
        u = sorted(set(a))
        return str(u[k - 1])
    cnt = {}
    for x in a: cnt[x] = cnt.get(x, 0) + 1
    best = max(cnt.values())
    return str(min(x for x in cnt if cnt[x] == best))


KTH_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n; cin >> n;
    int k = 0;
    if (MODE == 0 || MODE == 2 || MODE == 3) cin >> k;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    sort(a.begin(), a.end());
    if (MODE == 0) cout << a[n - k] << "\n";
    else if (MODE == 1) cout << a[(n - 1) / 2] << "\n";
    else if (MODE == 2) { long long s = 0; for (int i = n - k; i < n; i++) s += a[i]; cout << s << "\n"; }
    else if (MODE == 3) {
        vector<int> u;
        for (int i = 0; i < n; i++) if (i == 0 || a[i] != a[i-1]) u.push_back(a[i]);
        cout << u[k - 1] << "\n";
    } else {
        int best = 0, ans = a[0];
        for (int i = 0; i < n; ) {
            int j = i; while (j < n && a[j] == a[i]) j++;
            if (j - i > best) { best = j - i; ans = a[i]; }
            i = j;
        }
        cout << ans << "\n";
    }
    return 0;
}
"""

fam("kth", KTH_STORIES, [
    V("求第 k 高的挂牌价（k 从 1 开始）。",
      "第一行两个整数 n、k，第二行 n 个整数表示挂牌价。",
      "输出一个整数，表示第 k 大的价格。",
      "5 ≤ n ≤ 12，1 ≤ k ≤ n。",
      ["排序", "第 k 大"], 1,
      "升序排序后，第 k 大就是 a[n-k]。",
      "不要和“第 k 小”弄混。"),
    V("求成绩的下中位数（排序后第 ⌊(n-1)/2⌋ 个）。",
      "第一行一个整数 n，第二行 n 个整数。",
      "输出一个整数，表示下中位数。",
      "5 ≤ n ≤ 12，0 ≤ 成绩 ≤ 50。",
      ["排序", "中位数"], 1,
      "排序后取下标 (n-1)/2。",
      "偶数个时取偏小的那个。"),
    V("求营业额最高的 k 个摊位之和。",
      "第一行两个整数 n、k，第二行 n 个整数。",
      "输出一个整数，表示前 k 大之和。",
      "5 ≤ n ≤ 12，1 ≤ k ≤ n。",
      ["排序", "前缀和"], 1,
      "升序排序后，把最后 k 个数加起来。",
      "从 n-k 到 n-1 遍历。"),
    V("求第 k 个不同的成绩（从小到大）。",
      "第一行两个整数 n、k，第二行 n 个整数。",
      "输出一个整数，表示第 k 个不同的值。",
      "5 ≤ n ≤ 12，1 ≤ k ≤ 不同值个数。",
      ["排序", "去重"], 2,
      "排序后跳过重复值，数到第 k 个。",
      "不要先把所有重复都删掉再排序，先排序更简单。"),
    V("求出现次数最多的预约时段；并列取时段编号最小的。",
      "第一行一个整数 n，第二行 n 个整数表示时段编号。",
      "输出一个整数，表示众数。",
      "5 ≤ n ≤ 12，0 ≤ 编号 ≤ 50。",
      ["排序", "众数"], 2,
      "排序后统计每段连续相同值的长度。",
      "只有长度严格大于当前最大值时才换答案。"),
], KTH_CPP, solve_kth, rand_kth)

# 18. 下一个更大：值、下标、上一个、距离、数对
NEXT_STORIES = [
    ("观山湖天际线的下一栋高楼",
     "观山湖沿线有一排楼，高度依次排列。小黔想知道每栋楼右边第一栋比它高的楼有多高。"),
    ("黔灵山陡坡的下一段",
     "黔灵山步道按顺序记录每段坡度。游客想知道每段右边第一个比它陡的段是哪一段。"),
    ("南明河深水段的上一处",
     "南明河按水流方向记录每段水深。巡河员想知道每段左边第一个比它深的段有多深。"),
    ("花果园高楼的下一栋距离",
     "花果园一排高楼的高度高低错落。小黔想知道每栋楼右边第一栋更高的楼离它隔了几栋。"),
    ("贵阳气温的升温对",
     "气象站记录了连续 n 天的气温。小黔想数一数有多少对“前冷后暖”的日子（i<j 且气温 i < 气温 j）。"),
]


def rand_next(v, rng):
    n = rng.randint(5, 10)
    a = [rng.randint(0, 30) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_next(v, t):
    d = list(map(int, t.split()))
    n = d[0]; a = d[1:1 + n]
    if v == 0:
        out = []
        for i in range(n):
            nxt = next((a[j] for j in range(i + 1, n) if a[j] > a[i]), 0)
            out.append(str(nxt))
        return " ".join(out)
    if v == 1:
        out = []
        for i in range(n):
            idx = next((j + 1 for j in range(i + 1, n) if a[j] > a[i]), 0)
            out.append(str(idx))
        return " ".join(out)
    if v == 2:
        out = []
        for i in range(n):
            prev = next((a[j] for j in range(i - 1, -1, -1) if a[j] > a[i]), 0)
            out.append(str(prev))
        return " ".join(out)
    if v == 3:
        out = []
        for i in range(n):
            idx = next((j for j in range(i + 1, n) if a[j] > a[i]), -1)
            out.append(str(0 if idx < 0 else idx - i))
        return " ".join(out)
    return str(sum(1 for i in range(n) for j in range(i + 1, n) if a[i] < a[j]))


NEXT_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    int n; cin >> n; vector<int> a(n);
    for (int &x : a) cin >> x;
    if (MODE == 0 || MODE == 1 || MODE == 3) {
        vector<int> ans(n, 0);
        stack<int> st;
        for (int i = n - 1; i >= 0; i--) {
            while (!st.empty() && a[st.top()] <= a[i]) st.pop();
            if (!st.empty()) ans[i] = (MODE == 1 ? st.top() + 1 : (MODE == 3 ? st.top() - i : a[st.top()]));
            st.push(i);
        }
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? "\n" : " ");
    } else if (MODE == 2) {
        vector<int> ans(n, 0);
        stack<int> st;
        for (int i = 0; i < n; i++) {
            while (!st.empty() && a[st.top()] <= a[i]) st.pop();
            if (!st.empty()) ans[i] = a[st.top()];
            st.push(i);
        }
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? "\n" : " ");
    } else {
        long long cnt = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (a[i] < a[j]) cnt++;
        cout << cnt << "\n";
    }
    return 0;
}
"""

fam("nextgreater", NEXT_STORIES, [
    V("对每栋楼输出右边第一栋更高楼的高度；没有则输出 0。",
      "第一行一个整数 n，第二行 n 个整数表示楼高。",
      "输出一行 n 个整数，表示每栋楼的下一个更大值。",
      "5 ≤ n ≤ 10，0 ≤ 楼高 ≤ 30。",
      ["单调栈", "下一个更大"], 4,
      "从右往左维护一个单调递减的栈。",
      "栈顶就是右边第一个比当前高的楼。"),
    V("对每段输出右边第一段更陡的段的编号；没有则输出 0。",
      "第一行一个整数 n，第二行 n 个整数表示坡度。",
      "输出一行 n 个整数，表示下一个更大值的下标（从 1 开始）。",
      "5 ≤ n ≤ 10，0 ≤ 坡度 ≤ 30。",
      ["单调栈", "下标"], 4,
      "栈里存下标，比较时用 a[栈顶]。",
      "答案要输出下标而不是高度。"),
    V("对每段输出左边第一段更深的深度；没有则输出 0。",
      "第一行一个整数 n，第二行 n 个整数表示水深。",
      "输出一行 n 个整数，表示上一个更大值。",
      "5 ≤ n ≤ 10，0 ≤ 水深 ≤ 30。",
      ["单调栈", "上一个更大"], 4,
      "从左往右扫，栈里保留还没找到“左边更大”的元素。",
      "和下一个更大方向相反，注意遍历顺序。"),
    V("对每栋楼输出右边第一栋更高楼与它的间隔（隔了几栋）；没有则输出 0。",
      "第一行一个整数 n，第二行 n 个整数表示楼高。",
      "输出一行 n 个整数，表示到下一个更大元素的距离。",
      "5 ≤ n ≤ 10，0 ≤ 楼高 ≤ 30。",
      ["单调栈", "距离"], 4,
      "先求下一个更大的下标，再算 j-i。",
      "没有更大元素时输出 0。"),
    V("数一数有多少对 i<j 满足 a[i] < a[j]。",
      "第一行一个整数 n，第二行 n 个整数表示气温。",
      "输出一个整数，表示升温对数量。",
      "5 ≤ n ≤ 10，0 ≤ 气温 ≤ 30。",
      ["枚举", "计数"], 2,
      "n 很小，直接双重循环枚举 i<j。",
      "只有严格小于才算一对。"),
], NEXT_CPP, solve_next, rand_next)

# 19. 网格路径：最小和、方案数、最大和、三角形、最小化最大值
MINPATH_STORIES = [
    ("花果园送货的最短路线",
     "花果园的送货员从左上角出发，只能向右或向下走到右下角。每个格子有一个通行时间，求总时间最小的路线。"),
    ("黔灵山爬山的路线数",
     "黔灵山的一段山路被画成网格，只能向右或向下走。小黔想知道从左上到右下一共有多少条不同路线。"),
    ("青岩石板路的最高评分",
     "青岩古镇的石板路网格里，每个格子有一个风景评分。游客只能向右或向下走，想使沿途评分之和最大。"),
    ("数博会展馆的三角形通道",
     "数博会展馆的通道排成三角形，从顶端出发每次可以走到下一行相邻的两个位置，求到底部的最小路径和。"),
    ("南明河滨河步道的最陡台阶",
     "南明河滨河步道被分成网格，每个格子有一个台阶高度差。小黔只能向右或向下走，想让整条路线中最大的高度差尽量小。"),
]


def rand_minpath(v, rng):
    if v == 3:
        n = rng.randint(3, 5)
        rows = []
        for i in range(1, n + 1):
            rows.append(" ".join(str(rng.randint(0, 9)) for _ in range(i)))
        return "%d\n%s" % (n, "\n".join(rows))
    n = rng.randint(3, 5); m = rng.randint(3, 5)
    rows = [" ".join(str(rng.randint(0, 9)) for _ in range(m)) for _ in range(n)]
    return "%d %d\n%s" % (n, m, "\n".join(rows))


def solve_minpath(v, t):
    lines = _lines(t)
    if v == 3:
        n = int(lines[0])
        tri = [list(map(int, x.split())) for x in lines[1:1 + n]]
        dp = tri[-1][:]
        for i in range(n - 2, -1, -1):
            for j in range(i + 1):
                dp[j] = tri[i][j] + min(dp[j], dp[j + 1])
        return str(dp[0])
    n, m = map(int, lines[0].split())
    g = [list(map(int, x.split())) for x in lines[1:1 + n]]
    if v == 0:
        dp = [[10**9] * m for _ in range(n)]; dp[0][0] = g[0][0]
        for i in range(n):
            for j in range(m):
                if i: dp[i][j] = min(dp[i][j], dp[i-1][j] + g[i][j])
                if j: dp[i][j] = min(dp[i][j], dp[i][j-1] + g[i][j])
        return str(dp[n-1][m-1])
    if v == 1:
        dp = [[0] * m for _ in range(n)]; dp[0][0] = 1
        for i in range(n):
            for j in range(m):
                if i: dp[i][j] += dp[i-1][j]
                if j: dp[i][j] += dp[i][j-1]
        return str(dp[n-1][m-1] % 998244353)
    if v == 2:
        dp = [[-10**9] * m for _ in range(n)]; dp[0][0] = g[0][0]
        for i in range(n):
            for j in range(m):
                if i: dp[i][j] = max(dp[i][j], dp[i-1][j] + g[i][j])
                if j: dp[i][j] = max(dp[i][j], dp[i][j-1] + g[i][j])
        return str(dp[n-1][m-1])
    dp = [[10**9] * m for _ in range(n)]; dp[0][0] = g[0][0]
    for i in range(n):
        for j in range(m):
            if i: dp[i][j] = min(dp[i][j], max(dp[i-1][j], g[i][j]))
            if j: dp[i][j] = min(dp[i][j], max(dp[i][j-1], g[i][j]))
    return str(dp[n-1][m-1])


MINPATH_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    if (MODE == 3) {
        int n; cin >> n;
        vector<vector<int>> t(n);
        for (int i = 0; i < n; i++) { t[i].resize(i + 1); for (int &x : t[i]) cin >> x; }
        vector<int> dp = t[n-1];
        for (int i = n - 2; i >= 0; i--)
            for (int j = 0; j <= i; j++) dp[j] = t[i][j] + min(dp[j], dp[j+1]);
        cout << dp[0] << "\n";
        return 0;
    }
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n, vector<int>(m));
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) cin >> g[i][j];
    if (MODE == 0) {
        vector<vector<long long>> dp(n, vector<long long>(m, 1e18)); dp[0][0] = g[0][0];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] = min(dp[i][j], dp[i-1][j] + g[i][j]);
            if (j) dp[i][j] = min(dp[i][j], dp[i][j-1] + g[i][j]);
        }
        cout << dp[n-1][m-1] << "\n";
    } else if (MODE == 1) {
        vector<vector<long long>> dp(n, vector<long long>(m, 0)); dp[0][0] = 1;
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] += dp[i-1][j];
            if (j) dp[i][j] += dp[i][j-1];
            dp[i][j] %= 998244353;
        }
        cout << dp[n-1][m-1] << "\n";
    } else if (MODE == 2) {
        vector<vector<long long>> dp(n, vector<long long>(m, -1e18)); dp[0][0] = g[0][0];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] = max(dp[i][j], dp[i-1][j] + g[i][j]);
            if (j) dp[i][j] = max(dp[i][j], dp[i][j-1] + g[i][j]);
        }
        cout << dp[n-1][m-1] << "\n";
    } else {
        vector<vector<long long>> dp(n, vector<long long>(m, 1e18)); dp[0][0] = g[0][0];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] = min(dp[i][j], max(dp[i-1][j], (long long)g[i][j]));
            if (j) dp[i][j] = min(dp[i][j], max(dp[i][j-1], (long long)g[i][j]));
        }
        cout << dp[n-1][m-1] << "\n";
    }
    return 0;
}
"""

fam("minpath", MINPATH_STORIES, [
    V("从左上角到右下角，只能向右或向下，求路径上数字之和的最小值。",
      "第一行两个整数 n、m；接下来 n 行，每行 m 个整数。",
      "输出一个整数，表示最小路径和。",
      "3 ≤ n, m ≤ 5，0 ≤ 数字 ≤ 9。",
      ["动态规划", "网格路径"], 3,
      "dp[i][j] 表示走到 (i,j) 的最小和。",
      "可以从上方或左方转移过来。"),
    V("从左上角到右下角，只能向右或向下，求不同路径的条数（对 998244353 取模）。",
      "第一行两个整数 n、m；接下来 n 行每行 m 个整数（数值不影响路线数）。",
      "输出一个整数，表示路径条数。",
      "3 ≤ n, m ≤ 5。",
      ["动态规划", "计数"], 3,
      "dp[i][j] = dp[i-1][j] + dp[i][j-1]。",
      "起点 dp[0][0]=1。"),
    V("从左上角到右下角，只能向右或向下，求路径上数字之和的最大值。",
      "第一行两个整数 n、m；接下来 n 行每行 m 个整数。",
      "输出一个整数，表示最大路径和。",
      "3 ≤ n, m ≤ 5，0 ≤ 数字 ≤ 9。",
      ["动态规划", "网格路径"], 3,
      "和最小路径一样，只是把 min 换成 max。",
      "初值设成很小的数。"),
    V("三角形通道从顶端走到底部，每次只能走到下一行相邻位置，求最小路径和。",
      "第一行一个整数 n；接下来 n 行，第 i 行有 i 个整数。",
      "输出一个整数，表示从顶端到底部的最小路径和。",
      "3 ≤ n ≤ 5，0 ≤ 数字 ≤ 9。",
      ["动态规划", "三角形"], 3,
      "从倒数第二行往上推，dp[j]=t[i][j]+min(dp[j],dp[j+1])。",
      "最后答案是 dp[0]。"),
    V("只能向右或向下，求一条路线，使路线中最大数字尽量小；输出这个最小可能的最大值。",
      "第一行两个整数 n、m；接下来 n 行每行 m 个整数。",
      "输出一个整数，表示最小可能的最大格子值。",
      "3 ≤ n, m ≤ 5，0 ≤ 数字 ≤ 9。",
      ["动态规划", "最小化最大值"], 4,
      "dp[i][j] 表示走到 (i,j) 时路径最大值的下界。",
      "转移时取 max(前驱 dp, 当前格子)，再对所有前驱取 min。"),
], MINPATH_CPP, solve_minpath, rand_minpath)

# 20. 括号：合法性、最少添加、最长前缀、最大深度、配对总数
BRACKET_STORIES = [
    ("甲秀楼长联的括号",
     "甲秀楼长联的注音稿里混进了圆括号。编辑想检查这些括号是否一一配对、嵌套正确。"),
    ("地铁导向牌的括号",
     "地铁导向牌上有一串括号说明。设计师发现有的括号没闭合，想知道最少补几个括号才能全部配对。"),
    ("数博会展位编号的前缀",
     "数博会展位编号用括号分组。工作人员只关心从第一个字符开始，最长的合法括号前缀有多长。"),
    ("青云路招牌的嵌套层数",
     "青云路招牌上的括号一层套一层。城管想知道最深的一层嵌套有多少层。"),
    ("电梯告示的括号对",
     "电梯告示上有一串括号。物业想知道一共有多少对成功配对的括号。"),
]


def rand_bracket(v, rng):
    n = rng.randint(6, 12)
    s = "".join(rng.choice("()") for _ in range(n))
    if v == 0 and rng.random() < 0.4:
        s = "(" * (n // 2) + ")" * (n - n // 2)
    return s


def solve_bracket(v, t):
    s = t.strip()
    if v == 0:
        bal = 0
        for c in s:
            bal += 1 if c == "(" else -1
            if bal < 0: return "NO"
        return "YES" if bal == 0 else "NO"
    if v == 1:
        bal = 0; need = 0
        for c in s:
            bal += 1 if c == "(" else -1
            if bal < 0: need += 1; bal = 0
        return str(need + bal)
    if v == 2:
        bal = 0; ans = 0
        for i, c in enumerate(s, 1):
            bal += 1 if c == "(" else -1
            if bal < 0: break
            if bal == 0: ans = i
        return str(ans)
    if v == 3:
        bal = 0; mx = 0
        for c in s:
            bal += 1 if c == "(" else -1
            mx = max(mx, bal)
        return str(mx)
    bal = 0; pairs = 0
    for c in s:
        if c == "(": bal += 1
        elif bal > 0: bal -= 1; pairs += 1
    return str(pairs)


BRACKET_CPP = r"""
#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = @MODE@;
    string s; cin >> s;
    if (MODE == 0) {
        int bal = 0; bool ok = true;
        for (char c : s) { bal += (c == '(' ? 1 : -1); if (bal < 0) ok = false; }
        cout << (ok && bal == 0 ? "YES" : "NO") << "\n";
    } else if (MODE == 1) {
        int bal = 0, need = 0;
        for (char c : s) {
            bal += (c == '(' ? 1 : -1);
            if (bal < 0) { need++; bal = 0; }
        }
        cout << need + bal << "\n";
    } else if (MODE == 2) {
        int bal = 0, ans = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            bal += (s[i] == '(' ? 1 : -1);
            if (bal < 0) break;
            if (bal == 0) ans = i + 1;
        }
        cout << ans << "\n";
    } else if (MODE == 3) {
        int bal = 0, mx = 0;
        for (char c : s) { bal += (c == '(' ? 1 : -1); mx = max(mx, bal); }
        cout << mx << "\n";
    } else {
        int bal = 0, pairs = 0;
        for (char c : s) {
            if (c == '(') bal++;
            else if (bal > 0) { bal--; pairs++; }
        }
        cout << pairs << "\n";
    }
    return 0;
}
"""

fam("bracket", BRACKET_STORIES, [
    V("判断整串括号是否合法（每个左括号都有匹配的右括号，且嵌套正确）。",
      "一行一个只含 ( 和 ) 的字符串。",
      "合法输出 YES，否则输出 NO。",
      "6 ≤ |s| ≤ 12。",
      ["栈", "括号匹配"], 2,
      "遇到左括号计数加一，右括号减一。",
      "中途计数变成负数或最后不为 0 都不合法。"),
    V("最少补多少个括号，才能让整串括号合法？",
      "一行一个只含 ( 和 ) 的字符串。",
      "输出一个整数，表示最少需要添加的括号数。",
      "6 ≤ |s| ≤ 12。",
      ["贪心", "括号匹配"], 3,
      "遇到多余的右括号就补一个左括号，最后剩下的左括号也要补右括号。",
      "用一个 need 记已经补了几个。"),
    V("从第一个字符开始，最长的合法括号前缀有多长？遇到非法就停止。",
      "一行一个只含 ( 和 ) 的字符串。",
      "输出一个整数，表示最长合法前缀的长度。",
      "6 ≤ |s| ≤ 12。",
      ["括号匹配", "前缀"], 3,
      "从左往右扫，计数一旦变成负数就立刻停止。",
      "合法前缀要求任意前缀计数非负。"),
    V("求整串括号的最大嵌套深度。",
      "一行一个只含 ( 和 ) 的字符串。",
      "输出一个整数，表示最大深度。",
      "6 ≤ |s| ≤ 12。",
      ["括号匹配", "深度"], 2,
      "每遇到左括号深度加一，同时更新最大值。",
      "遇到右括号深度减一，但不用更新答案。"),
    V("求一共有多少对成功配对的括号（每个右括号匹配左边最近的未匹配左括号）。",
      "一行一个只含 ( 和 ) 的字符串。",
      "输出一个整数，表示匹配对数。",
      "6 ≤ |s| ≤ 12。",
      ["栈", "配对"], 2,
      "维护未匹配左括号的数量。",
      "右括号来时有左括号就配对并减一，否则丢弃。"),
], BRACKET_CPP, solve_bracket, rand_bracket)


def build():
    PROBLEMS.clear()
    SOL.clear()
    for fi, f in enumerate(FAMILIES):
        for vi in range(5):
            num = fi * 5 + vi + 1
            pid = "gy-%03d" % num
            title, story = f["stories"][vi]
            meta = f["variants"][vi]
            rng = random.Random("guiyang2-" + pid)
            cases = [f["rand"](vi, rng) for _ in range(6)]
            outs = [f["solve"](vi, c).strip("\n") for c in cases]
            cpp = f["cpp"][vi] if isinstance(f["cpp"], list) else f["cpp"].replace("@MODE@", str(vi))
            PROBLEMS.append({
                "id": pid, "kind": "local", "chapter": 0,
                "chapter_title": "贵阳生活 100 题",
                "label": "GY-%03d" % num, "title": title,
                "difficulty": meta["diff"],
                "difficulty_label": LABELS[meta["diff"]],
                "time_limit": 2.0,
                "statement_md": story + "\n\n**任务**：" + meta["task"],
                "input_md": meta["input"], "output_md": meta["output"],
                "constraints_md": meta["cons"],
                "hint_md": "\n".join(meta["hints"]), "hints": list(meta["hints"]),
                "note_md": "", "tags": list(meta["tags"]),
                "sample_n": 1,
                "cases": cases, "solve": lambda t, v=vi, f=f: f["solve"](v, t),
                "source": "本地 OJ 原创 · 贵阳生活 100 题（v2）",
                "samples": [{"in": cases[0], "out": outs[0]}],
                "tests": [{"in": cases[i], "out": outs[i]} for i in range(len(cases))],
            })
            SOL[pid] = cpp


build()
