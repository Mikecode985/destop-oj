#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];
bool vis[MAXN];

void dfs(int u) {
    vis[u] = true;
    cout << u << " ";                  // 一到达就输出，这就是访问顺序
    for (int v : g[u]) {
        if (!vis[v]) dfs(v);           // 没去过才深入
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);             // 无向边：两个方向都存
        g[v].push_back(u);
    }
    dfs(1);
    cout << "\n";
    return 0;
}
