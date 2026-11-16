#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 3;
    int n, W; cin >> n >> W;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    if (MODE == 0) {
        vector<long long> dp(W + 1, 0);
        for (int i = 0; i < n; i++)
            for (int x = w[i]; x <= W; x++) dp[x] = max(dp[x], dp[x - w[i]] + v[i]);
        cout << *max_element(dp.begin(), dp.end()) << "\n";
    } else if (MODE == 1) {
        vector<int> dp(W + 1, 1e9); dp[0] = 0;
        for (int x = 1; x <= W; x++)
            for (int i = 0; i < n; i++)
                if (x >= w[i]) dp[x] = min(dp[x], dp[x - w[i]] + 1);
        cout << (dp[W] >= 1e9 ? -1 : dp[W]) << "\n";
    } else if (MODE == 2) {
        vector<long long> dp(W + 1, 0); dp[0] = 1;
        for (int x = 1; x <= W; x++)
            for (int i = 0; i < n; i++)
                if (x >= w[i]) dp[x] += dp[x - w[i]];
        cout << dp[W] << "\n";
    } else if (MODE == 3) {
        cout << W / *min_element(w.begin(), w.end()) << "\n";
    } else {
        vector<bool> dp(W + 1, false); dp[0] = true;
        for (int x = 1; x <= W; x++)
            for (int i = 0; i < n; i++)
                if (x >= w[i] && dp[x - w[i]]) dp[x] = true;
        cout << (dp[W] ? "YES" : "NO") << "\n";
    }
    return 0;
}
