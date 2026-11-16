#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    int n = s.size(), best = 0;
    for (int c = 0; c < n; c++) {
        for (int l = c, r = c; l >= 0 && r < n && s[l] == s[r]; l--, r++)
            best = max(best, r - l + 1);
        for (int l = c, r = c + 1; l >= 0 && r < n && s[l] == s[r]; l--, r++)
            best = max(best, r - l + 1);
    }
    cout << best << "\n";
    return 0;
}
