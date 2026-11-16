#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> h(n);
    for (int i = 0; i < n; ++i) cin >> h[i];

    vector<int> inc(n, 1), dec(n, 1);
    for (int i = 1; i < n; ++i) {
        if (h[i - 1] < h[i]) inc[i] = inc[i - 1] + 1;
    }
    for (int i = n - 2; i >= 0; --i) {
        if (h[i] < h[i + 1]) dec[i] = dec[i + 1] + 1;
    }

    int ans = 0;
    for (int i = 0; i + 1 < n; ++i) {
        ans = max(ans, inc[i] + dec[i + 1]);
    }
    cout << ans << '\n';
    return 0;
}
