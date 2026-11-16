#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> d;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        auto it = upper_bound(d.begin(), d.end(), x);
        if (it == d.end()) d.push_back(x);
        else *it = x;
    }
    cout << d.size() << "\n";
    return 0;
}
