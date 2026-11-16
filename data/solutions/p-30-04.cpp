#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long pw(long long a, long long b) {
    long long r = 1;
    a %= MOD;
    while (b) {
        if (b & 1) r = (__int128)r * a % MOD;
        a = (__int128)a * a % MOD;
        b >>= 1;
    }
    return r;
}
int main() {
    int n;
    cin >> n;
    if (n == 0) { cout << 1 << "\n"; return 0; }
    long long f = 1;
    for (int i = 1; i <= 2 * n; i++) f = (__int128)f * i % MOD;
    long long g = 1;
    for (int i = 1; i <= n; i++) g = (__int128)g * i % MOD;
    long long h = 1;
    for (int i = 1; i <= n + 1; i++) h = (__int128)h * i % MOD;
    long long g2 = (__int128)g * g % MOD;
    long long den = g2 * (n + 1) % MOD;
    long long ans = (long long)((__int128)f * pw(den, MOD - 2) % MOD);
    cout << ans << "\n";
    return 0;
}
