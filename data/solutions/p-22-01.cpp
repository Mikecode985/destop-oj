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
    par[1] = -1;
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        order.push_back(u);
        for (int v : g[u])
            if (v != par[u]) { par[v] = u; dep[v] = dep[u] + 1; st.push_back(v); }
    }
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        if (par[u] > 0) sz[par[u]] += sz[u];
    }
    for (int i = 1; i <= n; i++) cout << dep[i] << " " << sz[i] << "\n";
    return 0;
}
