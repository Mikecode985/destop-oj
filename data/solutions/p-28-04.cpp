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
        string p;
        cin >> p;
        auto it = lower_bound(w.begin(), w.end(), p);
        if (it == w.end() || it->compare(0, p.size(), p) != 0) cout << "NONE\n";
        else cout << *it << "\n";
    }
    return 0;
}
