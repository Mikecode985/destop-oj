#include <bits/stdc++.h>
using namespace std;
long long d[16][16];
long long dp[1 << 15][15];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    if (n == 1) { cout << 0 << "\n"; return 0; }
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> d[i][j];
    const long long INF = (long long)4e18;
    for (int mask = 0; mask < (1 << n); mask++)
        for (int i = 0; i < n; i++) dp[mask][i] = INF;
    dp[1][0] = 0;
    for (int mask = 1; mask < (1 << n); mask++)
        for (int i = 0; i < n; i++) {
            if (dp[mask][i] == INF) continue;
            for (int j = 0; j < n; j++) {
                if (mask >> j & 1) continue;
                int nm = mask | (1 << j);
                if (dp[mask][i] + d[i][j] < dp[nm][j]) dp[nm][j] = dp[mask][i] + d[i][j];
            }
        }
    long long ans = INF;
    for (int i = 1; i < n; i++)
        ans = min(ans, dp[(1 << n) - 1][i] + d[i][0]);
    cout << ans << "\n";
    return 0;
}
