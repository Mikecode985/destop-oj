#include <bits/stdc++.h>
using namespace std;

const int MAXN = 6005;
vector<int> g[MAXN];
int r[MAXN];                  // 每个人的快乐值
int fa[MAXN];                 // 直接上司
int order[MAXN];              // BFS 顺序，倒着扫就是后序
int dp0[MAXN], dp1[MAXN];     // dp0：不请他；dp1：请他

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> r[i];
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;            // u 是 v 的上司
        g[u].push_back(v);
        g[v].push_back(u);
        fa[v] = u;
    }

    int root = 1;
    for (int i = 1; i <= n; i++)
        if (fa[i] == 0) { root = i; break; }     // 没有上司的就是大老板

    int cnt = 0;
    order[++cnt] = root;
    fa[root] = 0;
    for (int head = 1; head <= cnt; head++) {    // 用 order 当队列
        int u = order[head];
        for (int v : g[u])
            if (v != fa[u]) { fa[v] = u; order[++cnt] = v; }
    }

    for (int i = n; i >= 1; i--) {               // 后序：儿子先算完
        int u = order[i];
        dp1[u] = r[u];                           // 请他，先记上他的快乐值
        dp0[u] = 0;
        for (int v : g[u]) {
            if (v == fa[u]) continue;            // 跳过上司，只看下属
            dp1[u] += dp0[v];                    // 他去了，下属不能去
            dp0[u] += max(dp0[v], dp1[v]);       // 他不去，下属随意
        }
    }
    cout << max(dp0[root], dp1[root]) << "\n";
    return 0;
}
