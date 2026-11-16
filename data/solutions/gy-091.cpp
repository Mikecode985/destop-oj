#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 0;
    if (MODE == 3) {
        int n; cin >> n;
        vector<vector<int>> t(n);
        for (int i = 0; i < n; i++) { t[i].resize(i + 1); for (int &x : t[i]) cin >> x; }
        vector<int> dp = t[n-1];
        for (int i = n - 2; i >= 0; i--)
            for (int j = 0; j <= i; j++) dp[j] = t[i][j] + min(dp[j], dp[j+1]);
        cout << dp[0] << "\n";
        return 0;
    }
    int n, m; cin >> n >> m;
    vector<vector<int>> g(n, vector<int>(m));
    for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) cin >> g[i][j];
    if (MODE == 0) {
        vector<vector<long long>> dp(n, vector<long long>(m, 1e18)); dp[0][0] = g[0][0];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] = min(dp[i][j], dp[i-1][j] + g[i][j]);
            if (j) dp[i][j] = min(dp[i][j], dp[i][j-1] + g[i][j]);
        }
        cout << dp[n-1][m-1] << "\n";
    } else if (MODE == 1) {
        vector<vector<long long>> dp(n, vector<long long>(m, 0)); dp[0][0] = 1;
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] += dp[i-1][j];
            if (j) dp[i][j] += dp[i][j-1];
            dp[i][j] %= 998244353;
        }
        cout << dp[n-1][m-1] << "\n";
    } else if (MODE == 2) {
        vector<vector<long long>> dp(n, vector<long long>(m, -1e18)); dp[0][0] = g[0][0];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] = max(dp[i][j], dp[i-1][j] + g[i][j]);
            if (j) dp[i][j] = max(dp[i][j], dp[i][j-1] + g[i][j]);
        }
        cout << dp[n-1][m-1] << "\n";
    } else {
        vector<vector<long long>> dp(n, vector<long long>(m, 1e18)); dp[0][0] = g[0][0];
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) {
            if (i) dp[i][j] = min(dp[i][j], max(dp[i-1][j], (long long)g[i][j]));
            if (j) dp[i][j] = min(dp[i][j], max(dp[i][j-1], (long long)g[i][j]));
        }
        cout << dp[n-1][m-1] << "\n";
    }
    return 0;
}
