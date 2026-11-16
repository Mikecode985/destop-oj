#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<long long>> a(n, vector<long long>(n + 1, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j <= i; j++) cin >> a[i][j];
    vector<long long> dp(n + 1, 0);
    for (int j = 0; j < n; j++) dp[j] = a[n - 1][j];
    for (int i = n - 2; i >= 0; i--)
        for (int j = 0; j <= i; j++)
            dp[j] = a[i][j] + max(dp[j], dp[j + 1]);
    cout << dp[0] << "\n";
    return 0;
}
