#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n), b;
    for (auto &x : a) cin >> x;
    b = a;
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    for (int i = 0; i < n; i++) {
        int r = lower_bound(b.begin(), b.end(), a[i]) - b.begin() + 1;
        cout << r << (i == n - 1 ? '\n' : ' ');
    }
    return 0;
}
