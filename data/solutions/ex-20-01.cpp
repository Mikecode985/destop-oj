#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const long long INF = (long long)1e18;
struct Edge { int to; long long w; };
vector<Edge> g[MAXN];
long long dist[MAXN];
int pre[MAXN];
bool done[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s, t;
    cin >> n >> m >> s >> t;
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});          // 道路双向
    }
    for (int i = 1; i <= n; i++) dist[i] = INF;
    dist[s] = 0;
    priority_queue<pair<long long, int>,
                   vector<pair<long long, int>>,
                   greater<pair<long long, int>>> pq;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (done[u]) continue;           // 已经确定过的点不再处理
        done[u] = true;
        for (auto e : g[u]) {
            if (dist[e.to] > d + e.w) {  // 松弛：借道 u 更近
                dist[e.to] = d + e.w;
                pre[e.to] = u;           // 记下从哪来
                pq.push({dist[e.to], e.to});
            }
        }
    }
    if (dist[t] == INF) { cout << -1 << "\n"; return 0; }
    cout << dist[t] << "\n";
    vector<int> path;
    for (int x = t; x != s; x = pre[x]) path.push_back(x);
    path.push_back(s);
    reverse(path.begin(), path.end());
    for (int i = 0; i < (int)path.size(); i++) {
        if (i) cout << " ";
        cout << path[i];
    }
    cout << "\n";
    return 0;
}
