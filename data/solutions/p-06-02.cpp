#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    for (long long mask = 0; mask < (1LL << n); mask++) {
        long long s = 0;
        for (int i = 0; i < n; i++)
            if (mask >> i & 1) s += a[i];
        if (s == S) { cout << "YES\n"; return 0; }
    }
    cout << "NO\n";
    return 0;
}
