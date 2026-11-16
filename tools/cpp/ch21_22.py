# -*- coding: utf-8 -*-
"""第 21～22 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-21-01"] = r'''#include <bits/stdc++.h>
using namespace std;
struct Edge { int u, v; long long w; };
int par[100005];
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
    for (auto &x : e) cin >> x.u >> x.v >> x.w;
    sort(e.begin(), e.end(), [](const Edge &a, const Edge &b) { return a.w < b.w; });
    for (int i = 1; i <= n; i++) par[i] = i;
    long long total = 0;
    int used = 0;
    for (auto &x : e) {
        int a = find(x.u), b = find(x.v);
        if (a == b) continue;
        par[a] = b;
        total += x.w;
        if (++used == n - 1) break;
    }
    cout << (used == n - 1 ? total : -1) << "\n";
    return 0;
}
'''

SOL["p-21-02"] = r'''#include <bits/stdc++.h>
using namespace std;
long long g[205][205];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) cin >> g[i][j];
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    vector<int> vis(n + 1, 0);
    d[1] = 0;
    long long total = 0;
    for (int it = 1; it <= n; it++) {
        int u = -1;
        for (int i = 1; i <= n; i++)
            if (!vis[i] && (u == -1 || d[i] < d[u])) u = i;
        if (u == -1 || d[u] >= INF) { cout << -1 << "\n"; return 0; }
        vis[u] = 1;
        total += d[u];
        for (int v = 1; v <= n; v++)
            if (!vis[v] && g[u][v] > 0 && g[u][v] < d[v]) d[v] = g[u][v];
    }
    cout << total << "\n";
    return 0;
}
'''

SOL["p-21-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        indeg[v]++;
    }
    priority_queue<int, vector<int>, greater<int>> q;
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);
    vector<int> order;
    while (!q.empty()) {
        int u = q.top();
        q.pop();
        order.push_back(u);
        for (int v : g[u])
            if (--indeg[v] == 0) q.push(v);
    }
    if ((int)order.size() < n) { cout << "No\n"; return 0; }
    for (int i = 0; i < n; i++) cout << order[i] << (i == n - 1 ? '\n' : ' ');
    return 0;
}
'''

SOL["p-21-05"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        indeg[v]++;
    }
    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);
    vector<long long> dp(n + 1, 0);
    dp[1] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u]) {
            dp[v] = (dp[v] + dp[u]) % MOD;
            if (--indeg[v] == 0) q.push(v);
        }
    }
    cout << dp[n] % MOD << "\n";
    return 0;
}
'''

SOL["p-21-06"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-22-01"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-22-02"] = r'''#include <bits/stdc++.h>
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
    auto far = [&](int s) {
        vector<long long> d(n + 1, -1);
        vector<int> st{s};
        d[s] = 0;
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            for (auto &e : g[u])
                if (d[e.first] == -1) { d[e.first] = d[u] + e.second; st.push_back(e.first); }
        }
        int best = 1;
        for (int i = 2; i <= n; i++)
            if (d[i] > d[best]) best = i;
        return make_pair(best, d[best]);
    };
    if (n == 1) { cout << 0 << "\n"; return 0; }
    int a = far(1).first;
    cout << far(a).second << "\n";
    return 0;
}
'''

SOL["p-22-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    const int LOG = 17;
    vector<vector<int>> up(LOG + 1, vector<int>(n + 1, 0));
    vector<int> dep(n + 1, 0);
    vector<int> st{1};
    up[0][1] = 0;
    vector<int> order;
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
    while (q--) {
        int u, v;
        cin >> u >> v;
        int w = lca(u, v);
        cout << dep[u] + dep[v] - 2 * dep[w] << "\n";
    }
    return 0;
}
'''

SOL["p-22-04"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-22-05"] = r'''#include <bits/stdc++.h>
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
'''
