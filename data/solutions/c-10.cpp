#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<long long, long long>> a(n);
    for (auto &x : a) cin >> x.first >> x.second;
    sort(a.begin(), a.end(), [](const pair<long long, long long> &x, const pair<long long, long long> &y) {
        return x.second < y.second;
    });
    long long last = -1;
    int cnt = 0;
    for (auto &x : a)
        if (x.first >= last) { cnt++; last = x.second; }
    cout << cnt << "\n";
    return 0;
}
