#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<pair<pair<int, int>, long long>> edges;
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        edges.push_back({{u, v}, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    d[1] = 0;
    bool neg = false;
    for (int round = 0; round < n; round++) {
        bool changed = false;
        for (auto &e : edges) {
            int u = e.first.first, v = e.first.second;
            long long w = e.second;
            if (d[u] >= INF) continue;
            if (d[u] + w < d[v]) {
                d[v] = d[u] + w;
                changed = true;
                if (round == n - 1) neg = true;
            }
        }
        if (!changed) break;
    }
    cout << (neg ? "Yes" : "No") << "\n";
    return 0;
}
