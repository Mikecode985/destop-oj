#include <bits/stdc++.h>
using namespace std;

const int MAXN = 2000005;
const long long MOD = 1000000007;
long long fac[MAXN];

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

    int n;
    cin >> n;
    int top = 2 * n;
    fac[0] = 1;
    for (int i = 1; i <= top; i++) fac[i] = fac[i - 1] * i % MOD;

    // Cat(n) = (2n)! / (n! * n!) / (n+1)
    long long ans = fac[top];
    ans = ans * qpow(fac[n], MOD - 2) % MOD;
    ans = ans * qpow(fac[n], MOD - 2) % MOD;
    ans = ans * qpow(n + 1, MOD - 2) % MOD;
    cout << ans << "\n";
    return 0;
}
