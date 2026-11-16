#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> w(n);
    for (auto &s : w) cin >> s;
    sort(w.begin(), w.end());
    int q;
    cin >> q;
    while (q--) {
        string t;
        cin >> t;
        auto r = equal_range(w.begin(), w.end(), t);
        cout << r.second - r.first << "\n";
    }
    return 0;
}
