#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    int n;
    cin >> n;
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    long long S = 1;  // S[i] = dp[i-1] + ... + dp[i-8]
    for (int i = 1; i <= n; i++) {
        dp[i] = S % MOD;
        S += dp[i];
        if (i - 8 >= 0) S -= dp[i - 8];
        S %= MOD;
        if (S < 0) S += MOD;
    }
    cout << dp[n] % MOD << "\n";
    return 0;
}
