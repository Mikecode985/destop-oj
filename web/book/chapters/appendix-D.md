# 附录 D　术语中英对照与 STL 速查

读英文题面、翻国外题解时，最别扭的往往不是算法，而是术语对不上号：中文说"松弛"，英文是 relaxation；中文说"状压 DP"，英文是 bitmask DP。这一份表把全书用到的术语按"中文（English）加一句话解释"列出来，遇到不认识的词先在这里查一下。第二张表是 STL 速查，写题时忘了某个操作叫什么、有多快，直接翻表。

## D.1 术语中英对照表

| 中文 | English | 一句话解释 |
|---|---|---|
| 算法 | algorithm | 解决一类问题的确定步骤 |
| 时间复杂度 | time complexity | 输入规模变大时运算次数的增长趋势 |
| 空间复杂度 | space complexity | 运行时额外占用内存的增长趋势 |
| 数组 | array | 一段连续存放的同类型数据 |
| 下标 | index | 数组里第几个位置，从 0 或 1 开始数 |
| 递归 | recursion | 函数直接或间接调用自己 |
| 边界条件 | base case | 递归停下来、不再继续调用的条件 |
| 枚举 | enumeration | 把所有可能的情况逐个试一遍 |
| 模拟 | simulation | 严格按题面描述的规则一步步往下算 |
| 贪心 | greedy | 每一步都选当前看起来最好的 |
| 分治 | divide and conquer | 把大问题分成小问题分别解决，再合并 |
| 归并排序 | merge sort | 分治版排序，核心是合并两个有序段 |
| 二分查找 | binary search | 在有序区间里每次砍掉一半 |
| 二分答案 | binary search on answer | 把"求最值"变成"判断某个值行不行" |
| 前缀和 | prefix sum | 用 `s[i] = a[1] + … + a[i]` 快速求区间和 |
| 差分 | difference array | 让区间加变成两个端点上的单点修改 |
| 离散化 | discretization | 把很大的坐标按大小压缩成排名 |
| 栈 | stack | 后进先出的结构 |
| 队列 | queue | 先进先出的结构 |
| 单调栈 | monotonic stack | 栈里元素单调递增或递减的栈 |
| 单调队列 | monotonic deque | 队里元素单调、用来维护滑动窗口最值 |
| 哈希表 | hash table | 用哈希函数把键映射到桶里，冲突另外处理 |
| 堆 | heap | 父结点总比子结点大（或小）的完全二叉树 |
| 优先队列 | priority queue | 每次取出最大或最小元素的队列 |
| 并查集 | disjoint set union (DSU) | 维护"谁和谁是一伙的"，支持合并与查询 |
| 树状数组 | Fenwick tree (binary indexed tree) | 支持单点修改、前缀查询的数组结构 |
| 线段树 | segment tree | 支持区间修改、区间查询的树形结构 |
| 图 | graph | 点与边组成的结构 |
| 连通块 | connected component | 能互相走到的点组成的一块 |
| 深度优先搜索 | depth-first search (DFS) | 一条路走到黑，走不通再退回来 |
| 广度优先搜索 | breadth-first search (BFS) | 像水波一样一圈一圈向外扩散 |
| 回溯 | backtracking | DFS 加"撤销选择"，试完一种再换下一种 |
| 剪枝 | pruning | 判断出这条路不可能有解，提前返回 |
| 最短路 | shortest path | 两点之间边权之和最小的那条路 |
| 松弛 | relaxation | 用一条更短的路径去更新距离 |
| 最小生成树 | minimum spanning tree (MST) | 边权和最小、把所有点连通的树 |
| 拓扑排序 | topological sort | 把有向无环图排成"先修在前"的顺序 |
| 有向无环图 | directed acyclic graph (DAG) | 没有有向环的图 |
| 树 | tree | 没有环的连通无向图 |
| 树的直径 | diameter of a tree | 树上距离最远的两个点之间的距离 |
| 最近公共祖先 | lowest common ancestor (LCA) | 两个结点往上走第一次相遇的祖先 |
| 动态规划 | dynamic programming (DP) | 把子问题的答案存下来，避免重复计算 |
| 状态 | state | 描述"算到哪了"的一组变量 |
| 状态转移 | state transition | 从旧状态推出新状态的式子 |
| 记忆化搜索 | memoization | 递归时把算过的答案记进数组 |
| 滚动数组 | rolling array | 只保留相邻几行，省掉一维空间 |
| 背包问题 | knapsack problem | 每件物品选或不选，在容量限制下求最优 |
| 区间 DP | interval DP | 按区间长度从小到大枚举状态的 DP |
| 状压 DP | bitmask DP | 用二进制数表示集合的 DP |
| 字符串匹配 | string matching | 在一个串里找另一个串出现的位置 |
| 字典树 | trie | 用树的路径存字符串前缀 |
| 最大公约数 | greatest common divisor (GCD) | 能同时整除两个数的最大正整数 |
| 素数 | prime | 只有 1 和自身两个因数的正整数 |
| 筛法 | sieve | 一次性筛出 1 到 n 中所有素数的方法 |
| 快速幂 | binary exponentiation | 把指数按二进制拆分，快速算 a 的 b 次方 |
| 逆元 | modular inverse | 模意义下的"倒数" |
| 取余（取模） | modulo | 除以 m 之后得到的余数 |
| 组合数 | binomial coefficient | 从 n 个里选 m 个的方案数 |
| 位运算 | bitwise operation | 与、或、异或、移位这类按二进制位做的运算 |
| 高精度 | big integer arithmetic | 用数组按位存超出 `long long` 的整数 |

## D.2 STL 容器与算法速查表

表里的复杂度是最坏情况；标了"均摊"的，偶尔一次慢操作不影响总体。哈希表写的是平均复杂度，出题人专门构造数据时可以被卡到 `O(n)`。

| 组件 | 头文件 | 常用操作 | 复杂度 | 什么时候用 |
|---|---|---|---|---|
| `vector` | `<vector>` | `push_back`、`pop_back`、`size`、`a[i]` | 均摊 `O(1)`、均摊 `O(1)`、`O(1)`、`O(1)` | 日常最常用的动态数组 |
| `vector` 二维 | `<vector>` | `vector<vector<int>> a(n, vector<int>(m))` | 同数组 | 矩阵、网格题 |
| `array` | `<array>` | `a[i]`、`size` | `O(1)` | 大小固定的数组 |
| `string` | `<string>` | `+=`、`substr`、`find`、`length` | 均摊 `O(1)`、`O(len)`、最坏 `O(n·m)`、`O(1)` | 存字符串、拼接 |
| `getline` | `<string>` | `getline(cin, s)` | `O(len)` | 读一整行，含空格 |
| `to_string` | `<string>` | `to_string(x)` | `O(位数)` | 数字转字符串 |
| `stoi` | `<string>` | `stoi(s)` | `O(len)` | 字符串转整数 |
| `pair` | `<utility>` | `first`、`second`、`make_pair` | `O(1)` | 把两个值绑在一起 |
| `tuple` | `<tuple>` | `make_tuple`、`get<0>` | `O(1)` | 三个以上绑在一起 |
| `stack` | `<stack>` | `push`、`pop`、`top`、`empty` | `O(1)` | 括号匹配、单调栈 |
| `queue` | `<queue>` | `push`、`pop`、`front`、`empty` | `O(1)` | BFS、普通排队 |
| `deque` | `<deque>` | `push_front`、`push_back`、`a[i]` | `O(1)` | 两头都要进出的队列、单调队列 |
| `priority_queue` | `<queue>` | `push`、`pop`、`top` | `O(log n)`、`O(log n)`、`O(1)` | 每次取最大值的堆 |
| `priority_queue` 小根堆 | `<queue>` | `priority_queue<int, vector<int>, greater<int>>` | `O(log n)` | 取最小值：合并果子、Dijkstra |
| 建堆 | `<queue>` | 用区间构造 `priority_queue` | `O(n)` | 一次性把 n 个数做成堆 |
| `set` | `<set>` | `insert`、`count`、`erase`、`lower_bound` | `O(log n)` | 有序去重集合 |
| `multiset` | `<set>` | `insert`、`erase` | `O(log n)` | 有序但允许重复 |
| `map` | `<map>` | `[ ]`、`insert`、`count`、`find` | `O(log n)` | 键值对，按 key 有序 |
| `unordered_set` | `<unordered_set>` | `insert`、`count`、`erase` | 平均 `O(1)` | 只查在不在、去重 |
| `unordered_map` | `<unordered_map>` | `[ ]`、`count`、`find` | 平均 `O(1)` | 计数、查表 |
| `bitset` | `<bitset>` | `set`、`reset`、`count`、位运算 | `O(n/64)` | 定长二进制集合 |
| `sort` | `<algorithm>` | `sort(a.begin(), a.end())` | `O(n log n)` | 排序首选 |
| `stable_sort` | `<algorithm>` | `stable_sort(...)` | `O(n log n)` | 需要相等元素保持原顺序 |
| `sort` 降序 | `<algorithm>` | `sort(v.rbegin(), v.rend())` | `O(n log n)` | 从大到小排 |
| `sort` 自定义 | `<algorithm>` | `sort(v.begin(), v.end(), cmp)` | `O(n log n)` | 多关键字排序 |
| `reverse` | `<algorithm>` | `reverse(a.begin(), a.end())` | `O(n)` | 翻转数组、字符串 |
| `unique` | `<algorithm>` | 先 `sort`，再 `unique` 加 `erase` | `O(n)` | 排序后去重 |
| `lower_bound` | `<algorithm>` | `lower_bound(begin, end, x)` | `O(log n)` | 第一个大于等于 x 的位置 |
| `upper_bound` | `<algorithm>` | `upper_bound(begin, end, x)` | `O(log n)` | 第一个严格大于 x 的位置 |
| `binary_search` | `<algorithm>` | `binary_search(begin, end, x)` | `O(log n)` | 只问 x 在不在 |
| 求下标 | `<algorithm>` | `lower_bound(v.begin(), v.end(), x) - v.begin()` | `O(log n)` | 二分要找位置而不是迭代器 |
| `min` / `max` | `<algorithm>` | `min(a, b)`、`max(a, b)` | `O(1)` | 取较小值、较大值 |
| `swap` | `<utility>` | `swap(a, b)` | `O(1)` | 交换两个变量 |
| `fill` | `<algorithm>` | `fill(a.begin(), a.end(), x)` | `O(n)` | 批量赋初值 |
| `count` | `<algorithm>` | `count(begin, end, x)` | `O(n)` | 数某个值出现几次 |
| `max_element` | `<algorithm>` | `max_element(begin, end)` | `O(n)` | 找最大值的位置 |
| `accumulate` | `<numeric>` | `accumulate(begin, end, 0)` | `O(n)` | 求和 |
| `accumulate` 防溢出 | `<numeric>` | `accumulate(begin, end, 0LL)` | `O(n)` | 初值写 `0LL`，结果就是 `long long` |
| `iota` | `<numeric>` | `iota(a.begin(), a.end(), 0)` | `O(n)` | 填 0、1、2、… 这样的递增序列 |
| `gcd` | `<numeric>` | `gcd(a, b)` | `O(log n)` | C++17 内置的最大公约数 |
| `next_permutation` | `<algorithm>` | `next_permutation(begin, end)` | 单次 `O(n)` | 枚举全排列 |
| `shuffle` | `<algorithm>` | `shuffle(begin, end, rng)` | `O(n)` | 随机打乱，对拍造数据 |
| `memset` | `<cstring>` | `memset(a, 0, sizeof(a))` | `O(数组大小)` | 初始化，只能按字节填 0 或 -1 |
| `__builtin_popcount` | 内置 | `__builtin_popcount(x)` | `O(1)` | 数二进制里 1 的个数 |
| `stringstream` | `<sstream>` | `ss << x`、`ss >> y` | `O(len)` | 字符串和数字互转、按空格切词 |
| 范围 `for` | — | `for (auto &x : v)` | `O(n)` | 简洁地遍历容器 |
| `map` 计数 | `<map>` | `mp[x]++` | `O(log n)` | 统计每个值出现几次 |
| `set` 去重 | `<set>` | `s.insert(x)`、`s.size()` | `O(log n)` | 边读边排序去重 |

> **三个最容易踩的坑**
> ① `size()` 返回的是无符号数，空 `vector` 上写 `v.size() - 1` 会变成一个巨大的正整数。
> ② 边遍历 `vector` 边 `erase` 会让迭代器失效，要么用下标从后往前删，要么先记下来再删。
> ③ 大数组别开在函数里（占用的是栈，几 MB 就爆栈），开成全局变量或者用 `vector`。
