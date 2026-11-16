#include <bits/stdc++.h>
using namespace std;
int f[205][205];
int main() {
    string s;
    cin >> s;
    int n = s.size();
    for (int i = 0; i < n; i++) f[i][i] = 1;
    for (int len = 2; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            int best = f[i + 1][j] + 1;
            for (int k = i + 1; k <= j; k++)
                if (s[k] == s[i]) {
                    int v = (k - 1 >= i + 1 ? f[i + 1][k - 1] : 0) + f[k][j];
                    best = min(best, v);
                }
            f[i][j] = best;
        }
    cout << f[0][n - 1] << "\n";
    return 0;
}
