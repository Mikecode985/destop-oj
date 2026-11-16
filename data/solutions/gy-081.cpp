#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 0;
    int n; cin >> n;
    int k = 0;
    if (MODE == 0 || MODE == 2 || MODE == 3) cin >> k;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    sort(a.begin(), a.end());
    if (MODE == 0) cout << a[n - k] << "\n";
    else if (MODE == 1) cout << a[(n - 1) / 2] << "\n";
    else if (MODE == 2) { long long s = 0; for (int i = n - k; i < n; i++) s += a[i]; cout << s << "\n"; }
    else if (MODE == 3) {
        vector<int> u;
        for (int i = 0; i < n; i++) if (i == 0 || a[i] != a[i-1]) u.push_back(a[i]);
        cout << u[k - 1] << "\n";
    } else {
        int best = 0, ans = a[0];
        for (int i = 0; i < n; ) {
            int j = i; while (j < n && a[j] == a[i]) j++;
            if (j - i > best) { best = j - i; ans = a[i]; }
            i = j;
        }
        cout << ans << "\n";
    }
    return 0;
}
