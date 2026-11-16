#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W;
    cin >> n >> W;
    vector<vector<long long>> dp(W + 1, vector<long long>(2, 0));
    for (int g = 0; g < n; g++) {
        int k;
        cin >> k;
        for (int j = 0; j <= W; j++) dp[j][1] = dp[j][0];
        for (int t = 0; t < k; t++) {
            int w, v;
            cin >> w >> v;
            for (int j = W; j >= w; j--)
                dp[j][1] = max(dp[j][1], dp[j - w][0] + v);
        }
        for (int j = 0; j <= W; j++) dp[j][0] = dp[j][1];
    }
    long long ans = 0;
    for (int j = 0; j <= W; j++) ans = max(ans, dp[j][0]);
    cout << ans << "\n";
    return 0;
}
