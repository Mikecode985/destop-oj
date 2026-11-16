#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    vector<int> par(n + 1, 0), order;
    vector<int> st{1};
    par[1] = -1;
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        order.push_back(u);
        for (auto &e : g[u])
            if (e.first != par[u]) { par[e.first] = u; st.push_back(e.first); }
    }
    vector<long long> down1(n + 1, 0), down2(n + 1, 0);
    long long ans = 0;
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        for (auto &e : g[u]) {
            int v = e.first;
            if (v == par[u]) continue;
            long long d = down1[v] + e.second;
            if (d > down1[u]) { down2[u] = down1[u]; down1[u] = d; }
            else if (d > down2[u]) down2[u] = d;
        }
        ans = max(ans, down1[u] + down2[u]);
    }
    cout << ans << "\n";
    return 0;
}
