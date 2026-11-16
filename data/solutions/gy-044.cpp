#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 3;
    int n; cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    if (MODE == 0 || MODE == 1 || MODE == 2) {
        vector<int> b = a;
        if (MODE == 1) for (int &x : b) x = -x;
        vector<int> dp(n, 1);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < i; j++) {
                bool ok = (MODE == 2 ? b[j] <= b[i] : b[j] < b[i]);
                if (ok) dp[i] = max(dp[i], dp[j] + 1);
            }
        cout << *max_element(dp.begin(), dp.end()) << "\n";
    } else if (MODE == 3) {
        int best = 1, cur = 1;
        for (int i = 1; i < n; i++) {
            if (a[i] > a[i - 1]) cur++; else cur = 1;
            best = max(best, cur);
        }
        cout << best << "\n";
    } else {
        int best = 0; long long cnt = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            vector<int> s;
            for (int i = 0; i < n; i++) if (mask >> i & 1) s.push_back(a[i]);
            bool ok = true;
            for (size_t i = 1; i < s.size(); i++) if (s[i - 1] >= s[i]) ok = false;
            if (!ok) continue;
            if ((int)s.size() > best) { best = s.size(); cnt = 1; }
            else if ((int)s.size() == best) cnt++;
        }
        cout << cnt % 1000000007 << "\n";
    }
    return 0;
}
