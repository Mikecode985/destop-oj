#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int n;
long long k;                 // 最多 10^9 块，用 long long 更稳
int h[MAXN], w[MAXN];

// 边长 x 时，所有巧克力能不能切够 k 块
bool check(int x) {
    long long cnt = 0;
    for (int i = 1; i <= n; i++) {
        cnt += 1LL * (h[i] / x) * (w[i] / x);
        if (cnt >= k) return true;      // 够了就提前结束
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k;
    int maxSide = 0;
    for (int i = 1; i <= n; i++) {
        cin >> h[i] >> w[i];
        if (h[i] > maxSide) maxSide = h[i];
        if (w[i] > maxSide) maxSide = w[i];
    }

    int l = 1, r = maxSide, ans = 0;    // 答案范围 0 到最大边长
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (check(mid)) {
            ans = mid;                  // mid 行，再试试更大的
            l = mid + 1;
        } else {
            r = mid - 1;                // mid 不行，往小找
        }
    }
    cout << ans << "\n";
    return 0;
}
