#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 1;
    int n, W, K = 0; cin >> n >> W;
    if (MODE == 1 || MODE == 4) cin >> K;
    vector<int> w(n), v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    if (MODE == 0) {
        vector<long long> dp(W + 1, 0);
        for (int i = 0; i < n; i++)
            for (int x = W; x >= w[i]; x--) dp[x] = max(dp[x], dp[x - w[i]] + v[i]);
        cout << *max_element(dp.begin(), dp.end()) << "\n";
    } else if (MODE == 1) {
        vector<vector<long long>> dp(K + 1, vector<long long>(W + 1, -1));
        dp[0][0] = 0;
        for (int i = 0; i < n; i++)
            for (int k = K - 1; k >= 0; k--)
                for (int x = 0; x + w[i] <= W; x++)
                    if (dp[k][x] >= 0) dp[k + 1][x + w[i]] = max(dp[k + 1][x + w[i]], dp[k][x] + v[i]);
        cout << max(0LL, *max_element(dp[K].begin(), dp[K].end())) << "\n";
    } else if (MODE == 2) {
        sort(w.begin(), w.end());
        long long s = 0; int cnt = 0;
        for (int x : w) if (s + x <= W) { s += x; cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 3) {
        long long cnt = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int s = 0;
            for (int i = 0; i < n; i++) if (mask >> i & 1) s += w[i];
            if (s <= W) cnt++;
        }
        cout << cnt << "\n";
    } else {
        vector<vector<long long>> dp(K + 1, vector<long long>(W + 1, 0));
        for (int i = 0; i < n; i++)
            for (int k = K - 1; k >= 0; k--)
                for (int x = W; x >= w[i]; x--)
                    dp[k + 1][x] = max(dp[k + 1][x], dp[k][x - w[i]] + v[i]);
        long long ans = 0;
        for (int k = 0; k <= K; k++) for (int x = 0; x <= W; x++) ans = max(ans, dp[k][x]);
        cout << ans << "\n";
    }
    return 0;
}
