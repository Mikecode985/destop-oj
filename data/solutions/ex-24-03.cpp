#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
const int MAXW = 2005;
const int MAXM = 2005;        // 拆分后最多这么多个“0-1 物品”
int W2[MAXM], V2[MAXM];       // 每一捆的重量和价值
int dp[MAXW];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;

    int m = 0;                          // 拆分后的物品个数
    for (int i = 1; i <= n; i++) {
        int w, v, c;
        cin >> w >> v >> c;
        for (int k = 1; k <= c; k *= 2) {   // 1、2、4、8……
            W2[++m] = k * w;
            V2[m] = k * v;
            c -= k;
        }
        if (c > 0) {                    // 剩下的件数单独打成一捆
            W2[++m] = c * w;
            V2[m] = c * v;
        }
    }

    for (int i = 1; i <= m; i++)
        for (int j = W; j >= W2[i]; j--)          // 拆分后就是 0-1 背包
            dp[j] = max(dp[j], dp[j - W2[i]] + V2[i]);

    cout << dp[W] << "\n";
    return 0;
}
