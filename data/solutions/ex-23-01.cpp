#include <bits/stdc++.h>
using namespace std;

const int MAXN = 85;
long long memo[MAXN];          // memo[i] = -1 表示这个状态还没算过

// 记忆化搜索：从答案往回问，算过的记下来
long long climbMemo(int n) {
    if (n <= 1) return 1;                  // 0 级和 1 级都只有 1 种走法
    if (memo[n] != -1) return memo[n];     // 翻本子
    return memo[n] = climbMemo(n - 1) + climbMemo(n - 2);   // 算完先记账
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 0; i <= n; i++) memo[i] = -1;    // 初始化：全部“没算过”

    long long byMemo = climbMemo(n);

    vector<long long> dp(n + 2, 0);               // 递推：从边界往前推
    dp[0] = 1;
    dp[1] = 1;
    for (int i = 2; i <= n; i++) dp[i] = dp[i - 1] + dp[i - 2];

    cout << byMemo << "\n" << dp[n] << "\n";      // 两种写法必须给出同一个数
    return 0;
}
