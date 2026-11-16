#include <bits/stdc++.h>
using namespace std;

const int MAXN = 505;
int a[MAXN][MAXN];         // 三角形里的数
int dp[MAXN][MAXN];        // dp[i][j]：从 (i,j) 走到底能拿到的最大和

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= i; j++)
            cin >> a[i][j];

    // 边界：最后一行的 dp 就是它自己
    for (int j = 1; j <= n; j++) dp[n][j] = a[n][j];

    // 从倒数第二行往上推：下一步只能到下面或右下方
    for (int i = n - 1; i >= 1; i--)
        for (int j = 1; j <= i; j++)
            dp[i][j] = a[i][j] + max(dp[i + 1][j], dp[i + 1][j + 1]);

    cout << dp[1][1] << "\n";     // 顶端那一格就是答案
    return 0;
}
