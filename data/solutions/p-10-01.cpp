#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<long long> a(n), b(m);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    int i = 0, j = 0;
    vector<long long> c;
    c.reserve(n + m);
    while (i < n && j < m) {
        if (a[i] <= b[j]) c.push_back(a[i++]);
        else c.push_back(b[j++]);
    }
    while (i < n) c.push_back(a[i++]);
    while (j < m) c.push_back(b[j++]);
    for (size_t k = 0; k < c.size(); k++) cout << c[k] << (k + 1 == c.size() ? '\n' : ' ');
    return 0;
}
