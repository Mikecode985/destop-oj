#include <bits/stdc++.h>
using namespace std;
int n;
long long bit[100005];
void add(int i) {
    for (; i <= n; i += i & -i) bit[i]++;
}
long long sum(int i) {
    long long s = 0;
    for (; i > 0; i -= i & -i) s += bit[i];
    return s;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    vector<long long> a(n), b;
    for (auto &x : a) cin >> x;
    b = a;
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    long long ans = 0;
    for (int i = n - 1; i >= 0; i--) {
        int r = lower_bound(b.begin(), b.end(), a[i]) - b.begin() + 1;
        ans += sum(r - 1);
        add(r);
    }
    cout << ans << "\n";
    return 0;
}
