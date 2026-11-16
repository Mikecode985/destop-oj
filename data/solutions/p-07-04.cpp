#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> w(n);
    long long lo = 0, hi = 0;
    for (auto &x : w) {
        cin >> x;
        lo = max(lo, x);
        hi += x;
    }
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        int cars = 1;
        long long cur = 0;
        bool ok = true;
        for (auto x : w) {
            if (cur + x <= mid) cur += x;
            else { cars++; cur = x; }
            if (cars > k) { ok = false; break; }
        }
        if (ok) hi = mid;
        else lo = mid + 1;
    }
    cout << lo << "\n";
    return 0;
}
