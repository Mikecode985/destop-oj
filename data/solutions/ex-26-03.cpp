#include <bits/stdc++.h>
using namespace std;

const int MAXN = 15;
const int INF = 0x3f3f3f3f;
int d[MAXN][MAXN];
int dp[1 << MAXN][MAXN];      // dp[mask][i]：去过 mask 里的城市，现在停在 i

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) cin >> d[i][j];

    if (n == 1) {                    // 只有一个城市，不用走
        cout << 0 << "\n";
        return 0;
    }

    int full = 1 << n;
    for (int mask = 0; mask < full; mask++)
        for (int i = 0; i < n; i++) dp[mask][i] = INF;
    dp[1][0] = 0;                    // 只去过 0 号城市，停在 0

    for (int mask = 1; mask < full; mask++) {
        for (int i = 0; i < n; i++) {
            if (dp[mask][i] == INF) continue;         // 这个状态到不了
            if (!(mask >> i & 1)) continue;           // i 必须在集合里
            for (int j = 0; j < n; j++) {
                if (mask >> j & 1) continue;          // j 已经去过
                int nm = mask | (1 << j);
                dp[nm][j] = min(dp[nm][j], dp[mask][i] + d[i][j]);
            }
        }
    }

    int ans = INF;
    for (int i = 1; i < n; i++)                       // 最后要回到 0 号城市
        ans = min(ans, dp[full - 1][i] + d[i][0]);
    cout << ans << "\n";
    return 0;
}
