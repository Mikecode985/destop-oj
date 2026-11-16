#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 4;
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
