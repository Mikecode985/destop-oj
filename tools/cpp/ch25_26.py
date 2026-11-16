# -*- coding: utf-8 -*-
"""第 25～26 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-25-01"] = r'''#include <bits/stdc++.h>
using namespace std;
long long f[305][305], pre[305];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pre[i] = pre[i - 1] + x;
    }
    for (int len = 2; len <= n; len++)
        for (int i = 1; i + len - 1 <= n; i++) {
            int j = i + len - 1;
            f[i][j] = (long long)4e18;
            for (int k = i; k < j; k++)
                f[i][j] = min(f[i][j], f[i][k] + f[k + 1][j]);
            f[i][j] += pre[j] - pre[i - 1];
        }
    cout << f[1][n] << "\n";
    return 0;
}
'''

SOL["p-25-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    int n = s.size(), best = 0;
    for (int c = 0; c < n; c++) {
        for (int l = c, r = c; l >= 0 && r < n && s[l] == s[r]; l--, r++)
            best = max(best, r - l + 1);
        for (int l = c, r = c + 1; l >= 0 && r < n && s[l] == s[r]; l--, r++)
            best = max(best, r - l + 1);
    }
    cout << best << "\n";
    return 0;
}
'''

SOL["p-25-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int f[205][205];
int main() {
    string s;
    cin >> s;
    int n = s.size();
    for (int i = 0; i < n; i++) f[i][i] = 1;
    for (int len = 2; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            int best = f[i + 1][j] + 1;
            for (int k = i + 1; k <= j; k++)
                if (s[k] == s[i]) {
                    int v = (k - 1 >= i + 1 ? f[i + 1][k - 1] : 0) + f[k][j];
                    best = min(best, v);
                }
            f[i][j] = best;
        }
    cout << f[0][n - 1] << "\n";
    return 0;
}
'''

SOL["p-25-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    vector<int> st;
    st.push_back(-1);
    int best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') st.push_back(i);
        else {
            st.pop_back();
            if (st.empty()) st.push_back(i);
            else best = max(best, i - st.back());
        }
    }
    cout << best << "\n";
    return 0;
}
'''

SOL["p-25-05"] = r'''#include <bits/stdc++.h>
using namespace std;
long long f[205][205], pre[205];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(2 * n + 1);
    for (int i = 1; i <= n; i++) { cin >> a[i]; a[i + n] = a[i]; }
    for (int i = 1; i <= 2 * n; i++) pre[i] = pre[i - 1] + a[i];
    for (int len = 2; len <= n; len++)
        for (int i = 1; i + len - 1 <= 2 * n; i++) {
            int j = i + len - 1;
            f[i][j] = (long long)4e18;
            for (int k = i; k < j; k++)
                f[i][j] = min(f[i][j], f[i][k] + f[k + 1][j]);
            f[i][j] += pre[j] - pre[i - 1];
        }
    long long ans = (long long)4e18;
    for (int i = 1; i <= n; i++) ans = min(ans, f[i][i + n - 1]);
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-26-01"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-26-02"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-26-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> par(n + 1, 0), credit(n + 1, 0), sz(n + 1, 0);
    vector<vector<int>> ch(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> par[i] >> credit[i];
        ch[par[i]].push_back(i);
    }
    const long long NEG = -(long long)4e18;
    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, NEG));
    vector<int> order{0};
    for (size_t t = 0; t < order.size(); t++)
        for (int v : ch[order[t]]) order.push_back(v);
    for (int idx = (int)order.size() - 1; idx >= 0; idx--) {
        int u = order[idx];
        dp[u][0] = 0;
        if (u != 0) {
            if (m >= 1) dp[u][1] = credit[u];
            sz[u] = 1;
        }
        for (int v : ch[u]) {
            vector<long long> ndp(m + 1, NEG);
            for (int i = 0; i <= min(sz[u], m); i++) {
                if (dp[u][i] == NEG) continue;
                for (int j = 0; j <= min(sz[v], m - i); j++) {
                    if (dp[v][j] == NEG) continue;
                    ndp[i + j] = max(ndp[i + j], dp[u][i] + dp[v][j]);
                }
            }
            dp[u] = ndp;
            sz[u] = min(m, sz[u] + sz[v]);
        }
    }
    cout << dp[0][m] << "\n";
    return 0;
}
'''

SOL["p-26-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> allow(n, 0);
    for (int i = 0; i < n; i++) {
        int k;
        cin >> k;
        for (int j = 0; j < k; j++) {
            int c;
            cin >> c;
            allow[i] |= 1 << (c - 1);
        }
    }
    const int NEG = -1000000000;
    vector<int> dp(1 << m, NEG);
    dp[0] = 0;
    for (int a : allow) {
        vector<int> ndp = dp;
        for (int used = 0; used < (1 << m); used++) {
            if (dp[used] == NEG) continue;
            int fre = a & ~used;
            for (int sub = fre;; sub = (sub - 1) & fre) {
                int v = dp[used] + __builtin_popcount(sub);
                if (v > ndp[used | sub]) ndp[used | sub] = v;
                if (sub == 0) break;
            }
        }
        dp = ndp;
    }
    int ans = 0;
    for (int x : dp) ans = max(ans, x);
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-26-05"] = r'''#include <bits/stdc++.h>
using namespace std;
long long d[16][16];
long long dp[1 << 15][15];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    if (n == 1) { cout << 0 << "\n"; return 0; }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> d[i][j];
    const long long INF = (long long)4e18;
    for (int mask = 0; mask < (1 << n); mask++)
        for (int i = 0; i < n; i++) dp[mask][i] = INF;
    dp[1][0] = 0;
    for (int mask = 1; mask < (1 << n); mask++)
        for (int i = 0; i < n; i++) {
            if (dp[mask][i] == INF) continue;
            for (int j = 0; j < n; j++) {
                if (mask >> j & 1) continue;
                int nm = mask | (1 << j);
                if (dp[mask][i] + d[i][j] < dp[nm][j]) dp[nm][j] = dp[mask][i] + d[i][j];
            }
        }
    long long ans = INF;
    for (int i = 1; i < n; i++)
        ans = min(ans, dp[(1 << n) - 1][i] + d[i][0]);
    cout << ans << "\n";
    return 0;
}
'''
