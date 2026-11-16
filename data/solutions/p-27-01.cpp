#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    int n, m;
    cin >> n >> m;
    vector<long long> f(m + 1, 0);
    f[1] = 1;
    for (int i = 1; i <= n; i++)
        for (int j = 2; j <= m; j++) {
            f[j] += f[j - 1];
            if (f[j] >= MOD) f[j] -= MOD;
        }
    cout << f[m] % MOD << "\n";
    return 0;
}
