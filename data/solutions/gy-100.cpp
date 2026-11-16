#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 4;
    string s; cin >> s;
    if (MODE == 0) {
        int bal = 0; bool ok = true;
        for (char c : s) { bal += (c == '(' ? 1 : -1); if (bal < 0) ok = false; }
        cout << (ok && bal == 0 ? "YES" : "NO") << "\n";
    } else if (MODE == 1) {
        int bal = 0, need = 0;
        for (char c : s) {
            bal += (c == '(' ? 1 : -1);
            if (bal < 0) { need++; bal = 0; }
        }
        cout << need + bal << "\n";
    } else if (MODE == 2) {
        int bal = 0, ans = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            bal += (s[i] == '(' ? 1 : -1);
            if (bal < 0) break;
            if (bal == 0) ans = i + 1;
        }
        cout << ans << "\n";
    } else if (MODE == 3) {
        int bal = 0, mx = 0;
        for (char c : s) { bal += (c == '(' ? 1 : -1); mx = max(mx, bal); }
        cout << mx << "\n";
    } else {
        int bal = 0, pairs = 0;
        for (char c : s) {
            if (c == '(') bal++;
            else if (bal > 0) { bal--; pairs++; }
        }
        cout << pairs << "\n";
    }
    return 0;
}
