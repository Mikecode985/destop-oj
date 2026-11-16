#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long target;
    cin >> n >> target;
    set<long long> s;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        s.insert(x);
    }
    bool any = false;
    for (auto x : s) {
        long long y = target - x;
        if (y > x && s.count(y)) {
            cout << x << " " << y << "\n";
            any = true;
        }
    }
    if (!any) cout << "No\n";
    return 0;
}
