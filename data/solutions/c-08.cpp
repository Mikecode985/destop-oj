#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> p(n);
    for (auto &x : p) cin >> x;
    while (m--) {
        int x;
        cin >> x;
        auto it = upper_bound(p.begin(), p.end(), x);
        cout << (it == p.end() ? -1 : *it) << "\n";
    }
    return 0;
}
