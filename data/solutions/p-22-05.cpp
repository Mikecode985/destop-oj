#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> par(n + 1, 0), dep(n + 1, 0), sz(n + 1, 1), order;
    vector<int> st{1};
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        order.push_back(u);
        for (int v : g[u])
            if (v != par[u]) { par[v] = u; dep[v] = dep[u] + 1; st.push_back(v); }
    }
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        if (par[u]) sz[par[u]] += sz[u];
    }
    int centroid = 1;
    int bestMax = n;
    for (int u = 1; u <= n; u++) {
        int mx = n - sz[u];
        for (int v : g[u])
            if (v != par[u]) mx = max(mx, sz[v]);
        if (mx < bestMax || (mx == bestMax && u < centroid)) { bestMax = mx; centroid = u; }
    }
    cout << centroid << "\n";
    vector<long long> sum(n + 1, 0);
    long long base = 0;
    for (int i = 1; i <= n; i++) base += dep[i];
    sum[1] = base;
    for (int u : order) {
        for (int v : g[u])
            if (v != par[u]) sum[v] = sum[u] + n - 2LL * sz[v];
    }
    for (int i = 1; i <= n; i++) cout << sum[i] << "\n";
    return 0;
}
