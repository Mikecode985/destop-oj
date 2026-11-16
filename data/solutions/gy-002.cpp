#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 1;
    int n; cin >> n;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    if (MODE == 0) {
        long long s = 0, best = a[0]; int pos = 1;
        for (int i = 0; i < n; i++) {
            s += a[i];
            if (a[i] > best) { best = a[i]; pos = i + 1; }
        }
        cout << s << "\n" << pos << "\n";
    } else if (MODE == 1) {
        long long pos = 0, non = 0;
        for (long long x : a) { if (x > 0) pos += x; else non++; }
        cout << pos << "\n" << non << "\n";
    } else if (MODE == 2) {
        long long s = 0;
        for (int i = 0; i < n; i++) s += a[i] * (i + 1);
        cout << s << "\n";
    } else if (MODE == 3) {
        long long s = 0;
        for (long long x : a) s += x * x;
        cout << s << "\n";
    } else {
        long long s = 0;
        for (int i = 0; i < n; i++) s += (i % 2 == 0 ? a[i] : -a[i]);
        cout << s << "\n";
    }
    return 0;
}
