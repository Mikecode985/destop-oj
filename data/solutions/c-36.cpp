#include <bits/stdc++.h>
using namespace std;
int main() {
    long long a, b, p;
    cin >> a >> b >> p;
    long long r = 1 % p;
    a %= p;
    while (b) {
        if (b & 1) r = (__int128)r * a % p;
        a = (__int128)a * a % p;
        b >>= 1;
    }
    cout << r << "\n";
    return 0;
}
