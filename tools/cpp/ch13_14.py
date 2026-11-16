# -*- coding: utf-8 -*-
"""第 13～14 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-13-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
bool col[12], d1[24], d2[24];
int board[12];
bool dfs(int r) {
    if (r == n) return true;
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r + c] || d2[r - c + n]) continue;
        col[c] = d1[r + c] = d2[r - c + n] = true;
        board[r] = c;
        if (dfs(r + 1)) return true;
        col[c] = d1[r + c] = d2[r - c + n] = false;
    }
    return false;
}
int main() {
    cin >> n;
    if (!dfs(0)) { cout << "No\n"; return 0; }
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) cout << (board[r] == c ? 'Q' : '.');
        cout << "\n";
    }
    return 0;
}
'''

SOL["p-13-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
string cur;
void dfs(int open, int close) {
    if ((int)cur.size() == 2 * n) {
        cout << cur << "\n";
        return;
    }
    if (open < n) {
        cur.push_back('(');
        dfs(open + 1, close);
        cur.pop_back();
    }
    if (close < open) {
        cur.push_back(')');
        dfs(open, close + 1);
        cur.pop_back();
    }
}
int main() {
    cin >> n;
    dfs(0, 0);
    return 0;
}
'''

SOL["p-13-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
vector<int> a, cur;
void dfs(int start) {
    cout << "{";
    for (size_t i = 0; i < cur.size(); i++) cout << (i ? "," : "") << cur[i];
    cout << "}\n";
    for (int i = start; i < n; i++) {
        if (i > start && a[i] == a[i - 1]) continue;
        cur.push_back(a[i]);
        dfs(i + 1);
        cur.pop_back();
    }
}
int main() {
    cin >> n;
    a.resize(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    dfs(0);
    return 0;
}
'''

SOL["p-13-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, m, sx, sy, ex, ey;
vector<string> g;
bool vis[10][10];
long long cnt = 0;
int dx[4] = {-1, 1, 0, 0}, dy[4] = {0, 0, -1, 1};
void dfs(int x, int y) {
    if (x == ex && y == ey) { cnt++; return; }
    for (int k = 0; k < 4; k++) {
        int nx = x + dx[k], ny = y + dy[k];
        if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
        if (g[nx][ny] == '#' || vis[nx][ny]) continue;
        vis[nx][ny] = true;
        dfs(nx, ny);
        vis[nx][ny] = false;
    }
}
int main() {
    cin >> n >> m;
    g.resize(n);
    for (auto &s : g) cin >> s;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] == 'S') { sx = i; sy = j; }
            if (g[i][j] == 'E') { ex = i; ey = j; }
        }
    vis[sx][sy] = true;
    dfs(sx, sy);
    cout << cnt << "\n";
    return 0;
}
'''

SOL["p-13-05"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
long long W, best = 0;
struct Item { long long w, v; double r; } it[25];
bool cmp(const Item &a, const Item &b) { return a.r > b.r; }
void dfs(int i, long long cw, long long cv) {
    best = max(best, cv);
    if (i == n) return;
    if (cw + it[i].w <= W) dfs(i + 1, cw + it[i].w, cv + it[i].v);
    dfs(i + 1, cw, cv);
}
int main() {
    cin >> n >> W;
    for (int i = 0; i < n; i++) {
        cin >> it[i].w >> it[i].v;
        it[i].r = (double)it[i].v / it[i].w;
    }
    sort(it, it + n, cmp);
    dfs(0, 0, 0);
    cout << best << "\n";
    return 0;
}
'''

SOL["p-14-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string tok;
    vector<long long> st;
    while (cin >> tok) {
        if (tok == "+" || tok == "-" || tok == "*" || tok == "/") {
            long long b = st.back(); st.pop_back();
            long long a = st.back(); st.pop_back();
            if (tok == "+") st.push_back(a + b);
            else if (tok == "-") st.push_back(a - b);
            else if (tok == "*") st.push_back(a * b);
            else st.push_back(a / b);
        } else {
            st.push_back(stoll(tok));
        }
    }
    cout << st.back() << "\n";
    return 0;
}
'''

SOL["p-14-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    int d = 0, best = 0;
    for (char c : s) {
        if (c == '(') d++;
        else d--;
        best = max(best, d);
    }
    cout << best << "\n";
    return 0;
}
'''

SOL["p-14-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> h(n);
    for (auto &x : h) cin >> x;
    h.push_back(0);
    vector<int> st;
    long long ans = 0;
    for (int i = 0; i <= n; i++) {
        while (!st.empty() && h[st.back()] >= h[i]) {
            long long ht = h[st.back()];
            st.pop_back();
            int left = st.empty() ? -1 : st.back();
            ans = max(ans, ht * (i - left - 1));
        }
        st.push_back(i);
    }
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-14-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    deque<int> q;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        while (!q.empty() && a[q.back()] >= a[i]) q.pop_back();
        q.push_back(i);
        while (q.front() <= i - k) q.pop_front();
        if (i >= k - 1) cout << a[q.front()] << (i == n - 1 ? '\n' : ' ');
    }
    return 0;
}
'''
