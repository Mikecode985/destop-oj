#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long m;
    cin >> n >> m;
    vector<long long> h(n);
    long long hi = 0, total = 0;
    for (auto &x : h) {
        cin >> x;
        hi = max(hi, x);
        total += x;
    }
    if (total < m) { cout << 0 << "\n"; return 0; }
    long long lo = 0, ans = 0;
    while (lo <= hi) {
        long long mid = (lo + hi) / 2, wood = 0;
        for (auto x : h)
            if (x > mid) wood += x - mid;
        if (wood >= m) { ans = mid; lo = mid + 1; }
        else hi = mid - 1;
    }
    cout << ans << "\n";
    return 0;
}
