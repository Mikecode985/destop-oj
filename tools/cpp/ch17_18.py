# -*- coding: utf-8 -*-
"""第 17～18 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-17-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int par[100005], sz[100005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) { par[i] = i; sz[i] = 1; }
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) {
            if (sz[a] < sz[b]) swap(a, b);
            par[b] = a;
            sz[a] += sz[b];
        }
    }
    int cnt = 0, mx = 0;
    for (int i = 1; i <= n; i++)
        if (find(i) == i) { cnt++; mx = max(mx, sz[i]); }
    cout << cnt << " " << mx << "\n";
    return 0;
}
'''

SOL["p-17-02"] = r'''#include <bits/stdc++.h>
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
        if (a != b) par[a] = b;
    }
    int k = 0;
    for (int i = 1; i <= n; i++)
        if (find(i) == i) k++;
    cout << k - 1 << "\n";
    return 0;
}
'''

SOL["p-17-04"] = r'''#include <bits/stdc++.h>
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
    int comp = n;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) { par[a] = b; comp--; }
        cout << comp << "\n";
    }
    return 0;
}
'''

SOL["p-18-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, q;
long long bit[100005];
void add(int i, long long v) {
    for (; i <= n; i += i & -i) bit[i] += v;
}
long long sum(int i) {
    long long s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> q;
    while (q--) {
        int op;
        cin >> op;
        if (op == 1) {
            int x;
            long long k;
            cin >> x >> k;
            add(x, k);
        } else {
            int l, r;
            cin >> l >> r;
            cout << sum(r) - sum(l - 1) << "\n";
        }
    }
    return 0;
}
'''

SOL["p-18-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, q;
long long bit[100005];
void add(int i, long long v) {
    for (; i <= n; i += i & -i) bit[i] += v;
}
long long sum(int i) {
    long long s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> q;
    while (q--) {
        int op;
        cin >> op;
        if (op == 1) {
            int l, r;
            long long k;
            cin >> l >> r >> k;
            add(l, k);
            if (r + 1 <= n) add(r + 1, -k);
        } else {
            int x;
            cin >> x;
            cout << sum(x) << "\n";
        }
    }
    return 0;
}
'''

SOL["p-18-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
long long bit[100005];
void add(int i) {
    for (; i <= n; i += i & -i) bit[i]++;
}
long long sum(int i) {
    long long s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    vector<long long> a(n), b;
    for (auto &x : a) cin >> x;
    b = a;
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    long long ans = 0;
    for (int i = n - 1; i >= 0; i--) {
        int r = lower_bound(b.begin(), b.end(), a[i]) - b.begin() + 1;
        ans += sum(r - 1);
        add(r);
    }
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-18-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, q;
long long a[100005], tr[400005];
void build(int o, int l, int r) {
    if (l == r) { tr[o] = a[l]; return; }
    int mid = (l + r) / 2;
    build(o * 2, l, mid);
    build(o * 2 + 1, mid + 1, r);
    tr[o] = max(tr[o * 2], tr[o * 2 + 1]);
}
void upd(int o, int l, int r, int x, long long v) {
    if (l == r) { tr[o] = v; return; }
    int mid = (l + r) / 2;
    if (x <= mid) upd(o * 2, l, mid, x, v);
    else upd(o * 2 + 1, mid + 1, r, x, v);
    tr[o] = max(tr[o * 2], tr[o * 2 + 1]);
}
long long ask(int o, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return tr[o];
    int mid = (l + r) / 2;
    long long ans = LLONG_MIN;
    if (ql <= mid) ans = max(ans, ask(o * 2, l, mid, ql, qr));
    if (qr > mid) ans = max(ans, ask(o * 2 + 1, mid + 1, r, ql, qr));
    return ans;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];
    build(1, 1, n);
    while (q--) {
        int op;
        cin >> op;
        if (op == 1) {
            int x;
            long long v;
            cin >> x >> v;
            upd(1, 1, n, x, v);
        } else {
            int l, r;
            cin >> l >> r;
            cout << ask(1, 1, n, l, r) << "\n";
        }
    }
    return 0;
}
'''

SOL["p-18-06"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, m, q;
long long bit[505][505];
void add(int x, int y, long long v) {
    for (int i = x; i <= n; i += i & -i)
        for (int j = y; j <= m; j += j & -j) bit[i][j] += v;
}
long long sum(int x, int y) {
    long long s = 0;
    for (int i = x; i > 0; i -= i & -i)
        for (int j = y; j > 0; j -= j & -j) s += bit[i][j];
    return s;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m >> q;
    while (q--) {
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 1) {
            long long v;
            cin >> v;
            add(x, y, v);
        } else {
            cout << sum(x, y) << "\n";
        }
    }
    return 0;
}
'''
