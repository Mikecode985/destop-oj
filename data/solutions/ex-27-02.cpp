#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000005;
long long a[MAXN];     // 第 i 站的得分
long long dp[MAXN];    // dp[i]：停在第 i 站时的最大总分

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    for (int i = 1; i <= n; i++) cin >> a[i];

    deque<int> q;              // 存下标，dp 值从队头到队尾递减
    q.push_back(0);            // 第 0 站是起点，得分 0
    for (int i = 1; i <= n; i++) {
        while (!q.empty() && q.front() < i - k) q.pop_front();  // 弹掉过期窗口
        dp[i] = dp[q.front()] + a[i];                           // 队头即窗口最大值
        while (!q.empty() && dp[q.back()] <= dp[i]) q.pop_back(); // 又小又旧的留着没用
        q.push_back(i);
    }
    cout << dp[n] << "\n";
    return 0;
}
