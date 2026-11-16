#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m;
    cin >> m;
    map<string, vector<pair<int, string>>> g;
    for (int i = 0; i < m; i++) {
        string name, cat;
        int price;
        cin >> name >> cat >> price;
        g[cat].push_back({price, name});
    }
    for (auto &kv : g) {
        vector<pair<int, string>> &v = kv.second;
        sort(v.begin(), v.end());
        for (auto &p : v) cout << kv.first << " " << p.second << " " << p.first << "\n";
    }
    return 0;
}
