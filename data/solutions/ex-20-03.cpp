#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const long long INF = (long long)1e18;
const int MOD = 1000000007;
struct Edge { int to; long long w; };
vector<Edge> g[MAXN];
long long dist[MAXN];
int cnt[MAXN];                       // 到每个点的最短路条数

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    for (int i = 1; i <= n; i++) dist[i] = INF;
    dist[1] = 0;
    cnt[1] = 1;                      // 到起点自身有 1 条空路径
    priority_queue<pair<long long, int>,
                   vector<pair<long long, int>>,
                   greater<pair<long long, int>>> pq;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;   // 过期记录
        for (auto e : g[u]) {
            long long nd = d + e.w;
            if (nd < dist[e.to]) {
                dist[e.to] = nd;
                cnt[e.to] = cnt[u];              // 换了一条更短的路
                pq.push({nd, e.to});
            } else if (nd == dist[e.to]) {
                cnt[e.to] = (cnt[e.to] + cnt[u]) % MOD;   // 又一条等长的路
            }
        }
    }
    cout << cnt[n] << "\n";
    return 0;
}
