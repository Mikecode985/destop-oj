#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    map<string, int> lineOf;          // 站名 -> 线路号
    for (int i = 1; i <= n; i++) {
        string name;
        int line;
        cin >> name >> line;
        lineOf[name] = line;
    }

    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        string name;
        cin >> name;
        auto it = lineOf.find(name);   // 查找，找不到返回 end()
        if (it != lineOf.end()) {
            cout << it->second << "\n";
        } else {
            cout << "NO\n";
        }
    }
    return 0;
}
