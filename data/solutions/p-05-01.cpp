#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int cur = 1;
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        int t;
        cin >> t;
        ans += abs(t - cur) + 1;
        cur = t;
    }
    cout << ans << " " << cur << "\n";
    return 0;
}
