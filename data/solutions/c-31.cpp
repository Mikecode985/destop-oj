#include <bits/stdc++.h>
using namespace std;
long long dp[305][305], pre[305];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pre[i] = pre[i - 1] + x;
    }
    for (int len = 2; len <= n; len++)
        for (int i = 1; i + len - 1 <= n; i++) {
            int j = i + len - 1;
            dp[i][j] = LLONG_MAX / 4;
            long long w = pre[j] - pre[i - 1];
            for (int k = i; k < j; k++) dp[i][j] = min(dp[i][j], dp[i][k] + dp[k + 1][j] + w);
        }
    cout << dp[1][n] << "\n";
    return 0;
}
