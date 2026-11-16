#include <bits/stdc++.h>
using namespace std;
long long dp[505][505];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, B, T;
    cin >> n >> B >> T;
    for (int i = 0; i < n; i++) {
        int c, t, v;
        cin >> c >> t >> v;
        for (int a = B; a >= c; a--)
            for (int b = T; b >= t; b--)
                dp[a][b] = max(dp[a][b], dp[a - c][b - t] + v);
    }
    cout << dp[B][T] << "\n";
    return 0;
}
