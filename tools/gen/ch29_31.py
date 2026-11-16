#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 29～31 章可编程习题。"""
from math import isqrt

PROBLEMS = []


def add(**kw):
    kw.setdefault("kind", "exercise")
    kw.setdefault("sample_n", 1)
    kw.setdefault("time_limit", 2.0)
    PROBLEMS.append(kw)


# ================================================================ 第 29 章
def p2903(t):
    n = int(t.split()[0])
    if n < 2:
        return "0"
    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, isqrt(n) + 1):
        if sieve[i]:
            start = i * i
            sieve[start::i] = bytearray(len(range(start, n + 1, i)))
    return str(sum(sieve))


add(id="p-29-03", chapter=29, label="习题 29-3", title="线性筛统计素数个数",
    difficulty=2,
    statement_md="用筛法求出 1 到 n 内所有素数，统计素数个数。请说明为什么线性筛的复杂度是 O(n)，以及「`i % p == 0` 就 break」这一行在防什么（每个合数只被它最小的质因子筛一次）。\n\n本题是第 29 章习题 3。n 最大 10^7。",
    input_md="一行一个整数 n（1 ≤ n ≤ 10^7）。",
    output_md="一个整数，表示 1..n 中素数的个数。",
    constraints_md="1 ≤ n ≤ 10^7。",
    hint_md="埃氏筛 + `bytearray` 切片赋值也能在毫秒级跑完 10^7；线性筛则是每个合数只标记一次。",
    tags=["数论", "筛法"],
    cases=["1", "10", "100", "1000000", "10000000"],
    solve=p2903,
    time_limit=2.0)

def p2904(t):
    d = t.split()
    a, b, m = int(d[0]), int(d[1]), int(d[2])

    def pw(x, e, mod):
        r = 1
        x %= mod
        while e:
            if e & 1:
                r = r * x % mod
            x = x * x % mod
            e >>= 1
        return r

    return str(pw(a, b, m)) + "\n" + str(pow(a, m - 2, m))


add(id="p-29-04", chapter=29, label="习题 29-4", title="快速幂与模逆元",
    difficulty=2,
    statement_md="用快速幂求 a^b mod m，再求 a 在模 m 下的乘法逆元。请说明你用的是扩展欧几里得还是费马小定理，为什么两者能得到同一个答案。\n\n本题是第 29 章习题 4（书上算的是 `2^1000000 mod 1000000007` 和 `3^(-1) mod 1000000007`）。保证 m 是质数且 a 不是 m 的倍数。",
    input_md="一行三个整数 a、b、m（1 ≤ a < m ≤ 10^9，0 ≤ b ≤ 10^18，m 为质数）。",
    output_md="第一行 a^b mod m；第二行 a 模 m 的逆元。",
    constraints_md="1 ≤ a < m ≤ 10^9，0 ≤ b ≤ 10^18，m 为质数。",
    hint_md="费马小定理：`a^(m-1) ≡ 1`，所以逆元是 `a^(m-2) mod m`；扩展欧几里得解 `ax+my=1` 得到的是同一个 x。",
    tags=["快速幂", "逆元", "数论"],
    cases=["2 1000000 1000000007", "3 1 1000000007", "5 0 7", "123456789 987654321 1000000007"],
    solve=p2904)

def p2905(t):
    n = int(t.split()[0])
    M = 1000000007

    def mul(A, B):
        return [[(A[0][0] * B[0][0] + A[0][1] * B[1][0]) % M,
                 (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % M],
                [(A[1][0] * B[0][0] + A[1][1] * B[1][0]) % M,
                 (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % M]]

    def mpow(A, e):
        R = [[1, 0], [0, 1]]
        while e:
            if e & 1:
                R = mul(R, A)
            A = mul(A, A)
            e >>= 1
        return R

    if n == 0:
        return "0"
    base = [[1, 1], [1, 0]]
    res = mpow(base, n - 1)
    return str(res[0][0] % M)


add(id="p-29-05", chapter=29, label="习题 29-5", title="矩阵快速幂求斐波那契",
    difficulty=3,
    statement_md="用矩阵快速幂求 F(n) mod 10^9+7，其中 F(1)=F(2)=1。请说明为什么不能用递推一个一个算，以及 2×2 矩阵的 1 次方到 n 次方是怎么和斐波那契对上的。\n\n本题是第 29 章习题 5。",
    input_md="一行一个整数 n（0 ≤ n ≤ 10^18）。",
    output_md="一个整数，表示 F(n) mod 10^9+7（F(0)=0）。",
    constraints_md="0 ≤ n ≤ 10^18。",
    hint_md="`[[1,1],[1,0]]^n` 的左上角就是 F(n+1)；快速幂 O(log n)。",
    tags=["矩阵快速幂", "数论"],
    cases=["0", "1", "2", "10", "100", "1000000000000000000"],
    solve=p2905)

def p2906(t):
    d = t.split()
    p = 0
    k = int(d[p]); p += 1
    eq = []
    M = 1
    for _ in range(k):
        a, m = int(d[p]), int(d[p + 1]); p += 2
        eq.append((a, m))
        M *= m
    x = 0
    for a, m in eq:
        Mi = M // m
        x = (x + a * Mi * pow(Mi, -1, m)) % M
    return str(x % M)


add(id="p-29-06", chapter=29, label="习题 29-6", title="中国剩余定理",
    difficulty=3,
    statement_md="解同余方程组 `x ≡ a_i (mod m_i)`（模数两两互质），输出最小的非负整数解。先用书上 29.6 的构造公式手算 `x ≡ 2 (mod 3)`、`x ≡ 3 (mod 5)`、`x ≡ 2 (mod 7)`，再写程序验证；最后说明如果模数不两两互质，这个公式会出什么问题。\n\n本题是第 29 章习题 6。",
    input_md="第一行一个整数 k（1 ≤ k ≤ 3）。\n接下来 k 行，每行两个整数 a、m（0 ≤ a < m ≤ 10^4，m 两两互质）。",
    output_md="一个整数，表示最小的非负解（小于所有模数之积）。",
    constraints_md="1 ≤ k ≤ 3，0 ≤ a < m ≤ 10^4，模数两两互质。",
    hint_md="`M = Πm_i`，`M_i = M/m_i`，`t_i = M_i 在模 m_i 下的逆元`，答案 `Σ a_i·M_i·t_i mod M`。",
    tags=["数论", "中国剩余定理"],
    cases=["3\n2 3\n3 5\n2 7", "1\n5 7", "2\n1 2\n2 3", "3\n1 4\n2 5\n3 9"],
    solve=p2906)

# ================================================================ 第 30 章
def p3002(t):
    lines = t.strip().splitlines()
    p = 0
    q = int(lines[p]); p += 1
    out = []
    for _ in range(q):
        n, m, mod = map(int, lines[p].split()); p += 1
        if m > n:
            out.append("0")
            continue
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % mod
        out.append(str(fact[n] * pow(fact[m], mod - 2, mod) % mod
                       * pow(fact[n - m], mod - 2, mod) % mod))
    return "\n".join(out)


add(id="p-30-02", chapter=30, label="习题 30-2", title="组合数取模 C(n,m)",
    difficulty=2,
    statement_md="先手算 `C(10,3)`、`A(10,3)`、`C(10,7)`，验证 `C(10,3)=C(10,7)`。再用程序回答 q 次询问：每次给 n、m、p（p 是质数且 n < p），求 C(n,m) mod p。\n\n本题覆盖第 30 章习题 2，并把它推广成可判题版本。",
    input_md="第一行一个整数 q（1 ≤ q ≤ 100）。\n接下来 q 行，每行三个整数 n、m、p（0 ≤ m ≤ n ≤ 10^6，n < p ≤ 10^9，p 为质数）。",
    output_md="对每次询问输出一行，表示 C(n,m) mod p。",
    constraints_md="1 ≤ q ≤ 100，0 ≤ m ≤ n ≤ 10^6，n < p ≤ 10^9。",
    hint_md="`C(n,m) = n!/(m!(n-m)!)`；模意义下除以 x 等于乘 `x^(p-2)`（费马小定理）。",
    tags=["组合数", "逆元"],
    cases=["3\n5 2 1000000007\n10 0 1000000007\n6 3 1000000007", "1\n0 0 7",
           "2\n100 50 1000000007\n3 4 11"],
    solve=p3002)

def p3003(t):
    N = int(t.split()[0])
    primes = [2, 3, 5]
    total = 0
    for mask in range(1, 1 << 3):
        prod = 1
        bits = 0
        for i in range(3):
            if mask >> i & 1:
                prod *= primes[i]
                bits += 1
        if bits % 2 == 1:
            total += N // prod
        else:
            total -= N // prod
    return str(N - total)


add(id="p-30-03", chapter=30, label="习题 30-3", title="容斥原理",
    difficulty=2,
    statement_md="求 1 到 N 中「既不是 2 的倍数、也不是 3 的倍数、也不是 5 的倍数」的数有多少个。请用容斥写出算式，并说明每一项对应的是「被谁整除」。\n\n本题是第 30 章习题 3（书上算的是 N = 10^6，这里推广到 N ≤ 10^18）。",
    input_md="一行一个整数 N（1 ≤ N ≤ 10^18）。",
    output_md="一个整数，表示满足条件的数的个数。",
    constraints_md="1 ≤ N ≤ 10^18，答案用 `long long`。",
    hint_md="`N - N/2 - N/3 - N/5 + N/6 + N/10 + N/15 - N/30`，即「全部 - 单 + 双 - 三」。",
    tags=["容斥原理"],
    cases=["10", "1000000", "1", "30", "1000000000000000000"],
    solve=p3003)

def p3004(t):
    n = int(t.split()[0])
    M = 1000000007
    size = 2 * n
    fact = [1] * (size + 1)
    for i in range(1, size + 1):
        fact[i] = fact[i - 1] * i % M
    c = fact[size] * pow(fact[n], M - 2, M) % M * pow(fact[n], M - 2, M) % M
    return str(c * pow(n + 1, M - 2, M) % M)


add(id="p-30-04", chapter=30, label="习题 30-4", title="卡特兰数（括号匹配方案数）",
    difficulty=2,
    statement_md="n 对括号有多少种合法匹配方案？请用卡特兰数写出 n = 4 的答案（手算），并说明为什么它和「n 个元素出栈序列」是同一个问题。\n\n本题是第 30 章习题 4 的可判题版本：输出 Catalan(n) mod 10^9+7。",
    input_md="一行一个整数 n（0 ≤ n ≤ 10^5）。",
    output_md="一个整数，表示 Catalan(n) mod 10^9+7。",
    constraints_md="0 ≤ n ≤ 10^5。",
    hint_md="`Catalan(n) = C(2n, n)/(n+1)`；模意义下用费马小定理求 `(n+1)` 的逆元。",
    tags=["组合数学", "卡特兰数"],
    cases=["0", "1", "3", "4", "10", "100"],
    solve=p3004)

def p3005(t):
    n = int(t.split()[0])
    M = 1000000007
    if n == 0:
        return "1"
    if n == 1:
        return "0"
    a, b = 0, 1
    for i in range(3, n + 1):
        a, b = b, ((i - 1) * (a + b)) % M
    return str(b % M)


add(id="p-30-05", chapter=30, label="习题 30-5", title="错排问题（贺年卡）",
    difficulty=2,
    statement_md="5 个人各写一张贺年卡，打乱后重新分发，要求每个人都不能拿到自己写的那张。问有多少种分法？先用容斥手算 n=5，再写程序求 D(n) mod 10^9+7。\n\n本题是第 30 章习题 5。D(1)=0，D(2)=1。",
    input_md="一行一个整数 n（0 ≤ n ≤ 10^5）。",
    output_md="一个整数，表示 D(n) mod 10^9+7（n=0 规定为 1）。",
    constraints_md="0 ≤ n ≤ 10^5。",
    hint_md="`D(n) = (n-1)(D(n-1) + D(n-2))`：按「第 n 个人拿到谁的卡」分两类。",
    tags=["组合数学", "错排"],
    cases=["0", "1", "2", "3", "5", "100"],
    solve=p3005)

# ================================================================ 第 31 章
def p3102(t):
    n = int(t.split()[0])
    return str(bin(n).count("1"))


add(id="p-31-02", chapter=31, label="习题 31-2", title="二进制里有多少个 1",
    difficulty=1,
    statement_md="给定 n，求它的二进制表示中 1 的个数。先手算 n = 100，再用 `lowbit`（`x & -x`）的办法写一遍，验证两种方法结果一致。\n\n本题是第 31 章习题 2。",
    input_md="一行一个整数 n（0 ≤ n ≤ 10^18）。",
    output_md="一个整数，表示二进制中 1 的个数。",
    constraints_md="0 ≤ n ≤ 10^18。",
    hint_md="`while (n) { n &= n - 1; cnt++; }`；`n & (n-1)` 每次消掉最低位的 1。",
    tags=["位运算"],
    cases=["100", "0", "1", "7", "1000000000000000000"],
    solve=p3102)

def p3103(t):
    lines = [x.strip() for x in t.strip().splitlines() if x.strip() != ""]
    a = int(lines[0])
    b = int(lines[1])
    return str(a - b)


add(id="p-31-03", chapter=31, label="习题 31-3", title="高精度减法",
    difficulty=2,
    statement_md="输入两个非负整数 a、b（a ≥ b，位数可能上千，允许前导零），输出 a - b。请说明「去掉前导零」要注意什么，以及 a = b 时应该输出什么。\n\n本题是第 31 章习题 3。",
    input_md="第一行一个非负整数 a（位数 ≤ 1000）。\n第二行一个非负整数 b（位数 ≤ 1000，保证 a ≥ b）。",
    output_md="一行，表示 a - b（不带多余的前导零；结果为 0 时输出 0）。",
    constraints_md="0 ≤ 位数 ≤ 1000。",
    hint_md="按位从低位往高位减，借位 `+10` 再减；最后把高位多余的 0 去掉，全 0 就输出一个 0。",
    tags=["高精度"],
    cases=["1000\n1", "12345678901234567890\n12345678901234567889", "0\n0",
           "000123\n000045", "1000000000000000000000000000000\n999999999999999999999999999999"],
    solve=p3103)

def p3104(t):
    lines = [x.strip() for x in t.strip().splitlines() if x.strip() != ""]
    a = int(lines[0])
    b = int(lines[1])
    return str(a // b) + "\n" + str(a % b)


add(id="p-31-04", chapter=31, label="习题 31-4", title="高精度除以 int",
    difficulty=3,
    statement_md="用高精度除法求「一个最多 100 位的整数除以一个 int」的商和余数。提示：从高位到低位逐位试商，思想和小学生列竖式一样。\n\n本题是第 31 章习题 4。",
    input_md="第一行一个非负整数 a（位数 ≤ 100）。\n第二行一个正整数 b（1 ≤ b ≤ 10^9）。",
    output_md="第一行商（不带前导零，商为 0 时输出 0），第二行余数。",
    constraints_md="位数 ≤ 100，1 ≤ b ≤ 10^9。",
    hint_md="维护余数 `rem`：`cur = rem * 10 + digit`，这一位的商是 `cur / b`，`rem = cur % b`；商的最高位可能是 0，要跳过。",
    tags=["高精度"],
    cases=["100\n7", "123456789012345678901234567890\n1000", "5\n1000000000",
           "0\n3", "99999999999999999999999999999999999999999999999999\n97"],
    solve=p3104)

def p3105(t):
    s = t.strip().split()[-1]
    return str(int(s, 2))


add(id="p-31-05", chapter=31, label="习题 31-5", title="二进制转十进制（高精度）",
    difficulty=3,
    statement_md="给定一个二进制字符串（长度不超过 1000），输出它的十进制表示。提示：不能直接用 `long long`，可以反复用高精度「乘 2 加下一位」，或者用高精度除以 10 的办法。\n\n本题是第 31 章习题 5。",
    input_md="一行一个二进制串（长度 ≤ 1000，只有 0 和 1，允许前导零）。",
    output_md="一行，表示对应的十进制数（不带前导零）。",
    constraints_md="1 ≤ 长度 ≤ 1000。",
    hint_md="从最高位开始：`ans = ans * 2 + bit`，每一步都是高精度乘法和加法，O(n²)。",
    tags=["高精度", "进制转换"],
    cases=["101", "1", "0", "11111111",
           "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"],
    solve=p3105)
