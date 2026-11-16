#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 2;
    if (MODE == 4) {
        long long a, b; cin >> a >> b;
        long long g = gcd(a, b);
        cout << a / g << " " << b / g << "\n";
        return 0;
    }
    int n; cin >> n; vector<int> a(n);
    for (int &x : a) cin >> x;
    if (MODE == 0) { int g = 0; for (int x : a) g = gcd(g, x); cout << g << "\n"; }
    else if (MODE == 1) { long long l = 1; for (int x : a) l = l * x / gcd(l, x); cout << l << "\n"; }
    else if (MODE == 2) {
        long long s = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) s += gcd(a[i], a[j]);
        cout << s << "\n";
    } else {
        int cnt = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (gcd(a[i], a[j]) == 1) cnt++;
        cout << cnt << "\n";
    }
    return 0;
}
