#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, W;
    cin >> n >> W;
    vector<int> c(n);
    for (auto &x : c) cin >> x;
    const int INF = 1e9;
    vector<int> dp(W + 1, INF);
    dp[0] = 0;
    for (int j = 1; j <= W; j++)
        for (int i = 0; i < n; i++)
            if (j >= c[i] && dp[j - c[i]] + 1 < dp[j]) dp[j] = dp[j - c[i]] + 1;
    cout << (dp[W] >= INF ? -1 : dp[W]) << "\n";
    return 0;
}
