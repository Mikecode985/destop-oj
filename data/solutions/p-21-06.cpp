#include <bits/stdc++.h>
using namespace std;
struct Edge { int u, v; long long w; int idx; };
int par[1005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<Edge> e(m);
    for (int i = 0; i < m; i++) {
        cin >> e[i].u >> e[i].v >> e[i].w;
        e[i].idx = i;
    }
    sort(e.begin(), e.end(), [](const Edge &a, const Edge &b) {
        if (a.w != b.w) return a.w < b.w;
        if (a.u != b.u) return a.u < b.u;
        if (a.v != b.v) return a.v < b.v;
        return a.idx < b.idx;
    });
    for (int i = 1; i <= n; i++) par[i] = i;
    vector<vector<pair<int, long long>>> tree(n + 1);
    vector<char> inTree(m, 0);
    long long total = 0;
    int used = 0;
    for (int i = 0; i < m; i++) {
        Edge &x = e[i];
        int a = find(x.u), b = find(x.v);
        if (a == b) continue;
        par[a] = b;
        total += x.w;
        used++;
        inTree[i] = 1;
        tree[x.u].push_back({x.v, x.w});
        tree[x.v].push_back({x.u, x.w});
    }
    if (used != n - 1) { cout << -1 << "\n"; return 0; }

    long long ans = -1;
    for (int i = 0; i < m; i++) {
        if (inTree[i]) continue;
        Edge &x = e[i];
        // BFS 找树上 u-v 路径上的最大边
        vector<int> preNode(n + 1, -1);
        vector<long long> preW(n + 1, 0);
        preNode[x.u] = 0;
        vector<int> st{x.u};
        while (!st.empty()) {
            int cur = st.back();
            st.pop_back();
            if (cur == x.v) break;
            for (auto &y : tree[cur])
                if (preNode[y.first] == -1) {
                    preNode[y.first] = cur;
                    preW[y.first] = y.second;
                    st.push_back(y.first);
                }
        }
        long long mx = 0;
        for (int cur = x.v; cur != x.u; cur = preNode[cur]) mx = max(mx, preW[cur]);
        long long cand = total + x.w - mx;
        if (ans == -1 || cand < ans) ans = cand;
    }
    cout << (ans == -1 ? -1 : ans) << "\n";
    return 0;
}
