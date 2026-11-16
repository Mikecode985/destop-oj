#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007;

struct Mat {
    long long a[2][2];
};

Mat mul(const Mat &x, const Mat &y) {
    Mat z{};                        // 全部初始化为 0
    for (int i = 0; i < 2; i++)
        for (int k = 0; k < 2; k++) {
            if (x.a[i][k] == 0) continue;
            for (int j = 0; j < 2; j++)
                z.a[i][j] = (z.a[i][j] + x.a[i][k] * y.a[k][j]) % MOD;
        }
    return z;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    cin >> n;

    Mat base{};                     // 转移矩阵 [[1,1],[1,0]]
    base.a[0][0] = base.a[0][1] = 1;
    base.a[1][0] = 1;

    Mat res{};                      // 单位矩阵
    res.a[0][0] = res.a[1][1] = 1;

    long long e = n - 1;            // M^(n-1) 的左上角就是 F(n)
    while (e > 0) {
        if (e & 1) res = mul(res, base);
        base = mul(base, base);
        e >>= 1;
    }
    cout << res.a[0][0] % MOD << "\n";
    return 0;
}
