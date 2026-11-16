#include <bits/stdc++.h>
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
