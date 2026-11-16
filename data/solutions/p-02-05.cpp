#include <bits/stdc++.h>
using namespace std;
int main() {
    int m;
    cin >> m;
    cin.ignore();
    vector<pair<string, int>> a;
    for (int i = 0; i < m; i++) {
        string line;
        getline(cin, line);
        while (!line.empty() && line.back() == '\r') line.pop_back();
        size_t p = line.rfind(' ');
        string nm = line.substr(0, p);
        int pr = stoi(line.substr(p + 1));
        a.push_back({nm, pr});
    }
    sort(a.begin(), a.end(), [](const pair<string, int> &x, const pair<string, int> &y) {
        if (x.second != y.second) return x.second < y.second;
        return x.first < y.first;
    });
    for (auto &p : a) cout << p.first << " " << p.second << "\n";
    return 0;
}
