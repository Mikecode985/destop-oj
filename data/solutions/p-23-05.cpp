#include <bits/stdc++.h>
using namespace std;
long long solve(const vector<long long> &a, int l, int r) {
    long long take = 0, skip = 0;
    for (int i = l; i <= r; i++) {
        long long nt = skip + a[i];
        long long ns = max(take, skip);
        take = nt;
        skip = ns;
    }
    return max(take, skip);
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    if (n == 1) { cout << a[0] << "\n"; return 0; }
    cout << max(solve(a, 0, n - 2), solve(a, 1, n - 1)) << "\n";
    return 0;
}
