#include <bits/stdc++.h>
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
