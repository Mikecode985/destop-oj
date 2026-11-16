#include <bits/stdc++.h>
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
