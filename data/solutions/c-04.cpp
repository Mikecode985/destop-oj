#include <bits/stdc++.h>
using namespace std;
int main() {
    long long n;
    cin >> n;
    const long long MOD = 1000000007LL;
    long long a = n, b = n + 1;
    if (a % 2 == 0) a /= 2; else b /= 2;
    cout << (long long)((__int128)(a % MOD) * (b % MOD) % MOD) << "\n";
    return 0;
}
