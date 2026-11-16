#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN];               // 全局数组，10^5 个 int 约 400KB，放栈上偏大

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];

    // 方案一：每一对都试一遍，O(n^2)
    long long pairs1 = 0, ops1 = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = i + 1; j <= n; j++) {
            ops1++;
            if ((a[i] + a[j]) % 2 == 0) pairs1++;
        }
    }

    // 方案二：只数奇偶，再算组合数，O(n)
    long long even = 0, odd = 0, ops2 = 0;
    for (int i = 1; i <= n; i++) {
        ops2++;
        if (a[i] % 2 == 0) even++;
        else odd++;
    }
    long long pairs2 = even * (even - 1) / 2 + odd * (odd - 1) / 2;

    cout << pairs1 << " " << pairs2 << "\n";
    cout << ops1 << " " << ops2 << "\n";
    return 0;
}
