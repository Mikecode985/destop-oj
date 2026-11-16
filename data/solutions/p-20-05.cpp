#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
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
        g[v].push_back({u, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    vector<long long> cnt(n + 1, 0);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    d[1] = 0;
    cnt[1] = 1;
    pq.push({0, 1});
    while (!pq.empty()) {
        pair<long long, int> u = pq.top();
        pq.pop();
        if (u.first != d[u.second]) continue;
        for (auto &e : g[u.second]) {
            long long nd = u.first + e.second;
            if (nd < d[e.first]) {
                d[e.first] = nd;
                cnt[e.first] = cnt[u.second];
                pq.push({nd, e.first});
            } else if (nd == d[e.first]) {
                cnt[e.first] = (cnt[e.first] + cnt[u.second]) % MOD;
            }
        }
    }
    cout << (d[n] >= INF ? 0 : cnt[n] % MOD) << "\n";
    return 0;
}
