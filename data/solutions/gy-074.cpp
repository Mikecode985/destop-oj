#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 3;
    string s; cin >> s;
    if (MODE == 0) {
        int cnt = 0;
        for (char c : s) if (string("aeiou").find(c) != string::npos) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 1) {
        int cnt = 0;
        for (char c : s) if (isalpha(c) && string("aeiou").find(c) == string::npos) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 2) {
        int cnt[26] = {0};
        for (char c : s) cnt[c - 'a']++;
        int best = 0;
        for (int i = 1; i < 26; i++) if (cnt[i] > cnt[best]) best = i;
        cout << char('a' + best) << "\n";
    } else if (MODE == 3) {
        string r = s; reverse(r.begin(), r.end());
        cout << (s == r ? "YES" : "NO") << "\n";
    } else {
        for (int i = 0; i < (int)s.size(); ) {
            int j = i;
            while (j < (int)s.size() && s[j] == s[i]) j++;
            cout << s[i] << j - i;
            i = j;
        }
        cout << "\n";
    }
    return 0;
}
