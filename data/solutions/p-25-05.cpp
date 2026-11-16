#include <bits/stdc++.h>
using namespace std;
long long f[205][205], pre[205];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(2 * n + 1);
    for (int i = 1; i <= n; i++) { cin >> a[i]; a[i + n] = a[i]; }
    for (int i = 1; i <= 2 * n; i++) pre[i] = pre[i - 1] + a[i];
    for (int len = 2; len <= n; len++)
        for (int i = 1; i + len - 1 <= 2 * n; i++) {
            int j = i + len - 1;
            f[i][j] = (long long)4e18;
            for (int k = i; k < j; k++)
                f[i][j] = min(f[i][j], f[i][k] + f[k + 1][j]);
            f[i][j] += pre[j] - pre[i - 1];
        }
    long long ans = (long long)4e18;
    for (int i = 1; i <= n; i++) ans = min(ans, f[i][i + n - 1]);
    cout << ans << "\n";
    return 0;
}
