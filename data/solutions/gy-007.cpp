#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 1;
    int n; cin >> n;
    if (MODE == 0) {
        int k, cnt = 0; cin >> k;
        for (int i = 0; i < n; i++) { int x; cin >> x; if (x >= k) cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 1) {
        int l, r, cnt = 0; cin >> l >> r;
        for (int i = 0; i < n; i++) { int x; cin >> x; if (l <= x && x <= r) cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 2) {
        int d, cnt = 0; cin >> d;
        for (int i = 0; i < n; i++) { int x; cin >> x; if (abs(x) % 10 == d) cnt++; }
        cout << cnt << "\n";
    } else if (MODE == 3) {
        set<int> s;
        for (int i = 0; i < n; i++) { int x; cin >> x; s.insert(x); }
        cout << s.size() << "\n";
    } else {
        int k, cnt = 0, first = 0;
        cin >> k;
        for (int i = 1; i <= n; i++) {
            int x; cin >> x;
            if (x == k) { cnt++; if (!first) first = i; }
        }
        cout << cnt << "\n" << first << "\n";
    }
    return 0;
}
