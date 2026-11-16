# -*- coding: utf-8 -*-
"""第 2～3 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-02-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<string> name(n);
    vector<int> price(n);
    for (int i = 0; i < n; i++) cin >> name[i] >> price[i];
    vector<int> used(n, 0);
    int out = min(n, 3);
    for (int k = 0; k < out; k++) {
        int best = -1;
        for (int i = 0; i < n; i++) {
            if (used[i]) continue;
            if (best == -1 || price[i] > price[best]) best = i;
        }
        used[best] = 1;
        cout << name[best] << " " << price[best] << "\n";
    }
    return 0;
}
'''

SOL["p-02-05"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-03-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    a.erase(unique(a.begin(), a.end()), a.end());
    cout << a.size() << "\n";
    for (size_t i = 0; i < a.size(); i++) cout << a[i] << (i + 1 == a.size() ? '\n' : ' ');
    return 0;
}
'''

SOL["p-03-02"] = r'''#include <bits/stdc++.h>
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
'''

SOL["p-03-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> a(n, vector<int>(m));
    for (int i = 0; i < n; i++) {
        long long s = 0;
        for (int j = 0; j < m; j++) {
            cin >> a[i][j];
            s += a[i][j];
        }
        cout << s << "\n";
    }
    return 0;
}
'''

SOL["p-03-05"] = r'''#include <bits/stdc++.h>
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
'''
