#include <bits/stdc++.h>
using namespace std;

// gcd(a, b) = gcd(b, a % b)，b 为 0 时答案是 a
long long gcd(long long a, long long b) {
    if (b == 0) return a;          // 终止条件
    return gcd(b, a % b);          // 递推关系
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long a, b;
    cin >> a >> b;
    cout << gcd(a, b) << "\n";
    return 0;
}
