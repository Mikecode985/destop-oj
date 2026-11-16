#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000005;
const int MOD = 1000000007;
long long dp[MAXN];       // dp[i]：走到第 i 级的方案数
long long pre[MAXN];      // pre[i]：dp[0] + dp[1] + ... + dp[i]

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    dp[0] = 1;            // 站在第 0 级：不动也是一种方案
    pre[0] = 1;
    for (int i = 1; i <= n; i++) {
        int l = i - k;    // 上一步最早从第 l 级迈上来
        long long sum = pre[i - 1];
        if (l - 1 >= 0) {
            sum = (sum - pre[l - 1] + MOD) % MOD;   // 区间和 = 两个前缀和相减
        }
        dp[i] = sum;
        pre[i] = (pre[i - 1] + dp[i]) % MOD;
    }
    cout << dp[n] << "\n";
    return 0;
}
