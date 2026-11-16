#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long best = 0, cur = 0, x;
    cin >> x;
    best = cur = x;
    for (int i = 1; i < n; i++) {
        cin >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}
