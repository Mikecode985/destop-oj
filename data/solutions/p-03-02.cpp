#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    map<string, int> cnt;
    for (int i = 0; i < n; i++) {
        string s;
        cin >> s;
        cnt[s]++;
    }
    for (auto &p : cnt) cout << p.first << " " << p.second << "\n";
    return 0;
}
