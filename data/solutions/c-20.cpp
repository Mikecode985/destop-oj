#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    nth_element(a.begin(), a.begin() + (k - 1), a.end(), greater<int>());
    cout << a[k - 1] << "\n";
    return 0;
}
