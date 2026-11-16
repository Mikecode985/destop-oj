#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, p;
    cin >> s >> p;
    int m = p.size();
    vector<int> pi(m, 0);
    for (int i = 1; i < m; i++) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j]) j = pi[j - 1];
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    int j = 0;
    long long cnt = 0;
    for (char c : s) {
        while (j > 0 && c != p[j]) j = pi[j - 1];
        if (c == p[j]) j++;
        if (j == m) { cnt++; j = pi[j - 1]; }
    }
    cout << cnt << "\n";
    return 0;
}
