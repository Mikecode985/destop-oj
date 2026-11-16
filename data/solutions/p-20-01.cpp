#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    d[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        pair<long long, int> u = pq.top();
        pq.pop();
        if (u.first != d[u.second]) continue;
        for (auto &e : g[u.second]) {
            long long nd = u.first + e.second;
            if (nd < d[e.first]) {
                d[e.first] = nd;
                pq.push({nd, e.first});
            }
        }
    }
    cout << (d[n] >= INF ? -1 : d[n]) << "\n";
    return 0;
}
