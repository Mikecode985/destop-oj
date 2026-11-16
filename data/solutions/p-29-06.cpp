#include <bits/stdc++.h>
using namespace std;
long long exgcd(long long a, long long b, long long &x, long long &y) {
    if (!b) { x = 1; y = 0; return a; }
    long long d = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return d;
}
int main() {
    int k;
    cin >> k;
    vector<long long> a(k), m(k);
    long long M = 1;
    for (int i = 0; i < k; i++) {
        cin >> a[i] >> m[i];
        M *= m[i];
    }
    long long ans = 0;
    for (int i = 0; i < k; i++) {
        long long Mi = M / m[i], x, y;
        exgcd(Mi, m[i], x, y);
        x = (x % m[i] + m[i]) % m[i];
        ans = (ans + (__int128)a[i] * Mi % M * x) % M;
    }
    cout << ans % M << "\n";
    return 0;
}
