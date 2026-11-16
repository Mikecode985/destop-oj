#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000005;
const long long MOD = 1000000007;
long long fac[MAXN];      // fac[i] = i! mod MOD
long long invfac[MAXN];   // invfac[i] = (i!)^(-1) mod MOD

long long qpow(long long a, long long n) {
    long long res = 1;
    a %= MOD;
    while (n > 0) {
        if (n & 1) res = res * a % MOD;
        a = a * a % MOD;
        n >>= 1;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    fac[0] = 1;
    for (int i = 1; i <= n; i++) fac[i] = fac[i - 1] * i % MOD;

    invfac[n] = qpow(fac[n], MOD - 2);          // 费马小定理求逆元
    for (int i = n; i >= 1; i--) invfac[i - 1] = invfac[i] * i % MOD;

    while (q--) {
        int a, b;
        cin >> a >> b;
        long long ans = fac[a] * invfac[b] % MOD * invfac[a - b] % MOD;
        cout << ans << "\n";
    }
    return 0;
}
