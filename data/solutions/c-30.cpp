#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> c(n);
    for (auto &x : c) cin >> x;
    vector<int> dp(m + 1, INT_MAX / 2);
    dp[0] = 0;
    for (int j = 1; j <= m; j++)
        for (int x : c)
            if (j >= x) dp[j] = min(dp[j], dp[j - x] + 1);
    cout << (dp[m] >= INT_MAX / 2 ? -1 : dp[m]) << "\n";
    return 0;
}
