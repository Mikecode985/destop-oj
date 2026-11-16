#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    unsigned long long xr = 0;
    long long cnt = 0;
    while (n--) {
        unsigned long long x;
        cin >> x;
        xr ^= x;
        cnt += __builtin_popcountll(x);
    }
    cout << xr << "\n" << cnt << "\n";
    return 0;
}
