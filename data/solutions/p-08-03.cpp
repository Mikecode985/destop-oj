#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    int la = 0, ra = n - 1, lb = 0, rb = n - 1;
    long long ans = 0;
    while (la <= ra) {
        if (a[ra] > b[rb]) { ans += 200; ra--; rb--; }
        else if (a[la] > b[lb]) { ans += 200; la++; lb++; }
        else {
            if (a[la] < b[rb]) ans -= 200;
            la++;
            rb--;
        }
    }
    cout << ans << "\n";
    return 0;
}
