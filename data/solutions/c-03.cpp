#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<pair<string, int>> rec;
    for (int i = 0; i < n; i++) {
        int line;
        string st;
        cin >> line >> st;
        rec.push_back({st, line});
    }
    sort(rec.begin(), rec.end());
    while (m--) {
        string st;
        int line;
        cin >> st >> line;
        auto it = lower_bound(rec.begin(), rec.end(), make_pair(st, line));
        if (it != rec.end() && it->first == st && it->second == line) cout << "Yes\n";
        else cout << "No\n";
    }
    return 0;
}
