# -*- coding: utf-8 -*-
"""第 11～12 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-11-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    vector<vector<int>> vis(n, vector<int>(m, 0));
    int dx[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
    int dy[8] = {-1, 0, 1, -1, 1, -1, 0, 1};
    int comp = 0;
    vector<pair<int, int>> st;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] != '1' || vis[i][j]) continue;
            comp++;
            vis[i][j] = 1;
            st.push_back({i, j});
            while (!st.empty()) {
                pair<int, int> u = st.back();
                st.pop_back();
                for (int d = 0; d < 8; d++) {
                    int x = u.first + dx[d], y = u.second + dy[d];
                    if (x < 0 || x >= n || y < 0 || y >= m) continue;
                    if (g[x][y] == '1' && !vis[x][y]) {
                        vis[x][y] = 1;
                        st.push_back({x, y});
                    }
                }
            }
        }
    cout << comp << "\n";
    return 0;
}
'''

SOL["p-11-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, k;
vector<int> cur;
void dfs(int start) {
    if ((int)cur.size() == k) {
        for (int i = 0; i < k; i++) cout << cur[i] << (i == k - 1 ? '\n' : ' ');
        return;
    }
    for (int v = start; v <= n; v++) {
        if (n - v + 1 < k - (int)cur.size()) break;
        cur.push_back(v);
        dfs(v + 1);
        cur.pop_back();
    }
}
int main() {
    cin >> n >> k;
    dfs(1);
    return 0;
}
'''

SOL["p-11-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, m;
vector<int> adj[25];
int col[25];
bool dfs(int u) {
    if (u == n + 1) return true;
    for (int c = 1; c <= 4; c++) {
        bool ok = true;
        for (int v : adj[u])
            if (col[v] == c) { ok = false; break; }
        if (!ok) continue;
        col[u] = c;
        if (dfs(u + 1)) return true;
        col[u] = 0;
    }
    return false;
}
int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    if (!dfs(1)) { cout << "No\n"; return 0; }
    for (int i = 1; i <= n; i++) cout << col[i] << "\n";
    return 0;
}
'''

SOL["p-11-06"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
bool isp[25];
bool used[10];
int ans[10];
bool found = false;
void dfs(int d, int last) {
    if (d == n) {
        found = true;
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? '\n' : ' ');
        return;
    }
    for (int v = 1; v <= n; v++) {
        if (used[v]) continue;
        if (d > 0 && !isp[last + v]) continue;
        used[v] = true;
        ans[d] = v;
        dfs(d + 1, v);
        used[v] = false;
    }
}
int main() {
    cin >> n;
    for (int i = 2; i <= 2 * n; i++) {
        bool p = true;
        for (int j = 2; j * j <= i; j++)
            if (i % j == 0) { p = false; break; }
        isp[i] = p;
    }
    dfs(0, 0);
    if (!found) cout << "No\n";
    return 0;
}
'''

SOL["p-12-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<int>> g(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u])
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
    }
    cout << dist[t] << "\n";
    return 0;
}
'''

SOL["p-12-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    vector<vector<int>> d(n, vector<int>(m, -1));
    queue<pair<int, int>> q;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (g[i][j] == 'X') { d[i][j] = 0; q.push({i, j}); }
    int dx[4] = {-1, 1, 0, 0}, dy[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        pair<int, int> u = q.front();
        q.pop();
        for (int k = 0; k < 4; k++) {
            int x = u.first + dx[k], y = u.second + dy[k];
            if (x < 0 || x >= n || y < 0 || y >= m) continue;
            if (g[x][y] == '#' || d[x][y] != -1) continue;
            d[x][y] = d[u.first][u.second] + 1;
            q.push({x, y});
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '#') cout << '#';
            else cout << d[i][j];
            cout << (j == m - 1 ? '\n' : ' ');
        }
    }
    return 0;
}
'''

SOL["p-12-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int a[9];
    char c;
    for (int i = 0; i < 9; i++) { cin >> c; a[i] = c - '0'; }
    int inv = 0;
    for (int i = 0; i < 9; i++) {
        if (a[i] == 0) continue;
        for (int j = i + 1; j < 9; j++) {
            if (a[j] == 0) continue;
            if (a[i] > a[j]) inv++;
        }
    }
    cout << (inv % 2 == 0 ? "Yes" : "No") << "\n";
    return 0;
}
'''

SOL["p-12-06"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<string> w(n);
    for (auto &s : w) cin >> s;
    string s, t;
    cin >> s >> t;
    if (s == t) { cout << 0 << "\n"; return 0; }
    int si = -1, ti = -1;
    for (int i = 0; i < n; i++) {
        if (w[i] == s) si = i;
        if (w[i] == t) ti = i;
    }
    if (si < 0 || ti < 0) { cout << -1 << "\n"; return 0; }
    vector<int> d(n, -1);
    queue<int> q;
    d[si] = 0;
    q.push(si);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v = 0; v < n; v++) {
            if (d[v] != -1 || w[v].size() != w[u].size()) continue;
            int diff = 0;
            for (size_t k = 0; k < w[u].size(); k++)
                if (w[u][k] != w[v][k]) diff++;
            if (diff == 1) {
                d[v] = d[u] + 1;
                if (v == ti) { cout << d[v] << "\n"; return 0; }
                q.push(v);
            }
        }
    }
    cout << -1 << "\n";
    return 0;
}
'''
