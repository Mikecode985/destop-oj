#include <bits/stdc++.h>
using namespace std;

const int MAXN = 5005;
int a[MAXN];
int dp[MAXN];        // dp[i]：以 a[i] 结尾的最长上升子序列长度

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];

    int ans = 0;
    for (int i = 1; i <= n; i++) {
        dp[i] = 1;                            // 谁都接不上时，至少自己一个
        for (int j = 1; j < i; j++)
            if (a[j] < a[i])                  // 严格小于才能接在后面
                dp[i] = max(dp[i], dp[j] + 1);
        ans = max(ans, dp[i]);                // 边算边更新全局答案
    }
    cout << ans << "\n";
    return 0;
}
