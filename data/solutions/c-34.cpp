#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> a(n + 1), dp(n + 1, (long long)4e18);
    for (int i = 1; i <= n; i++) cin >> a[i];
    deque<int> dq;
    dp[1] = a[1];
    dq.push_back(1);
    for (int i = 2; i <= n; i++) {
        while (!dq.empty() && dq.front() < i - k) dq.pop_front();
        dp[i] = dp[dq.front()] + a[i];
        while (!dq.empty() && dp[dq.back()] >= dp[i]) dq.pop_back();
        dq.push_back(i);
    }
    cout << dp[n] << "\n";
    return 0;
}
