#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
const int MAXW = 1005;
long long dp[MAXW];         // dp[j]：凑出金额 j 的方案数

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    dp[0] = 1;                      // 凑出 0 元：一枚都不拿，算 1 种
    for (int i = 1; i <= n; i++) {
        int a;
        cin >> a;                   // 第 i 种面额
        for (int j = a; j <= W; j++)        // 正序：每种钱币无限多
            dp[j] += dp[j - a];
    }
    cout << dp[W] << "\n";
    return 0;
}
