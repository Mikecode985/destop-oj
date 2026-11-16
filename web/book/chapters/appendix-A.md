# 附录 A　竞赛代码模板库

> 这一页的模板都是**片段**，用的时候拼进你的缺省源里。每个模板都标了"什么时候用"和"易错点"。
> 比赛前请自己手敲一遍、调通一遍；抄来的模板在紧张时最容易用错。

## A.1 缺省源

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
#include <queue>
#include <cstring>
using namespace std;

int main() {
    ios::sync_with_stdio(false);   // 关掉 cin/cout 与 stdio 的同步，快很多
    cin.tie(nullptr);              // 解除 cin 和 cout 的绑定

    int n;
    cin >> n;
    // 你的代码写在这里

    return 0;
}
```

> 学习阶段**不要**用 `#include <bits/stdc++.h>`：它会把所有头文件一次塞进来，编译变慢，而且你不知道每个容器来自哪个头文件。比赛时可以用，但要知道自己在偷懒。

## A.2 快读（卡常数时再上）

```cpp
inline int readInt() {
    int x = 0, f = 1;
    char c = getchar();
    while (c < '0' || c > '9') {        // 跳过空格、换行、负号
        if (c == '-') f = -1;
        c = getchar();
    }
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = getchar();
    }
    return x * f;
}
```

**什么时候用**：输入量超过 10^6 个数，且 `cin` 已经开了 `sync_with_stdio(false)` 还超时。
**易错点**：读到文件结尾时 `c` 会一直是 EOF，需要判断；返回值记得乘符号。

## A.3 数论三件套

```cpp
long long gcd(long long a, long long b) {      // 最大公约数，O(log n)
    while (b) { long long t = a % b; a = b; b = t; }
    return a;
}

long long qpow(long long a, long long b, long long mod) {   // a^b % mod
    long long res = 1 % mod;
    a %= mod;
    while (b) {
        if (b & 1) res = res * a % mod;         // 注意溢出：mod 很大时用 __int128
        a = a * a % mod;
        b >>= 1;
    }
    return res;
}

long long C(long long n, long long m) {         // 组合数，n 较小（≤ 60）时可用
    if (m < 0 || m > n) return 0;
    long long res = 1;
    for (long long i = 1; i <= m; i++) res = res * (n - m + i) / i;
    return res;
}
```

**易错点**：`C(n,m)` 这个写法依赖"先乘后除能整除"，只在结果不超过 `long long` 时对它成立；要取模请用"阶乘 + 逆元"（第 29、30 章）。

## A.4 二分三模板

```cpp
// ① 在有序数组 a[0..n-1] 里找第一个 >= x 的位置（找不到返回 n）
int lowerBound(int a[], int n, int x) {
    int l = 0, r = n;                  // 答案范围 [l, r]
    while (l < r) {
        int mid = l + (r - l) / 2;      // 防溢出
        if (a[mid] >= x) r = mid;
        else l = mid + 1;
    }
    return l;
}

// ② 二分答案：求最小的 x，使 check(x) 为真（check 必须单调）
int binaryAnswer(int lo, int hi) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (check(mid)) hi = mid;       // mid 可行，答案在 [lo, mid]
        else lo = mid + 1;              // mid 不可行，答案在 [mid+1, hi]
    }
    return lo;
}

// ③ 浮点二分：求方程的根，固定迭代 100 次比写 eps 稳
double binaryDouble(double lo, double hi) {
    for (int iter = 0; iter < 100; iter++) {
        double mid = (lo + hi) / 2;
        if (ok(mid)) hi = mid;
        else lo = mid;
    }
    return lo;
}
```

**易错点**：边界到底是 `mid` 还是 `mid ± 1`，取决于"mid 有没有可能是答案"；同一份代码里只允许用一种写法。

## A.5 数据结构

```cpp
// 并查集：O(α(n))，近似 O(1)
int fa[MAXN];
void initDSU(int n) { for (int i = 1; i <= n; i++) fa[i] = i; }
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }   // 路径压缩
bool unite(int x, int y) {
    x = find(x); y = find(y);
    if (x == y) return false;
    fa[x] = y;                       // 想更稳就加按秩合并
    return true;
}

// 树状数组：单点加、前缀和，O(log n)
long long bit[MAXN];
void add(int i, long long v) {
    for (; i <= n; i += i & -i) bit[i] += v;
}
long long sum(int i) {               // a[1] + ... + a[i]
    long long s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}

// 线段树：区间加、区间和（懒标记）
long long tree[MAXN * 4], lazy[MAXN * 4];
void pushdown(int p, int l, int r) {
    if (lazy[p] == 0) return;
    int mid = (l + r) / 2;
    tree[p * 2] += lazy[p] * (mid - l + 1);
    tree[p * 2 + 1] += lazy[p] * (r - mid);
    lazy[p * 2] += lazy[p];
    lazy[p * 2 + 1] += lazy[p];
    lazy[p] = 0;
}
void update(int p, int l, int r, int ql, int qr, long long v) {
    if (ql <= l && r <= qr) {
        tree[p] += v * (r - l + 1);
        lazy[p] += v;
        return;
    }
    pushdown(p, l, r);
    int mid = (l + r) / 2;
    if (ql <= mid) update(p * 2, l, mid, ql, qr, v);
    if (qr > mid) update(p * 2 + 1, mid + 1, r, ql, qr, v);
    tree[p] = tree[p * 2] + tree[p * 2 + 1];
}
```

**易错点**：线段树的数组要开 `4 × MAXN`；`mid` 用 `(l + r) / 2` 时注意 `l + r` 不要溢出（数组下标一般没事）。

## A.6 图论模板

```cpp
// 邻接表建图：u -> v，边权 w
vector<pair<int, int>> g[MAXN];       // (邻接点, 边权)
g[u].push_back({v, w});

// 堆优化 Dijkstra：单源最短路，O(m log m)，不能有负权
long long dis[MAXN];
void dijkstra(int s, int n) {
    fill(dis + 1, dis + n + 1, LLONG_MAX / 2);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>,
                   greater<pair<long long, int>>> pq;
    dis[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top(); pq.pop();
        if (d != dis[u]) continue;     // 过期状态，跳过
        for (auto [v, w] : g[u]) {
            if (dis[v] > d + w) {
                dis[v] = d + w;
                pq.push({dis[v], v});
            }
        }
    }
}

// Floyd：多源最短路，O(n^3)，n ≤ 500
for (int k = 1; k <= n; k++)
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            if (d[i][k] + d[k][j] < d[i][j]) d[i][j] = d[i][k] + d[k][j];

// Kruskal：最小生成树，O(m log m)
int kruskal(int n, vector<tuple<int, int, int>> edges) {  // (w, u, v)
    sort(edges.begin(), edges.end());
    initDSU(n);
    int cnt = 0, total = 0;
    for (auto [w, u, v] : edges) {
        if (unite(u, v)) { total += w; cnt++; if (cnt == n - 1) break; }
    }
    return cnt == n - 1 ? total : -1;   // -1 表示不连通
}
```

**易错点**：Dijkstra 的 `dis` 初始值要足够大（`1e18` 级别），写成 `INT_MAX` 再相加会溢出；`LLONG_MAX` 直接加也会溢出，所以用 `LLONG_MAX / 2`。

## A.7 字符串模板

```cpp
// KMP：求模式串 p 在文本串 s 中出现的所有位置
void getNext(const string& p, vector<int>& nxt) {
    int m = p.size();
    nxt.assign(m + 1, 0);
    nxt[0] = -1;
    int i = 0, j = -1;
    while (i < m) {
        if (j == -1 || p[i] == p[j]) nxt[++i] = ++j;
        else j = nxt[j];
    }
}
void kmp(const string& s, const string& p) {
    vector<int> nxt;
    getNext(p, nxt);
    int i = 0, j = 0, n = s.size(), m = p.size();
    while (i < n) {
        if (j == -1 || s[i] == p[j]) { i++; j++; }
        else j = nxt[j];
        if (j == m) { cout << i - m << " "; j = nxt[j]; }
    }
}

// Trie：插入与查询单词出现次数
int trie[MAXN][26], tot = 0, cnt[MAXN];
void insertTrie(const string& s) {
    int p = 0;
    for (char ch : s) {
        int c = ch - 'a';
        if (!trie[p][c]) trie[p][c] = ++tot;
        p = trie[p][c];
    }
    cnt[p]++;
}
int queryTrie(const string& s) {
    int p = 0;
    for (char ch : s) {
        int c = ch - 'a';
        if (!trie[p][c]) return 0;
        p = trie[p][c];
    }
    return cnt[p];
}
```

**易错点**：KMP 的 `nxt[0] = -1` 这套写法里，`j` 是 `int` 并且允许为 -1，不要改成 `size_t`（无符号会变成巨大数）。

## A.8 对拍脚本（Windows 批处理）

把三个程序放在同一目录：`gen.exe`（造数据）、`std.exe`（暴力/标准答案）、`my.exe`（你的程序）。

```bat
@echo off
for /l %%i in (1,1,1000) do (
    gen.exe > in.txt
    std.exe < in.txt > out1.txt
    my.exe  < in.txt > out2.txt
    fc out1.txt out2.txt > nul
    if errorlevel 1 (
        echo WA on test %%i
        type in.txt
        pause
        exit /b
    )
)
echo All OK
pause
```

**用法**：造数据的小程序里用 `rand()` 生成小规模、带边界的数据；先让数据规模小（比如 n ≤ 10），确认对拍能跑通，再放大。

## A.9 比赛检查清单（打印版）

```
提交前 10 秒检查：
□ 数组开够了吗（+5 或 +10 冗余）
□ 会不会溢出（long long）
□ 初始值对吗（最大/最小/全负/全正）
□ 多组数据清空了吗
□ 输出格式对吗（空格/换行/小数/大小写）
□ 边界样例试了吗（n=1、n=0、最大值）
□ 复杂度会超时吗
□ 交的是最新代码吗
```

> 模板是拐杖，不是腿。用得越多，越要知道每一行为什么这么写。
