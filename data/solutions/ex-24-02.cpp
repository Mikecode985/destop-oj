#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
const int MAXW = 1005;
int w[MAXN], v[MAXN];
int dp[MAXW];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    for (int i = 1; i <= n; i++) cin >> w[i] >> v[i];

    for (int i = 1; i <= n; i++)
        for (int j = w[i]; j <= W; j++)          // 正序！同一件可以反复拿
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);

    cout << dp[W] << "\n";
    return 0;
}
