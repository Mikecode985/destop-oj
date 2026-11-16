#include <bits/stdc++.h>
using namespace std;

const int MAXN = 305;
const int INF = 0x3f3f3f3f;
int a[MAXN];
int pre[MAXN];              // 前缀和：pre[i] = a[1] + ... + a[i]
int dp[MAXN][MAXN];         // dp[l][r]：把 [l,r] 合成一堆的最小代价

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        pre[i] = pre[i - 1] + a[i];
    }

    for (int len = 2; len <= n; len++)               // 第一层：区间长度
        for (int l = 1; l + len - 1 <= n; l++) {     // 第二层：左端点
            int r = l + len - 1;
            dp[l][r] = INF;
            for (int k = l; k < r; k++)              // 第三层：断点
                dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r]);
            dp[l][r] += pre[r] - pre[l - 1];         // 加上最后合并这一段的代价
        }

    cout << dp[1][n] << "\n";
    return 0;
}
