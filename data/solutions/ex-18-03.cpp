#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int n, m;
long long a[MAXN], sum[MAXN * 4], lazy[MAXN * 4];

void build(int o, int l, int r) {
    if (l == r) { sum[o] = a[l]; return; }
    int mid = (l + r) / 2;
    build(o * 2, l, mid);
    build(o * 2 + 1, mid + 1, r);
    sum[o] = sum[o * 2] + sum[o * 2 + 1];
}

void pushdown(int o, int l, int r) {               // 把欠孩子的账还掉
    if (lazy[o] == 0) return;
    int mid = (l + r) / 2;
    sum[o * 2] += lazy[o] * (mid - l + 1);
    lazy[o * 2] += lazy[o];
    sum[o * 2 + 1] += lazy[o] * (r - mid);
    lazy[o * 2 + 1] += lazy[o];
    lazy[o] = 0;
}

void update(int o, int l, int r, int ql, int qr, long long v) {
    if (ql <= l && r <= qr) {                      // 整段被覆盖，先欠着
        sum[o] += v * (r - l + 1);
        lazy[o] += v;
        return;
    }
    pushdown(o, l, r);
    int mid = (l + r) / 2;
    if (ql <= mid) update(o * 2, l, mid, ql, qr, v);
    if (qr > mid) update(o * 2 + 1, mid + 1, r, ql, qr, v);
    sum[o] = sum[o * 2] + sum[o * 2 + 1];
}

long long query(int o, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return sum[o];
    pushdown(o, l, r);
    int mid = (l + r) / 2;
    long long res = 0;
    if (ql <= mid) res += query(o * 2, l, mid, ql, qr);
    if (qr > mid) res += query(o * 2 + 1, mid + 1, r, ql, qr);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    build(1, 1, n);
    while (m--) {
        int op, l, r;
        cin >> op >> l >> r;
        if (op == 1) {
            long long v; cin >> v;                 // 区间 [l, r] 每个数加 v
            update(1, 1, n, l, r, v);
        } else {
            cout << query(1, 1, n, l, r) << "\n";
        }
    }
    return 0;
}
