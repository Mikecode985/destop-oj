#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
struct Mat { long long a[2][2]; };
Mat mul(const Mat &x, const Mat &y) {
    Mat z{};
    for (int i = 0; i < 2; i++)
        for (int k = 0; k < 2; k++) {
            if (!x.a[i][k]) continue;
            for (int j = 0; j < 2; j++)
                z.a[i][j] = (z.a[i][j] + (__int128)x.a[i][k] * y.a[k][j]) % MOD;
        }
    return z;
}
int main() {
    long long n;
    cin >> n;
    if (n == 0) { cout << 0 << "\n"; return 0; }
    Mat r{{{1, 0}, {0, 1}}}, b{{{1, 1}, {1, 0}}};
    long long e = n - 1;
    while (e > 0) {
        if (e & 1) r = mul(r, b);
        b = mul(b, b);
        e >>= 1;
    }
    // [F(n), F(n-1)] = b^(n-1) * [F(1), F(0)]
    cout << r.a[0][0] % MOD << "\n";
    return 0;
}
