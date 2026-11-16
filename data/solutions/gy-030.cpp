#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 4;
    int n; cin >> n;
    vector<pair<int,int>> s(n);
    for (auto &p : s) cin >> p.first >> p.second;
    if (MODE == 0 || MODE == 2) {
        sort(s.begin(), s.end(), [](auto &a, auto &b) { return a.second < b.second; });
        int cnt = 0, last = INT_MIN;
        for (auto &p : s) if (p.first >= last) { cnt++; last = p.second; }
        cout << (MODE == 0 ? cnt : n - cnt) << "\n";
    } else if (MODE == 1) {
        vector<pair<int,int>> ev;
        for (auto &p : s) { ev.push_back({p.first, 1}); ev.push_back({p.second, -1}); }
        sort(ev.begin(), ev.end());
        long long total = 0; int cur = 0, prev = ev[0].first;
        for (auto &e : ev) {
            if (cur > 0) total += e.first - prev;
            cur += e.second; prev = e.first;
        }
        cout << total << "\n";
    } else if (MODE == 3) {
        sort(s.begin(), s.end());
        vector<pair<int,int>> m;
        for (auto &p : s) {
            if (!m.empty() && p.first <= m.back().second) m.back().second = max(m.back().second, p.second);
            else m.push_back(p);
        }
        cout << m.size() << "\n";
        for (auto &p : m) cout << p.first << " " << p.second << "\n";
    } else {
        vector<pair<int,int>> ev;
        for (auto &p : s) { ev.push_back({p.first, 1}); ev.push_back({p.second, -1}); }
        sort(ev.begin(), ev.end());
        int cur = 0, best = 0;
        for (auto &e : ev) { cur += e.second; best = max(best, cur); }
        cout << best << "\n";
    }
    return 0;
}
