#include <bits/stdc++.h>
using namespace std;
long long cnt(long long n, long long d) { return n / d; }
int main() {
    long long n;
    cin >> n;
    long long ans = cnt(n, 2) + cnt(n, 3) + cnt(n, 5)
                  - cnt(n, 6) - cnt(n, 10) - cnt(n, 15)
                  + cnt(n, 30);
    cout << n - ans << "\n";
    return 0;
}
