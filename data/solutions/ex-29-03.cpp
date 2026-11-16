#include <bits/stdc++.h>
using namespace std;

long long exgcd(long long a, long long b, long long &x, long long &y) {
    if (b == 0) { x = 1; y = 0; return a; }
    long long g = exgcd(b, a % b, y, x);   // 递归时 x、y 交换
    y -= a / b * x;
    return g;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long a, b;
    cin >> a >> b;

    long long x, y;
    long long g = exgcd(a, b, x, y);
    if (g != 1) {
        cout << -1 << "\n";
    } else {
        long long ans = (x % b + b) % b;   // 把负解调成正解
        cout << ans << "\n";
    }
    return 0;
}
