#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 0;
    int n, m; cin >> n >> m;
    int p = 0;
    if (MODE == 2 || MODE == 4) cin >> p;
    vector<long long> a(n + 1), d(n + 2, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 0; i < m; i++) {
        int l, r, x; cin >> l >> r >> x;
        d[l] += x; d[r + 1] -= x;
    }
    for (int i = 1; i <= n; i++) d[i] += d[i - 1], a[i] += d[i];
    if (MODE == 0) {
        long long mx = a[1], s = 0;
        for (int i = 1; i <= n; i++) { mx = max(mx, a[i]); s += a[i]; }
        cout << mx << " " << s << "\n";
    } else if (MODE == 1) {
        for (int i = 1; i <= n; i++) cout << a[i] << (i == n ? "\n" : " ");
    } else if (MODE == 2) {
        int cnt = 0;
        for (int i = 1; i <= n; i++) if (a[i] >= p) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 3) {
        cout << *min_element(a.begin() + 1, a.end()) << " " << *max_element(a.begin() + 1, a.end()) << "\n";
    } else {
        cout << a[p] << "\n";
    }
    return 0;
}
