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
    vector<int> pre(n + 1, 0);
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
                pre[e.first] = u.second;
                pq.push({nd, e.first});
            }
        }
    }
    if (d[n] >= INF) { cout << -1 << "\n"; return 0; }
    cout << d[n] << "\n";
    vector<int> path;
    for (int x = n; x; x = pre[x]) {
        path.push_back(x);
        if (x == 1) break;
    }
    reverse(path.begin(), path.end());
    for (size_t i = 0; i < path.size(); i++) cout << path[i] << (i + 1 == path.size() ? '\n' : ' ');
    return 0;
}
