#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
long long a[MAXN];
long long dp[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];

    long long ans = a[1];          // 初始值取第一个元素，兼容全负数
    dp[1] = a[1];
    for (int i = 2; i <= n; i++) {
        dp[i] = max(a[i], dp[i - 1] + a[i]);   // 接上前面，或从自己重新开始
        ans = max(ans, dp[i]);
    }
    cout << ans << "\n";
    return 0;
}
