#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 27～28 章可编程习题。"""
from bisect import bisect_left
from collections import deque

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 27 章
def p2701(t):
    d = t.split()
    n, m = int(d[0]), int(d[1])
    MOD = 1000000007
    if m == 1 or n == 1:
        return "1"
    prev = [1] * (m + 1)
    for _ in range(2, n + 1):
        cur = [0] * (m + 1)
        cur[1] = 1
        for j in range(2, m + 1):
            cur[j] = (cur[j - 1] + prev[j]) % MOD
        prev = cur
    return str(prev[m])


add(id="p-27-01", chapter=27, label="习题 27-1", title="网格路径数（滚动数组）",
    difficulty=1,
    statement_md="一个 n 行 m 列的网格，从左上角走到右下角，每步只能向右或向下，求走法数（对 10^9+7 取模）。原写法开 `f[n][m]` 的二维数组；请改成一维滚动数组，并说明 j 该从小到大还是从大到小循环，为什么。\n\n本题是第 27 章习题 1。",
    input_md="一行两个整数 n、m（1 ≤ n, m ≤ 1000）。",
    output_md="一个整数，表示走法数对 10^9+7 取模。",
    constraints_md="1 ≤ n, m ≤ 1000。",
    hint_md="滚动数组里 `f[j] = f[j] + f[j-1]`，j 必须从小到大（因为 `f[j-1]` 表示本行刚更新过的左边格子）。",
    tags=["DP", "滚动数组"],
    cases=["2 2", "1 5", "3 3", "1000 1000", "1 1"],
    solve=p2701)

def p2702(t):
    n = int(t.split()[0])
    M = 1000000007
    K = 8
    buf = [0] * K
    buf[0] = 1
    total = 1
    if n == 0:
        return "1"
    pos = 1
    for i in range(1, n + 1):
        v = total % M
        old = buf[pos % K]
        buf[pos % K] = v
        pos += 1
        total = (total + v - old) % M
    return str(v)


add(id="p-27-02", chapter=27, label="习题 27-2", title="八项递推（前缀和优化）",
    difficulty=2,
    statement_md="小黔的转移是 `dp[i] = dp[i-1] + dp[i-2] + ... + dp[i-8]`（下标为负的项按 0 算），`dp[0] = 1`，n ≤ 5×10^6。请用「维护一个滚动窗口和」把单次转移从 8 次加法降到常数次，写出核心代码，并说明取模后相减为负怎么办。\n\n本题是第 27 章习题 2。",
    input_md="一行一个整数 n（0 ≤ n ≤ 5×10^6）。",
    output_md="一个整数，表示 dp[n] 对 10^9+7 取模。",
    constraints_md="0 ≤ n ≤ 5×10^6。",
    hint_md="记 `S[i] = dp[i-1]+...+dp[i-8]`，则 `dp[i]=S[i]`，`S[i+1] = S[i] + dp[i] - dp[i-8]`；减出负数就 `+MOD`。",
    tags=["DP", "前缀和优化"],
    cases=["0", "1", "2", "9", "100", "5000000"],
    solve=p2702)

def p2703(t):
    d = t.split()
    n, k = int(d[0]), int(d[1])
    a = list(map(int, d[1 + 1:1 + 1 + n]))
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + a[i]
    # 求 max(pre[i] - min(pre[j])), i-k <= j < i
    dq = deque()
    best = -10 ** 30
    for i in range(1, n + 1):
        while dq and dq[0] < i - k:
            dq.popleft()
        # 先把 pre[i-1] 放进窗口
        j = i - 1
        while dq and pre[dq[-1]] >= pre[j]:
            dq.pop()
        dq.append(j)
        if dq and pre[i] - pre[dq[0]] > best:
            best = pre[i] - pre[dq[0]]
    return str(best)


add(id="p-27-03", chapter=27, label="习题 27-3", title="长度不超过 k 的最大子段和",
    difficulty=3,
    statement_md="给定 n 个整数（可能有负数）和窗口长度 k，求「长度不超过 k 的连续子段」的最大和。提示：用前缀和把子段和变成两个前缀和相减，再用单调队列维护窗口内的最小前缀和。\n\n本题是第 27 章习题 3。",
    input_md="第一行两个整数 n、k（1 ≤ n ≤ 10^5，1 ≤ k ≤ n）。\n第二行 n 个整数（|a[i]| ≤ 10^9）。",
    output_md="一个整数，表示最大子段和（至少取一个数）。",
    constraints_md="1 ≤ n ≤ 10^5，1 ≤ k ≤ n，答案用 `long long`。",
    hint_md="枚举右端点 i，维护 `pre[j]`（`i-k ≤ j ≤ i-1`）的单调递增队列，答案取 `pre[i] - pre[队首]` 的最大值。",
    tags=["DP 优化", "单调队列"],
    cases=["5 2\n1 -2 3 4 -1", "3 1\n-5 -2 -9", "1 1\n7", "6 6\n-1 -2 -3 -4 -5 -6",
           "5 3\n2 -1 2 -1 2"],
    solve=p2703)

# ================================================================ 第 28 章
def p2801(t):
    lines = t.strip().splitlines()
    p = 0
    n = int(lines[p]); p += 1
    mp = {}
    for _ in range(n):
        s = lines[p].strip(); p += 1
        mp[s] = mp.get(s, 0) + 1
    q = int(lines[p]); p += 1
    out = []
    for _ in range(q):
        s = lines[p].strip(); p += 1
        out.append(str(mp.get(s, 0)))
    return "\n".join(out)


add(id="p-28-01", chapter=28, label="习题 28-1", title="字典树查词频",
    difficulty=1,
    statement_md="读入 n 个单词，再读入 q 次询问，每次给一个单词，输出它在 n 个单词里出现的次数。先用 `map` 写一遍，再用字典树（Trie）写一遍，比较两者的时间与空间。\n\n本题对应第 28 章「字符串算法」中的 Trie（28.4）。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行一个小写单词（长度 ≤ 20）。\n接下来一行一个整数 q（1 ≤ q ≤ 10^5）。\n接下来 q 行，每行一个小写单词。",
    output_md="对每次询问输出一行，表示出现次数（没出现输出 0）。",
    constraints_md="1 ≤ n, q ≤ 10^5，单词长度 ≤ 20。",
    hint_md="字典树每个代表「单词结尾」的结点记一个 `cnt`；查询时沿路径走，走不下去就是 0。",
    tags=["字典树", "字符串"],
    cases=["3\napple\napp\nbanana\n3\napp\napple\ncat", "1\na\n1\na", "2\nab\nab\n1\nab",
           "3\nabc\nabd\nabe\n3\nab\nabc\nzzz"],
    solve=p2801)

def p2802(t):
    lines = t.strip().splitlines()
    p = 0
    n = int(lines[p]); p += 1
    words = [lines[p + i].strip() for i in range(n)]
    p += n
    q = int(lines[p]); p += 1
    out = []
    for i in range(q):
        pre = lines[p + i].strip()
        c = 0
        for w in words:
            if w.startswith(pre):
                c += 1
        out.append(str(c))
    return "\n".join(out)


add(id="p-28-02", chapter=28, label="习题 28-2", title="前缀计数（Trie 结点计数）",
    difficulty=2,
    statement_md="读入 n 个单词，再读入 q 个前缀，问每个前缀是多少个单词的前缀。要求每次询问 O(长度)，提示：字典树每个结点记「有多少单词经过这里」。\n\n本题是第 28 章「字符串算法」的 Trie 应用。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行一个小写单词（长度 ≤ 20）。\n接下来一行一个整数 q（1 ≤ q ≤ 10^5）。\n接下来 q 行，每行一个前缀。",
    output_md="对每个前缀输出一行，表示以它为前缀的单词个数。",
    constraints_md="1 ≤ n, q ≤ 10^5，单词长度 ≤ 20。",
    hint_md="插入单词时每经过一个结点就 `cnt++`；查询沿前缀走到底，返回该结点的 `cnt`。",
    tags=["字典树"],
    cases=["3\napple\napp\nbanana\n3\napp\nb\nz", "1\nabc\n2\na\nabcd", "2\nab\nac\n2\na\nb"],
    solve=p2802)

def p2803(t):
    s = t.strip()
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    p = n - pi[n - 1]
    if n % p == 0:
        return str(p)
    return str(n)


add(id="p-28-03", chapter=28, label="习题 28-3", title="最小循环节（Z 函数）",
    difficulty=2,
    statement_md="给一个字符串 s，如果它能由某个更短的串重复若干次得到，输出那个最短串的长度；否则输出 n。要求用 Z 函数 O(n)。提示：考察 `z[i]` 与 `n - i` 的关系，以及 n 能否被周期整除。\n\n本题是第 28 章习题 3。",
    input_md="一行一个小写字符串（1 ≤ 长度 ≤ 10^6）。",
    output_md="一个整数，表示最小循环节长度。",
    constraints_md="1 ≤ 长度 ≤ 10^6。",
    hint_md="用 KMP 前缀函数更直接：`p = n - pi[n-1]`；只有 `n % p == 0` 时 p 才是最小循环节，否则答案是 n。",
    tags=["字符串", "Z 函数"],
    cases=["ababab", "abcabcabc", "abcd", "a", "aaaaaa", "abababa"],
    solve=p2803)

def p2804(t):
    lines = t.strip().splitlines()
    p = 0
    n = int(lines[p]); p += 1
    words = sorted(lines[p + i].strip() for i in range(n))
    p += n
    q = int(lines[p]); p += 1
    out = []
    for i in range(q):
        pre = lines[p + i].strip()
        idx = bisect_left(words, pre)
        if idx < n and words[idx].startswith(pre):
            out.append(words[idx])
        else:
            out.append("NONE")
    return "\n".join(out)


add(id="p-28-04", chapter=28, label="习题 28-4", title="前缀下字典序最小的词",
    difficulty=2,
    statement_md="在 Trie 上增加一个功能：查询某个前缀下字典序最小的词。请说明需要给每个结点额外存什么信息，以及插入时怎么维护。\n\n本题是第 28 章习题 4。这里用标准输入输出实现，若没有任何单词以该前缀开头，输出 `NONE`。",
    input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行一个小写单词（长度 ≤ 20）。\n接下来一行一个整数 q（1 ≤ q ≤ 10^5）。\n接下来 q 行，每行一个前缀。",
    output_md="对每个前缀输出一行：字典序最小的、以它为前缀的单词；不存在输出 `NONE`。",
    constraints_md="1 ≤ n, q ≤ 10^5，单词长度 ≤ 20。",
    hint_md="每个结点存「子树里字典序最小的完整单词」，插入时从根一路更新；或者直接对单词排序后二分查找。",
    tags=["字典树", "字符串"],
    cases=["3\nbanana\napple\napp\n3\napp\nban\nzz", "1\nabc\n2\na\nab",
           "3\nb\naa\nab\n2\na\nb"],
    solve=p2804)

def p2805(t):
    lines = [x for x in t.strip().splitlines() if x != ""]
    s = lines[0].strip()
    p = lines[1].strip()
    n, m = len(s), len(p)
    nxt = [0] * m
    k = 0
    for i in range(1, m):
        while k and p[i] != p[k]:
            k = nxt[k - 1]
        if p[i] == p[k]:
            k += 1
        nxt[i] = k
    cnt = 0
    k = 0
    for i in range(n):
        while k and s[i] != p[k]:
            k = nxt[k - 1]
        if s[i] == p[k]:
            k += 1
        if k == m:
            cnt += 1
            k = nxt[k - 1]
    return str(cnt)


add(id="p-28-05", chapter=28, label="习题 28-5", title="KMP 数出现次数",
    difficulty=2,
    statement_md="给定文本串 s 和模式串 p，统计 p 在 s 中出现了多少次（允许重叠，例如 s = `aaaa`、p = `aa` 时答案是 3）。要求用 KMP，O(n+m)；再用暴力匹配跑同一组数据，比较比较次数。\n\n本题是第 28 章「字符串算法」中 KMP 的应用（对应习题 1、2 的 next 数组）。",
    input_md="第一行一个字符串 s（长度 ≤ 10^6，只含小写字母）。\n第二行一个字符串 p（长度 ≤ 10^6，只含小写字母）。",
    output_md="一个整数，表示出现次数。",
    constraints_md="1 ≤ |p| ≤ |s| ≤ 10^6。",
    hint_md="匹配成功后 `cnt++`，然后 `k = next[k-1]` 继续，这样就能允许重叠。",
    tags=["KMP", "字符串"],
    cases=["aaaa\naa", "abcabcabc\nabc", "abc\nd", "a\na", "abababab\nabab"],
    solve=p2805)
