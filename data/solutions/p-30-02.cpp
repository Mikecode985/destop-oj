#include <bits/stdc++.h>
using namespace std;
long long pw(long long a, long long b, long long m) {
    long long r = 1 % m;
    a %= m;
    while (b) {
        if (b & 1) r = (__int128)r * a % m;
        a = (__int128)a * a % m;
        b >>= 1;
    }
    return r;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    long long n, m, p;
    while (q--) {
        cin >> n >> m >> p;
        if (m > n) { cout << 0 << "\n"; continue; }
        long long cur = 1, fm = 1, fnm = 1;
        for (long long i = 1; i <= n; i++) {
            cur = (__int128)cur * i % p;
            if (i == m) fm = cur;
            if (i == n - m) fnm = cur;
        }
        long long ans = (__int128)cur * pw((__int128)fm * fnm % p, p - 2, p) % p;
        cout << ans << "\n";
    }
    return 0;
}
