#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, s;
    cin >> n >> s;

    const int MAXN = 25;
    int a[MAXN];
    for (int i = 0; i < n; i++) cin >> a[i];

    long long ans = 0;
    // mask 的第 i 个二进制位为 1，表示选第 i 样菜
    for (int mask = 0; mask < (1 << n); mask++) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) sum += a[i];
        }
        if (sum == s) ans++;
    }

    cout << ans << "\n";
    return 0;
}
