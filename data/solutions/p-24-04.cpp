#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, W;
    cin >> n >> W;
    const long long NEG = -(long long)4e18;
    vector<long long> dp(W + 1, NEG);
    dp[0] = 0;
    for (int i = 0; i < n; i++) {
        int w, v;
        cin >> w >> v;
        for (int j = W; j >= w; j--)
            if (dp[j - w] > NEG / 2) dp[j] = max(dp[j], dp[j - w] + v);
    }
    cout << (dp[W] <= NEG / 2 ? -1 : dp[W]) << "\n";
    return 0;
}
