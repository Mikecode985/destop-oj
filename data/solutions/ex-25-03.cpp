#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1005;
int dp[MAXN][MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    cin >> s >> t;
    s = " " + s;                       // 前面补一个空格，变成 1-indexed
    t = " " + t;
    int n = (int)s.size() - 1;
    int m = (int)t.size() - 1;

    // 边界：一边是空串时，只能全删或者全插入
    for (int i = 0; i <= n; i++) dp[i][0] = i;
    for (int j = 0; j <= m; j++) dp[0][j] = j;

    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) {
            if (s[i] == t[j]) {
                dp[i][j] = dp[i - 1][j - 1];            // 这一位相同，不用动
            } else {
                dp[i][j] = 1 + min({dp[i - 1][j - 1],   // 替换
                                    dp[i - 1][j],       // 删除
                                    dp[i][j - 1]});     // 插入
            }
        }

    cout << dp[n][m] << "\n";
    return 0;
}
