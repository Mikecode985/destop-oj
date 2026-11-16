#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    unordered_map<long long, int> cnt;
    for (auto &x : a) {
        cin >> x;
        cnt[x]++;
    }
    for (auto x : a)
        if (cnt[x] == 1) { cout << x << "\n"; return 0; }
    cout << -1 << "\n";
    return 0;
}
