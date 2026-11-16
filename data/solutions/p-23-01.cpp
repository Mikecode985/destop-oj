#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    long long f[75];
    f[0] = 1;
    for (int i = 1; i <= n; i++) {
        f[i] = 0;
        for (int k = 1; k <= 3; k++)
            if (i - k >= 0) f[i] += f[i - k];
    }
    cout << f[n] << "\n";
    return 0;
}
