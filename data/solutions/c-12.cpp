#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    vector<long long> v = a;
    sort(v.begin(), v.end());
    v.erase(unique(v.begin(), v.end()), v.end());
    int sz = v.size();
    vector<int> bit(sz + 1, 0);
    auto add = [&](int i) { for (; i <= sz; i += i & -i) bit[i]++; };
    auto qry = [&](int i) {
        int s = 0;
        for (; i > 0; i -= i & -i) s += bit[i];
        return s;
    };
    long long ans = 0;
    for (int i = n - 1; i >= 0; i--) {
        int p = lower_bound(v.begin(), v.end(), a[i]) - v.begin() + 1;
        ans += qry(p - 1);
        add(p);
    }
    cout << ans << "\n";
    return 0;
}
