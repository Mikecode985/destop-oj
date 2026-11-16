#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, int>>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }
    const int INF = 1e9;
    vector<int> d(n + 1, INF);
    deque<int> dq;
    d[1] = 0;
    dq.push_back(1);
    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        for (auto &e : g[u]) {
            int v = e.first, w = e.second;
            if (d[u] + w < d[v]) {
                d[v] = d[u] + w;
                if (w == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    cout << (d[n] >= INF ? -1 : d[n]) << "\n";
    return 0;
}
