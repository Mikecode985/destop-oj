#include <bits/stdc++.h>
using namespace std;

long long gcd(long long a, long long b) {
    return b == 0 ? a : gcd(b, a % b);
}

long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;   // 先除后乘，防止溢出
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n, a, b, c;
    cin >> n >> a >> b >> c;

    long long ans = n / a + n / b + n / c;                    // 三个单集合
    ans -= n / lcm(a, b) + n / lcm(a, c) + n / lcm(b, c);     // 减两两交集
    ans += n / lcm(lcm(a, b), c);                             // 加三集合交集

    cout << ans << "\n";
    return 0;
}
