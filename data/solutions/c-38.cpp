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
    int n, m;
    cin >> n >> m;
    long long f = 1, g = 1, h = 1;
    for (int i = 1; i <= n; i++) f = (__int128)f * i % MOD;
    for (int i = 1; i <= m; i++) g = (__int128)g * i % MOD;
    for (int i = 1; i <= n - m; i++) h = (__int128)h * i % MOD;
    cout << (long long)((__int128)f * pw((__int128)g * h % MOD, MOD - 2) % MOD) << "\n";
    return 0;
}
