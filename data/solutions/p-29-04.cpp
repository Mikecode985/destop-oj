#include <bits/stdc++.h>
using namespace std;
long long pw(long long a, long long b, long long m) {
    long long r = 1 % m;
    a %= m;
    while (b > 0) {
        if (b & 1) r = (__int128)r * a % m;
        a = (__int128)a * a % m;
        b >>= 1;
    }
    return r;
}
int main() {
    long long a, b, m;
    cin >> a >> b >> m;
    cout << pw(a, b, m) << "\n" << pw(a, m - 2, m) << "\n";
    return 0;
}
