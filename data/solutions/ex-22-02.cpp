#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const int LOG = 17;            // 2^17 = 131072 > 10^5，够跳完任何深度

vector<int> g[MAXN];
int depth[MAXN];               // 根到该点的边数，根自己为 0
int up[LOG][MAXN];             // up[k][v]：从 v 往上跳 2^k 步落到的点

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    // 第一层：BFS 从根 1 出发，算出每个点的深度和父亲
    vector<bool> vis(n + 1, false);
    queue<int> que;
    vis[1] = true;
    up[0][1] = 0;              // 根没有父亲，记 0 号点
    que.push(1);
    while (!que.empty()) {
        int u = que.front();
        que.pop();
        for (int v : g[u]) {
            if (!vis[v]) {
                vis[v] = true;
                depth[v] = depth[u] + 1;
                up[0][v] = u;
                que.push(v);
            }
        }
    }

    // 第二层：跳 2^k 步 = 先跳 2^(k-1) 步再跳 2^(k-1) 步
    for (int k = 1; k < LOG; k++)
        for (int v = 1; v <= n; v++)
            up[k][v] = up[k - 1][up[k - 1][v]];

    while (q--) {
        int a, b;
        cin >> a >> b;
        if (depth[a] < depth[b]) swap(a, b);       // 让 a 是更深的那一个
        int diff = depth[a] - depth[b];
        for (int k = 0; k < LOG; k++)
            if (diff >> k & 1) a = up[k][a];       // 按二进制位跳，把深度差抹平
        if (a == b) { cout << a << "\n"; continue; }   // 浅的那个就是祖先
        for (int k = LOG - 1; k >= 0; k--)
            if (up[k][a] != up[k][b]) {            // 没撞上就先跳过去
                a = up[k][a];
                b = up[k][b];
            }
        cout << up[0][a] << "\n";                  // 停在了 LCA 的两个儿子上
    }
    return 0;
}
