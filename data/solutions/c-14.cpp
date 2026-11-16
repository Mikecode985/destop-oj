#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<int>> g(n + 1);
    while (m--) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> d(n + 1, -1);
    deque<int> q;
    d[s] = 0;
    q.push_back(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        for (int v : g[u])
            if (d[v] == -1) { d[v] = d[u] + 1; q.push_back(v); }
    }
    cout << d[t] << "\n";
    return 0;
}
