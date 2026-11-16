#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    const int LOG = 17;
    vector<vector<int>> up(LOG + 1, vector<int>(n + 1, 0));
    vector<int> dep(n + 1, 0), order;
    vector<int> st{1};
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        order.push_back(u);
        for (int v : g[u])
            if (v != up[0][u]) { up[0][v] = u; dep[v] = dep[u] + 1; st.push_back(v); }
    }
    for (int k = 1; k <= LOG; k++)
        for (int v = 1; v <= n; v++) up[k][v] = up[k - 1][up[k - 1][v]];
    auto lca = [&](int u, int v) {
        if (dep[u] < dep[v]) swap(u, v);
        int diff = dep[u] - dep[v];
        for (int k = 0; k <= LOG; k++)
            if (diff >> k & 1) u = up[k][u];
        if (u == v) return u;
        for (int k = LOG; k >= 0; k--)
            if (up[k][u] != up[k][v]) { u = up[k][u]; v = up[k][v]; }
        return up[0][u];
    };
    vector<long long> diff(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        int w = lca(u, v);
        diff[u]++;
        diff[v]++;
        diff[w] -= 2;
    }
    vector<long long> sum = diff;
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        if (up[0][u]) sum[up[0][u]] += sum[u];
    }
    for (int i = 2; i <= n; i++) cout << sum[i] << "\n";
    return 0;
}
