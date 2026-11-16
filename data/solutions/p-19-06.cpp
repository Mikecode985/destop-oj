#include <bits/stdc++.h>
using namespace std;
int par[100005];
bool active[100005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, k;
    cin >> n >> m >> k;
    vector<pair<int, int>> edges(m);
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        edges[i] = {u, v};
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> del(k);
    vector<char> dead(n + 1, 0);
    for (int i = 0; i < k; i++) {
        cin >> del[i];
        dead[del[i]] = 1;
    }
    for (int i = 1; i <= n; i++) {
        par[i] = i;
        active[i] = !dead[i];
    }
    int comp = 0;
    for (int i = 1; i <= n; i++) if (active[i]) comp++;
    for (auto &e : edges) {
        int u = e.first, v = e.second;
        if (!active[u] || !active[v]) continue;
        int a = find(u), b = find(v);
        if (a != b) { par[a] = b; comp--; }
    }
    vector<int> ans(k + 1, 0);
    ans[k] = comp;
    for (int i = k - 1; i >= 0; i--) {
        int x = del[i];
        active[x] = true;
        comp++;
        for (int y : g[x]) {
            if (!active[y]) continue;
            int a = find(x), b = find(y);
            if (a != b) { par[a] = b; comp--; }
        }
        ans[i] = comp;
    }
    for (int i = 1; i <= k; i++) cout << ans[i] << "\n";
    return 0;
}
