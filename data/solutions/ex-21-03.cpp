#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
const long long NEG = (long long)-1e18;
struct Edge { int to; long long w; };
vector<Edge> g[MAXN];
int indeg[MAXN];
long long dp[MAXN];

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
        indeg[v]++;
    }
    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);
    for (int i = 1; i <= n; i++) dp[i] = NEG;
    dp[1] = 0;                           // 起点到自己是 0
    int seen = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        seen++;
        for (auto e : g[u]) {
            if (dp[u] != NEG)            // 到不了 u，就别用它更新
                dp[e.to] = max(dp[e.to], dp[u] + e.w);
            if (--indeg[e.to] == 0) q.push(e.to);
        }
    }
    if (seen < n || dp[n] == NEG) cout << -1 << "\n";
    else cout << dp[n] << "\n";
    return 0;
}
