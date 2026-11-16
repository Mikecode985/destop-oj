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
        string hi = p;
        hi.back() = hi.back() + 1;  // 比所有以 p 开头的串都大
        cout << lower_bound(w.begin(), w.end(), hi) - lower_bound(w.begin(), w.end(), p) << "\n";
    }
    return 0;
}
