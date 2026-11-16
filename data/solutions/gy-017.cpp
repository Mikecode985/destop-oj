#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 1;
    int n, q; cin >> n >> q;
    vector<long long> a(n + 1), pre(n + 1, 0), px(n + 1, 0);
    for (int i = 1; i <= n; i++) { cin >> a[i]; pre[i] = pre[i - 1] + a[i]; px[i] = px[i - 1] ^ a[i]; }
    while (q--) {
        int l, r; cin >> l >> r;
        if (MODE == 0) cout << pre[r] - pre[l - 1] << "\n";
        else if (MODE == 1) {
            long long mx = a[l];
            for (int i = l; i <= r; i++) mx = max(mx, a[i]);
            cout << mx << "\n";
        } else if (MODE == 2) {
            long long mn = a[l];
            for (int i = l; i <= r; i++) mn = min(mn, a[i]);
            cout << mn << "\n";
        } else if (MODE == 3) {
            cout << (pre[r] - pre[l - 1]) / (r - l + 1) << "\n";
        } else {
            cout << (px[r] ^ px[l - 1]) << "\n";
        }
    }
    return 0;
}
