# -*- coding: utf-8 -*-
"""第 7～8 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-07-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    while (q--) {
        int x;
        cin >> x;
        int pos = upper_bound(a.begin(), a.end(), x) - a.begin() + 1;
        cout << pos << "\n";
    }
    return 0;
}
'''

SOL["p-07-03"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-07-04"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-07-05"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    double lo = 1.0, hi = 2.0;
    for (int i = 0; i < 100; i++) {
        double mid = (lo + hi) / 2;
        if (mid * mid * mid - mid - 1 >= 0) hi = mid;
        else lo = mid;
    }
    cout << (long long)((lo + hi) / 2 * 1000000.0) << "\n";
    return 0;
}
'''

SOL["p-08-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    long long n;
    cin >> n;
    long long cnt = 0;
    int c[4] = {10, 5, 2, 1};
    for (int i = 0; i < 4; i++) {
        cnt += n / c[i];
        n %= c[i];
    }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["p-08-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, d;
    cin >> n >> d;
    vector<pair<double, double>> seg;
    for (int i = 0; i < n; i++) {
        int x, y;
        cin >> x >> y;
        if (y > d) { cout << -1 << "\n"; return 0; }
        double half = sqrt((double)d * d - (double)y * y);
        seg.push_back({x + half, x - half});
    }
    sort(seg.begin(), seg.end());
    int cnt = 0;
    double last = -1e18;
    for (auto &s : seg) {
        if (s.second > last) {
            cnt++;
            last = s.first;
        }
    }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["p-08-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    int la = 0, ra = n - 1, lb = 0, rb = n - 1;
    long long ans = 0;
    while (la <= ra) {
        if (a[ra] > b[rb]) { ans += 200; ra--; rb--; }
        else if (a[la] > b[lb]) { ans += 200; la++; lb++; }
        else {
            if (a[la] < b[rb]) ans -= 200;
            la++;
            rb--;
        }
    }
    cout << ans << "\n";
    return 0;
}
'''
