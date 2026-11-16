#include <bits/stdc++.h>
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
