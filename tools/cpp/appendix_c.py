# -*- coding: utf-8 -*-
"""附录 C 40 道入门题的 C++ 参考答案"""

SOL = {}

SOL["c-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long sum = 0, mx = -1;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        sum += x;
        if (x > mx) { mx = x; pos = i; }
    }
    cout << sum << "\n" << pos << "\n";
    return 0;
}
'''

SOL["c-02"] = r'''#include <bits/stdc++.h>
using namespace std;
struct Item { string name; long long price; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Item> v(n);
    for (auto &it : v) cin >> it.name >> it.price;
    sort(v.begin(), v.end(), [](const Item &a, const Item &b) {
        if (a.price != b.price) return a.price < b.price;
        return a.name < b.name;
    });
    for (auto &it : v) cout << it.name << " " << it.price << "\n";
    return 0;
}
'''

SOL["c-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<pair<string, int>> rec;
    for (int i = 0; i < n; i++) {
        int line;
        string st;
        cin >> line >> st;
        rec.push_back({st, line});
    }
    sort(rec.begin(), rec.end());
    while (m--) {
        string st;
        int line;
        cin >> st >> line;
        auto it = lower_bound(rec.begin(), rec.end(), make_pair(st, line));
        if (it != rec.end() && it->first == st && it->second == line) cout << "Yes\n";
        else cout << "No\n";
    }
    return 0;
}
'''

SOL["c-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    long long n;
    cin >> n;
    const long long MOD = 1000000007LL;
    long long a = n, b = n + 1;
    if (a % 2 == 0) a /= 2; else b /= 2;
    cout << (long long)((__int128)(a % MOD) * (b % MOD) % MOD) << "\n";
    return 0;
}
'''

SOL["c-05"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    long long x, sum = 0;
    int days = 0;
    for (int i = 0; i < 7; i++) {
        cin >> x;
        if (x != -1) { days++; sum += x; }
    }
    cout << days << "\n" << sum << "\n" << (days ? sum / days : 0) << "\n";
    return 0;
}
'''

SOL["c-06"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int s;
    cin >> s;
    int price;
    if (s <= 4) price = 2;
    else if (s <= 9) price = 3;
    else if (s <= 15) price = 4;
    else {
        int extra = (s - 15 + 4) / 5;
        price = 4 + extra;
        if (price > 8) price = 8;
    }
    cout << price << "\n";
    return 0;
}
'''

SOL["c-07"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end(), greater<int>());
    long long sum = 0;
    for (int i = 0; i < min(n, k); i++) sum += a[i];
    cout << sum << "\n";
    return 0;
}
'''

SOL["c-08"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> p(n);
    for (auto &x : p) cin >> x;
    while (m--) {
        int x;
        cin >> x;
        auto it = upper_bound(p.begin(), p.end(), x);
        cout << (it == p.end() ? -1 : *it) << "\n";
    }
    return 0;
}
'''

SOL["c-09"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    vector<long long> L(n);
    for (auto &x : L) cin >> x;
    long long lo = 1, hi = 1000000000LL, ans = 0;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        long long cnt = 0;
        for (long long x : L) cnt += mid ? x / mid : 0;
        if (cnt >= k) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    cout << ans << "\n";
    return 0;
}
'''

SOL["c-10"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<long long, long long>> a(n);
    for (auto &x : a) cin >> x.first >> x.second;
    sort(a.begin(), a.end(), [](const pair<long long, long long> &x, const pair<long long, long long> &y) {
        return x.second < y.second;
    });
    long long last = -1;
    int cnt = 0;
    for (auto &x : a)
        if (x.first >= last) { cnt++; last = x.second; }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["c-11"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> f(max(3, n + 1));
    f[1] = 1; f[2] = 2;
    for (int i = 3; i <= n; i++) f[i] = f[i - 1] + f[i - 2];
    cout << f[n] << "\n";
    return 0;
}
'''

SOL["c-12"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    vector<long long> v = a;
    sort(v.begin(), v.end());
    v.erase(unique(v.begin(), v.end()), v.end());
    int sz = v.size();
    vector<int> bit(sz + 1, 0);
    auto add = [&](int i) { for (; i <= sz; i += i & -i) bit[i]++; };
    auto qry = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += bit[i];
        return s;
    };
    long long ans = 0;
    for (int i = n - 1; i >= 0; i--) {
        int p = lower_bound(v.begin(), v.end(), a[i]) - v.begin() + 1;
        ans += qry(p - 1);
        add(p);
    }
    cout << ans << "\n";
    return 0;
}
'''

SOL["c-13"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    int best = 0;
    vector<int> dx{1, -1, 0, 0}, dy{0, 0, 1, -1};
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] != '1') continue;
            int cnt = 0;
            deque<pair<int, int>> q;
            q.push_back({i, j});
            g[i][j] = '0';
            while (!q.empty()) {
                auto [x, y] = q.front();
                q.pop_front();
                cnt++;
                for (int d = 0; d < 4; d++) {
                    int nx = x + dx[d], ny = y + dy[d];
                    if (nx < 0 || ny < 0 || nx >= n || ny >= m || g[nx][ny] != '1') continue;
                    g[nx][ny] = '0';
                    q.push_back({nx, ny});
                }
            }
            best = max(best, cnt);
        }
    cout << best << "\n";
    return 0;
}
'''

SOL["c-14"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<int>> g(n + 1);
    while (m--) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    vector<int> d(n + 1, -1);
    deque<int> q;
    d[s] = 0;
    q.push_back(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        for (int v : g[u])
            if (d[v] == -1) { d[v] = d[u] + 1; q.push_back(v); }
    }
    cout << d[t] << "\n";
    return 0;
}
'''

SOL["c-15"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    vector<vector<int>> d(n, vector<int>(m, -1));
    deque<pair<int, int>> q;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (g[i][j] == '2') { d[i][j] = 0; q.push_back({i, j}); }
    vector<int> dx{1, -1, 0, 0}, dy{0, 0, 1, -1};
    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop_front();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || ny < 0 || nx >= n || ny >= m) continue;
            if (g[nx][ny] == '1' || d[nx][ny] != -1) continue;
            d[nx][ny] = d[x][y] + 1;
            q.push_back({nx, ny});
        }
    }
    int ans = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (g[i][j] == '0') {
                if (d[i][j] == -1) { cout << -1 << "\n"; return 0; }
                ans = max(ans, d[i][j]);
            }
    cout << ans << "\n";
    return 0;
}
'''

SOL["c-16"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, cnt;
bool col[20], d1[40], d2[40];
void dfs(int r) {
    if (r == n) { cnt++; return; }
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r + c] || d2[r - c + n]) continue;
        col[c] = d1[r + c] = d2[r - c + n] = true;
        dfs(r + 1);
        col[c] = d1[r + c] = d2[r - c + n] = false;
    }
}
int main() {
    cin >> n;
    dfs(0);
    cout << cnt << "\n";
    return 0;
}
'''

SOL["c-17"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    int bal = 0;
    for (char c : s) {
        if (c == '(') bal++;
        else { bal--; if (bal < 0) { cout << "No\n"; return 0; } }
    }
    cout << (bal == 0 ? "Yes\n" : "No\n");
    return 0;
}
'''

SOL["c-18"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> h(n);
    for (auto &x : h) cin >> x;
    vector<int> ans(n, 0);
    vector<int> st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && h[st.back()] <= h[i]) st.pop_back();
        if (!st.empty()) ans[i] = st.back() + 1;
        st.push_back(i);
    }
    for (int i = 0; i < n; i++) cout << ans[i] << (i + 1 == n ? '\n' : ' ');
    return 0;
}
'''

SOL["c-19"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    unordered_set<int> st;
    st.reserve(n * 2);
    int x, rep = -1;
    for (int i = 0; i < n; i++) {
        cin >> x;
        if (!st.insert(x).second) rep = x;
    }
    cout << rep << "\n";
    return 0;
}
'''

SOL["c-20"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    nth_element(a.begin(), a.begin() + (k - 1), a.end(), greater<int>());
    cout << a[k - 1] << "\n";
    return 0;
}
'''

SOL["c-21"] = r'''#include <bits/stdc++.h>
using namespace std;
int fa[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++) fa[i] = i;
    while (m--) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) fa[a] = b;
    }
    while (q--) {
        int u, v;
        cin >> u >> v;
        cout << (find(u) == find(v) ? "Yes\n" : "No\n");
    }
    return 0;
}
'''

SOL["c-22"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, q;
long long bit[200005];
void add(int i, long long v) { for (; i <= n; i += i & -i) bit[i] += v; }
long long sum(int i) { long long s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; }
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> q;
    while (q--) {
        int op;
        cin >> op;
        if (op == 1) {
            int x;
            long long v;
            cin >> x >> v;
            add(x, v);
        } else {
            int l, r;
            cin >> l >> r;
            cout << sum(r) - sum(l - 1) << "\n";
        }
    }
    return 0;
}
'''

SOL["c-23"] = r'''#include <bits/stdc++.h>
using namespace std;
int fa[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) fa[i] = i;
    int cnt = n;
    while (m--) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) { fa[a] = b; cnt--; }
    }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["c-24"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<pair<int, long long>>> g(n + 1);
    while (m--) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> pq;
    d[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != d[u]) continue;
        for (auto [v, w] : g[u])
            if (d[v] > du + w) { d[v] = du + w; pq.push({d[v], v}); }
    }
    cout << (d[t] == INF ? -1 : d[t]) << "\n";
    return 0;
}
'''

SOL["c-25"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<pair<int, long long>>> g(n + 1);
    while (m--) {
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
    d[s] = 0;
    cnt[s] = 1;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != d[u]) continue;
        for (auto [v, w] : g[u]) {
            if (d[v] > du + w) {
                d[v] = du + w;
                cnt[v] = cnt[u];
                pq.push({d[v], v});
            } else if (d[v] == du + w) {
                cnt[v] = (cnt[v] + cnt[u]) % MOD;
            }
        }
    }
    cout << (d[t] == INF ? 0 : cnt[t] % MOD) << "\n";
    return 0;
}
'''

SOL["c-26"] = r'''#include <bits/stdc++.h>
using namespace std;
int fa[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
struct E { int u, v; long long w; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<E> e(m);
    for (auto &x : e) cin >> x.u >> x.v >> x.w;
    sort(e.begin(), e.end(), [](const E &a, const E &b) { return a.w < b.w; });
    for (int i = 1; i <= n; i++) fa[i] = i;
    long long tot = 0;
    int used = 0;
    for (auto &x : e) {
        int a = find(x.u), b = find(x.v);
        if (a == b) continue;
        fa[a] = b;
        tot += x.w;
        if (++used == n - 1) break;
    }
    cout << (used == n - 1 ? tot : -1) << "\n";
    return 0;
}
'''

SOL["c-27"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 1; i < n; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    auto far = [&](int s) {
        vector<long long> d(n + 1, -1);
        deque<int> q;
        d[s] = 0;
        q.push_back(s);
        int best = s;
        while (!q.empty()) {
            int u = q.front();
            q.pop_front();
            if (d[u] > d[best]) best = u;
            for (auto [v, w] : g[u])
                if (d[v] == -1) { d[v] = d[u] + w; q.push_back(v); }
        }
        return make_pair(best, d[best]);
    };
    int a = far(1).first;
    cout << far(a).second << "\n";
    return 0;
}
'''

SOL["c-28"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<long long>> a(n, vector<long long>(n + 1, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j <= i; j++) cin >> a[i][j];
    vector<long long> dp(n + 1, 0);
    for (int j = 0; j < n; j++) dp[j] = a[n - 1][j];
    for (int i = n - 2; i >= 0; i--)
        for (int j = 0; j <= i; j++)
            dp[j] = a[i][j] + max(dp[j], dp[j + 1]);
    cout << dp[0] << "\n";
    return 0;
}
'''

SOL["c-29"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W;
    cin >> n >> W;
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        int w, v;
        cin >> w >> v;
        for (int j = W; j >= w; j--) dp[j] = max(dp[j], dp[j - w] + v);
    }
    cout << dp[W] << "\n";
    return 0;
}
'''

SOL["c-30"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> c(n);
    for (auto &x : c) cin >> x;
    vector<int> dp(m + 1, INT_MAX / 2);
    dp[0] = 0;
    for (int j = 1; j <= m; j++)
        for (int x : c)
            if (j >= x) dp[j] = min(dp[j], dp[j - x] + 1);
    cout << (dp[m] >= INT_MAX / 2 ? -1 : dp[m]) << "\n";
    return 0;
}
'''

SOL["c-31"] = r'''#include <bits/stdc++.h>
using namespace std;
long long dp[305][305], pre[305];
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
            dp[i][j] = LLONG_MAX / 4;
            long long w = pre[j] - pre[i - 1];
            for (int k = i; k < j; k++) dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + w);
        }
    cout << dp[1][n] << "\n";
    return 0;
}
'''

SOL["c-32"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> tail;
    while (n--) {
        int x;
        cin >> x;
        auto it = upper_bound(tail.begin(), tail.end(), x);
        if (it == tail.end()) tail.push_back(x);
        else *it = x;
    }
    cout << tail.size() << "\n";
    return 0;
}
'''

SOL["c-33"] = r'''#include <bits/stdc++.h>
using namespace std;
const int MOD = 1000000007;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> mask(m, 0);
    for (int i = 0; i < m; i++) {
        int k;
        cin >> k;
        while (k--) {
            int p;
            cin >> p;
            mask[i] |= 1 << (p - 1);
        }
    }
    vector<int> dp(1 << m, 0);
    dp[0] = 1;
    for (int post = 0; post < n; post++) {
        vector<int> ndp(1 << m, 0);
        for (int s = 0; s < (1 << m); s++) {
            if (!dp[s]) continue;
            for (int v = 0; v < m; v++) {
                if ((s >> v) & 1) continue;
                if (!((mask[v] >> post) & 1)) continue;
                ndp[s | (1 << v)] = (ndp[s | (1 << v)] + dp[s]) % MOD;
            }
        }
        dp.swap(ndp);
    }
    long long ans = 0;
    for (int s = 0; s < (1 << m); s++) ans = (ans + dp[s]) % MOD;
    cout << ans << "\n";
    return 0;
}
'''

SOL["c-34"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> a(n + 1), dp(n + 1, (long long)4e18);
    for (int i = 1; i <= n; i++) cin >> a[i];
    deque<int> dq;
    dp[1] = a[1];
    dq.push_back(1);
    for (int i = 2; i <= n; i++) {
        while (!dq.empty() && dq.front() < i - k) dq.pop_front();
        dp[i] = dp[dq.front()] + a[i];
        while (!dq.empty() && dp[dq.back()] >= dp[i]) dq.pop_back();
        dq.push_back(i);
    }
    cout << dp[n] << "\n";
    return 0;
}
'''

SOL["c-35"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, p;
    cin >> s >> p;
    int m = p.size();
    vector<int> pi(m, 0);
    for (int i = 1; i < m; i++) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j]) j = pi[j - 1];
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    int j = 0;
    long long cnt = 0;
    for (char c : s) {
        while (j > 0 && c != p[j]) j = pi[j - 1];
        if (c == p[j]) j++;
        if (j == m) { cnt++; j = pi[j - 1]; }
    }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["c-36"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    long long a, b, p;
    cin >> a >> b >> p;
    long long r = 1 % p;
    a %= p;
    while (b) {
        if (b & 1) r = (__int128)r * a % p;
        a = (__int128)a * a % p;
        b >>= 1;
    }
    cout << r << "\n";
    return 0;
}
'''

SOL["c-37"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<char> comp(n + 1, 0);
    int cnt = 0;
    for (int i = 2; i <= n; i++) {
        if (comp[i]) continue;
        cnt++;
        for (long long j = (long long)i * i; j <= n; j += i) comp[j] = 1;
    }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["c-38"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long pw(long long a, long long b) {
    long long r = 1;
    a %= MOD;
    while (b) {
        if (b & 1) r = (__int128)r * a % MOD;
        a = (__int128)a * a % MOD;
        b >>= 1;
    }
    return r;
}
int main() {
    int n, m;
    cin >> n >> m;
    long long f = 1, g = 1, h = 1;
    for (int i = 1; i <= n; i++) f = (__int128)f * i % MOD;
    for (int i = 1; i <= m; i++) g = (__int128)g * i % MOD;
    for (int i = 1; i <= n - m; i++) h = (__int128)h * i % MOD;
    cout << (long long)((__int128)f * pw((__int128)g * h % MOD, MOD - 2) % MOD) << "\n";
    return 0;
}
'''

SOL["c-39"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    unsigned long long xr = 0;
    long long cnt = 0;
    while (n--) {
        unsigned long long x;
        cin >> x;
        xr ^= x;
        cnt += __builtin_popcountll(x);
    }
    cout << xr << "\n" << cnt << "\n";
    return 0;
}
'''

SOL["c-40"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string a, b;
    cin >> a >> b;
    if (a.size() < b.size()) swap(a, b);
    string r;
    int i = a.size() - 1, j = b.size() - 1, carry = 0;
    while (i >= 0) {
        int d = (a[i] - '0') + (j >= 0 ? b[j] - '0' : 0) + carry;
        r.push_back('0' + d % 10);
        carry = d / 10;
        i--;
        j--;
    }
    if (carry) r.push_back('0' + carry);
    reverse(r.begin(), r.end());
    cout << r << "\n";
    return 0;
}
'''
