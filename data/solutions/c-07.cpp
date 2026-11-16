#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end(), greater<int>());
    long long sum = 0;
    for (int i = 0; i < min(n, k); i++) sum += a[i];
    cout << sum << "\n";
    return 0;
}
