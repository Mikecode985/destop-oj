#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<string> w(n);
    for (auto &s : w) cin >> s;
    string s, t;
    cin >> s >> t;
    if (s == t) { cout << 0 << "\n"; return 0; }
    int si = -1, ti = -1;
    for (int i = 0; i < n; i++) {
        if (w[i] == s) si = i;
        if (w[i] == t) ti = i;
    }
    if (si < 0 || ti < 0) { cout << -1 << "\n"; return 0; }
    vector<int> d(n, -1);
    queue<int> q;
    d[si] = 0;
    q.push(si);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v = 0; v < n; v++) {
            if (d[v] != -1 || w[v].size() != w[u].size()) continue;
            int diff = 0;
            for (size_t k = 0; k < w[u].size(); k++)
                if (w[u][k] != w[v][k]) diff++;
            if (diff == 1) {
                d[v] = d[u] + 1;
                if (v == ti) { cout << d[v] << "\n"; return 0; }
                q.push(v);
            }
        }
    }
    cout << -1 << "\n";
    return 0;
}
