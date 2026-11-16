#include <bits/stdc++.h>
using namespace std;

const int MAXN = 15;
const int MAXM = 12;
const int MOD = 100000000;
int field[MAXN];              // field[i] 的第 j 位为 1 表示第 i 行第 j 列能种
int dp[1 << MAXM];            // dp[s]：当前行种成状态 s 的方案数
int ndp[1 << MAXM];           // 下一行

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++)
        for (int j = 0; j < m; j++) {
            int x;
            cin >> x;
            if (x) field[i] |= 1 << j;        // 能种的列记成 1
        }

    int total = 1 << m;
    dp[0] = 1;                                  // 第 0 行“什么都没种”算 1 种
    for (int i = 1; i <= n; i++) {
        for (int s = 0; s < total; s++) ndp[s] = 0;
        for (int s = 0; s < total; s++) {
            if (s & (s << 1)) continue;                 // 行内不能左右相邻
            if ((s & ~field[i]) != 0) continue;         // 不能种在不能种的地方
            for (int p = 0; p < total; p++)
                if ((s & p) == 0)                       // 上下不能同时种
                    ndp[s] = (ndp[s] + dp[p]) % MOD;
        }
        for (int s = 0; s < total; s++) dp[s] = ndp[s];
    }

    int ans = 0;
    for (int s = 0; s < total; s++) ans = (ans + dp[s]) % MOD;
    cout << ans << "\n";
    return 0;
}
