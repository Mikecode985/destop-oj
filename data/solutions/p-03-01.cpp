#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());
    cout << a.size() << "\n";
    for (size_t i = 0; i < a.size(); i++) cout << a[i] << (i + 1 == a.size() ? '\n' : ' ');
    return 0;
}
