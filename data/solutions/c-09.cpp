#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long k;
    cin >> n >> k;
    vector<long long> L(n);
    for (auto &x : L) cin >> x;
    long long lo = 1, hi = 1000000000LL, ans = 0;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2;
        long long cnt = 0;
        for (long long x : L) cnt += mid ? x / mid : 0;
        if (cnt >= k) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    cout << ans << "\n";
    return 0;
}
