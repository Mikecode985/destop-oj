#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int n, m, a[MAXN], tree[MAXN * 4];

void build(int o, int l, int r) {
    if (l == r) { tree[o] = a[l]; return; }
    int mid = (l + r) / 2;
    build(o * 2, l, mid);
    build(o * 2 + 1, mid + 1, r);
    tree[o] = max(tree[o * 2], tree[o * 2 + 1]);   // pushup：合并左右
}

void modify(int o, int l, int r, int pos, int val) {
    if (l == r) { tree[o] = val; return; }
    int mid = (l + r) / 2;
    if (pos <= mid) modify(o * 2, l, mid, pos, val);
    else modify(o * 2 + 1, mid + 1, r, pos, val);
    tree[o] = max(tree[o * 2], tree[o * 2 + 1]);
}

int query(int o, int l, int r, int ql, int qr) {
    if (ql <= l && r <= qr) return tree[o];        // 整段被覆盖，直接用
    int mid = (l + r) / 2, res = 0;
    if (ql <= mid) res = max(res, query(o * 2, l, mid, ql, qr));
    if (qr > mid) res = max(res, query(o * 2 + 1, mid + 1, r, ql, qr));
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    build(1, 1, n);
    while (m--) {
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 1) modify(1, 1, n, x, y);        // 把第 x 个数改成 y
        else cout << query(1, 1, n, x, y) << "\n"; // 问 [x, y] 的最大值
    }
    return 0;
}
