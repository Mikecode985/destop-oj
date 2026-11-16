#include <bits/stdc++.h>
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
