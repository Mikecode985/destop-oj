#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];
int fa[MAXN];                 // 每个点的父亲
int order[MAXN];              // BFS 访问顺序，倒着扫就是后序
int dp0[MAXN], dp1[MAXN];     // dp0[u]：u 不选；dp1[u]：u 选

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    // BFS 一次：拿到父亲数组和一个"父亲在前、儿子在后"的顺序
    int cnt = 0;
    order[++cnt] = 1;
    fa[1] = 0;
    for (int head = 1; head <= cnt; head++) {
        int u = order[head];
        for (int v : g[u]) {
            if (v != fa[u]) {         // 树里不走回头路
                fa[v] = u;
                order[++cnt] = v;
            }
        }
    }

    // 倒着扫：轮到 u 时，它的儿子一定都算完了
    for (int i = n; i >= 1; i--) {
        int u = order[i];
        dp1[u] = 1;                   // u 选了，先把自己记上
        dp0[u] = 0;
        for (int v : g[u]) {
            if (v == fa[u]) continue; // 只看儿子，跳过父亲
            dp1[u] += dp0[v];         // u 选了，儿子只能不选
            dp0[u] += max(dp0[v], dp1[v]);   // u 不选，儿子随意
        }
    }
    cout << max(dp0[1], dp1[1]) << "\n";
    return 0;
}
