#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> allow(n, 0);
    for (int i = 0; i < n; i++) {
        int k;
        cin >> k;
        for (int j = 0; j < k; j++) {
            int c;
            cin >> c;
            allow[i] |= 1 << (c - 1);
        }
    }
    const int NEG = -1000000000;
    vector<int> dp(1 << m, NEG);
    dp[0] = 0;
    for (int a : allow) {
        vector<int> ndp = dp;
        for (int used = 0; used < (1 << m); used++) {
            if (dp[used] == NEG) continue;
            int fre = a & ~used;
            for (int sub = fre;; sub = (sub - 1) & fre) {
                int v = dp[used] + __builtin_popcount(sub);
                if (v > ndp[used | sub]) ndp[used | sub] = v;
                if (sub == 0) break;
            }
        }
        dp = ndp;
    }
    int ans = 0;
    for (int x : dp) ans = max(ans, x);
    cout << ans << "\n";
    return 0;
}
