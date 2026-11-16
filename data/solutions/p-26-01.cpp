#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> par(n + 1, 0), order;
    vector<int> st{1};
    par[1] = -1;
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        order.push_back(u);
        for (int v : g[u])
            if (v != par[u]) { par[v] = u; st.push_back(v); }
    }
    vector<long long> dp0(n + 1, 0), dp1(n + 1, 0);
    for (int i = n - 1; i >= 0; i--) {
        int u = order[i];
        dp1[u] = a[u];
        for (int v : g[u])
            if (v != par[u]) {
                dp1[u] += dp0[v];
                dp0[u] += max(dp0[v], dp1[v]);
            }
    }
    cout << dp1[1] << "\n";
    return 0;
}
