#include <bits/stdc++.h>
using namespace std;
long long f[305][305], pre[305];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pre[i] = pre[i - 1] + x;
    }
    for (int len = 2; len <= n; len++)
        for (int i = 1; i + len - 1 <= n; i++) {
            int j = i + len - 1;
            f[i][j] = (long long)4e18;
            for (int k = i; k < j; k++)
                f[i][j] = min(f[i][j], f[i][k] + f[k + 1][j]);
            f[i][j] += pre[j] - pre[i - 1];
        }
    cout << f[1][n] << "\n";
    return 0;
}
