# -*- coding: utf-8 -*-
"""第 19～20 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-19-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        deg[u]++;
        deg[v]++;
    }
    int best = 1;
    for (int i = 1; i <= n; i++) {
        cout << deg[i] << "\n";
        if (deg[i] > deg[best]) best = i;
    }
    cout << best << "\n";
    return 0;
}
'''

SOL["p-19-02"] = r'''#include <bits/stdc++.h>
using namespace std;
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
    for (int i = 1; i <= n; i++) par[i] = i;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a == b) { cout << "Yes\n"; return 0; }
        par[a] = b;
    }
    cout << "No\n";
    return 0;
}
'''

SOL["p-19-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> col(n + 1, -1);
    for (int s = 1; s <= n; s++) {
        if (col[s] != -1) continue;
        col[s] = 0;
        queue<int> q;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : g[u]) {
                if (col[v] == -1) { col[v] = col[u] ^ 1; q.push(v); }
                else if (col[v] == col[u]) { cout << "No\n"; return 0; }
            }
        }
    }
    cout << "Yes\n";
    int c0 = 0, c1 = 0;
    for (int i = 1; i <= n; i++) {
        cout << col[i] << "\n";
        if (col[i] == 0) c0++; else c1++;
    }
    cout << c0 << " " << c1 << "\n";
    return 0;
}
'''

SOL["p-19-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> d(n + 1, -1);
    queue<int> q;
    d[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u])
            if (d[v] == -1) { d[v] = d[u] + 1; q.push(v); }
    }
    for (int i = 1; i <= n; i++) cout << d[i] << (i == n ? '\n' : ' ');
    return 0;
}
'''

SOL["p-19-06"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-20-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    d[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        pair<long long, int> u = pq.top();
        pq.pop();
        if (u.first != d[u.second]) continue;
        for (auto &e : g[u.second]) {
            long long nd = u.first + e.second;
            if (nd < d[e.first]) {
                d[e.first] = nd;
                pq.push({nd, e.first});
            }
        }
    }
    cout << (d[n] >= INF ? -1 : d[n]) << "\n";
    return 0;
}
'''

SOL["p-20-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    vector<int> pre(n + 1, 0);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    d[1] = 0;
    pq.push({0, 1});
    while (!pq.empty()) {
        pair<long long, int> u = pq.top();
        pq.pop();
        if (u.first != d[u.second]) continue;
        for (auto &e : g[u.second]) {
            long long nd = u.first + e.second;
            if (nd < d[e.first]) {
                d[e.first] = nd;
                pre[e.first] = u.second;
                pq.push({nd, e.first});
            }
        }
    }
    if (d[n] >= INF) { cout << -1 << "\n"; return 0; }
    cout << d[n] << "\n";
    vector<int> path;
    for (int x = n; x; x = pre[x]) {
        path.push_back(x);
        if (x == 1) break;
    }
    reverse(path.begin(), path.end());
    for (size_t i = 0; i < path.size(); i++) cout << path[i] << (i + 1 == path.size() ? '\n' : ' ');
    return 0;
}
'''

SOL["p-20-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<pair<pair<int, int>, long long>> edges;
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        edges.push_back({{u, v}, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    d[1] = 0;
    bool neg = false;
    for (int round = 0; round < n; round++) {
        bool changed = false;
        for (auto &e : edges) {
            int u = e.first.first, v = e.first.second;
            long long w = e.second;
            if (d[u] >= INF) continue;
            if (d[u] + w < d[v]) {
                d[v] = d[u] + w;
                changed = true;
                if (round == n - 1) neg = true;
            }
        }
        if (!changed) break;
    }
    cout << (neg ? "Yes" : "No") << "\n";
    return 0;
}
'''

SOL["p-20-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, int>>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }
    const int INF = 1e9;
    vector<int> d(n + 1, INF);
    deque<int> dq;
    d[1] = 0;
    dq.push_back(1);
    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        for (auto &e : g[u]) {
            int v = e.first, w = e.second;
            if (d[u] + w < d[v]) {
                d[v] = d[u] + w;
                if (w == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    cout << (d[n] >= INF ? -1 : d[n]) << "\n";
    return 0;
}
'''

SOL["p-20-05"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    vector<long long> cnt(n + 1, 0);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    d[1] = 0;
    cnt[1] = 1;
    pq.push({0, 1});
    while (!pq.empty()) {
        pair<long long, int> u = pq.top();
        pq.pop();
        if (u.first != d[u.second]) continue;
        for (auto &e : g[u.second]) {
            long long nd = u.first + e.second;
            if (nd < d[e.first]) {
                d[e.first] = nd;
                cnt[e.first] = cnt[u.second];
                pq.push({nd, e.first});
            } else if (nd == d[e.first]) {
                cnt[e.first] = (cnt[e.first] + cnt[u.second]) % MOD;
            }
        }
    }
    cout << (d[n] >= INF ? 0 : cnt[n] % MOD) << "\n";
    return 0;
}
'''
