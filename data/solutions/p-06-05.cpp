#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int half = n / 2;
    vector<long long> L{0}, R{0};
    for (int i = 0; i < half; i++) {
        int sz = L.size();
        for (int j = 0; j < sz; j++) L.push_back(L[j] + a[i]);
    }
    for (int i = half; i < n; i++) {
        int sz = R.size();
        for (int j = 0; j < sz; j++) R.push_back(R[j] + a[i]);
    }
    sort(L.begin(), L.end());
    long long ans = 0;
    for (long long s : R)
        ans += upper_bound(L.begin(), L.end(), S - s) - lower_bound(L.begin(), L.end(), S - s);
    cout << ans << "\n";
    return 0;
}
