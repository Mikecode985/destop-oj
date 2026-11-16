#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> d(n + 1, -1);
    queue<int> q;
    d[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u])
            if (d[v] == -1) { d[v] = d[u] + 1; q.push(v); }
    }
    for (int i = 1; i <= n; i++) cout << d[i] << (i == n ? '\n' : ' ');
    return 0;
}
