#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 2;
    if (MODE == 0) {
        int n; cin >> n;
        vector<pair<int, string>> v;
        for (int i = 0; i < n; i++) { string s; int x; cin >> s >> x; v.push_back({x, s}); }
        sort(v.begin(), v.end());
        for (auto &p : v) cout << p.second << " " << p.first << "\n";
    } else if (MODE == 1) {
        int n; cin >> n;
        vector<pair<int, string>> v;
        for (int i = 0; i < n; i++) { string s; int x; cin >> s >> x; v.push_back({-x, s}); }
        sort(v.begin(), v.end());
        for (int i = 0; i < min(3, n); i++) cout << v[i].second << " " << -v[i].first << "\n";
    } else if (MODE == 2) {
        int n; cin >> n; vector<int> a(n);
        for (int &x : a) cin >> x;
        sort(a.begin(), a.end());
        cout << a[(n - 1) / 2] << "\n";
    } else if (MODE == 3) {
        int n, k; cin >> n >> k; vector<int> a(n);
        for (int &x : a) cin >> x;
        sort(a.begin(), a.end());
        cout << a[k - 1] << "\n";
    } else {
        int t, n; cin >> t >> n;
        string bests; int bestd = INT_MAX; int bestv = 0;
        for (int i = 0; i < n; i++) {
            string s; int x; cin >> s >> x;
            int d = abs(x - t);
            if (d < bestd || (d == bestd && s < bests)) { bestd = d; bests = s; bestv = x; }
        }
        cout << bests << " " << bestd << "\n";
    }
    return 0;
}
