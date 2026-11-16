#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long pw(long long a, long long n) {
    if (n == 0) return 1;
    long long t = pw(a, n / 2);
    t = t * t % MOD;
    if (n % 2) t = t * (a % MOD) % MOD;
    return t;
}
int main() {
    long long a, n;
    cin >> a >> n;
    cout << pw(a, n) << "\n";
    return 0;
}
