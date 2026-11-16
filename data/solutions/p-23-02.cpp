#include <bits/stdc++.h>
using namespace std;
long long a[1005][1005], f[1005][1005];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= i; j++) cin >> a[i][j];
    for (int j = 1; j <= n; j++) f[n][j] = a[n][j];
    for (int i = n - 1; i >= 1; i--)
        for (int j = 1; j <= i; j++)
            f[i][j] = a[i][j] + max(f[i + 1][j], f[i + 1][j + 1]);
    cout << f[1][1] << "\n";
    int j = 1;
    for (int i = 1; i <= n; i++) {
        cout << j << (i == n ? '\n' : ' ');
        if (i == n) break;
        if (f[i + 1][j + 1] > f[i + 1][j]) j++;
    }
    return 0;
}
