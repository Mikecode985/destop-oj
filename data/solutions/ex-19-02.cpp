#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];
bool vis[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    int comp = 0;
    for (int s = 1; s <= n; s++) {
        if (vis[s]) continue;
        comp++;                          // 发现一个从没访问过的连通块
        queue<int> q;
        q.push(s);
        vis[s] = true;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : g[u]) {
                if (!vis[v]) {
                    vis[v] = true;       // 入队时就标记，避免重复入队
                    q.push(v);
                }
            }
        }
    }
    cout << comp << "\n";
    return 0;
}
