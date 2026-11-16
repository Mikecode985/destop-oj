#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> par(n + 1, 0), credit(n + 1, 0), sz(n + 1, 0);
    vector<vector<int>> ch(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> par[i] >> credit[i];
        ch[par[i]].push_back(i);
    }
    const long long NEG = -(long long)4e18;
    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, NEG));
    vector<int> order{0};
    for (size_t t = 0; t < order.size(); t++)
        for (int v : ch[order[t]]) order.push_back(v);
    for (int idx = (int)order.size() - 1; idx >= 0; idx--) {
        int u = order[idx];
        dp[u][0] = 0;
        if (u != 0) {
            if (m >= 1) dp[u][1] = credit[u];
            sz[u] = 1;
        }
        for (int v : ch[u]) {
            vector<long long> ndp(m + 1, NEG);
            for (int i = 0; i <= min(sz[u], m); i++) {
                if (dp[u][i] == NEG) continue;
                for (int j = 0; j <= min(sz[v], m - i); j++) {
                    if (dp[v][j] == NEG) continue;
                    ndp[i + j] = max(ndp[i + j], dp[u][i] + dp[v][j]);
                }
            }
            dp[u] = ndp;
            sz[u] = min(m, sz[u] + sz[v]);
        }
    }
    cout << dp[0][m] << "\n";
    return 0;
}
