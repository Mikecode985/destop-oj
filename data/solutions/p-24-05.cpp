#include <bits/stdc++.h>
using namespace std;
long long dp[505][505];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W1, W2;
    cin >> n >> W1 >> W2;
    for (int i = 0; i < n; i++) {
        int w1, w2, v;
        cin >> w1 >> w2 >> v;
        for (int a = W1; a >= w1; a--)
            for (int b = W2; b >= w2; b--)
                dp[a][b] = max(dp[a][b], dp[a - w1][b - w2] + v);
    }
    cout << dp[W1][W2] << "\n";
    return 0;
}
