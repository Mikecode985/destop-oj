#include <bits/stdc++.h>
using namespace std;
const int MOD = 1000000007;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> mask(m, 0);
    for (int i = 0; i < m; i++) {
        int k;
        cin >> k;
        while (k--) {
            int p;
            cin >> p;
            mask[i] |= 1 << (p - 1);
        }
    }
    vector<int> dp(1 << m, 0);
    dp[0] = 1;
    for (int post = 0; post < n; post++) {
        vector<int> ndp(1 << m, 0);
        for (int s = 0; s < (1 << m); s++) {
            if (!dp[s]) continue;
            for (int v = 0; v < m; v++) {
                if ((s >> v) & 1) continue;
                if (!((mask[v] >> post) & 1)) continue;
                ndp[s | (1 << v)] = (ndp[s | (1 << v)] + dp[s]) % MOD;
            }
        }
        dp.swap(ndp);
    }
    long long ans = 0;
    for (int s = 0; s < (1 << m); s++) ans = (ans + dp[s]) % MOD;
    cout << ans << "\n";
    return 0;
}
