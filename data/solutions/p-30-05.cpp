#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long D[100005];
int main() {
    int n;
    cin >> n;
    D[0] = 1;
    if (n >= 1) D[1] = 0;
    for (int i = 2; i <= n; i++) D[i] = (i - 1) * ((D[i - 1] + D[i - 2]) % MOD) % MOD;
    cout << D[n] % MOD << "\n";
    return 0;
}
