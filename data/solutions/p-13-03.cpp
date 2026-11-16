#include <bits/stdc++.h>
using namespace std;
int n;
vector<int> a, cur;
void dfs(int start) {
    cout << "{";
    for (size_t i = 0; i < cur.size(); i++) cout << (i ? "," : "") << cur[i];
    cout << "}\n";
    for (int i = start; i < n; i++) {
        if (i > start && a[i] == a[i - 1]) continue;
        cur.push_back(a[i]);
        dfs(i + 1);
        cur.pop_back();
    }
}
int main() {
    cin >> n;
    a.resize(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    dfs(0);
    return 0;
}
