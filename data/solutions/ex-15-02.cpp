#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    map<string, int> cnt;            // 键自动按字典序排好
    for (int i = 1; i <= n; i++) {
        string w;
        cin >> w;
        cnt[w]++;                    // 不存在则新建并置 0，再自增
    }
    for (const auto &kv : cnt) {     // 有序遍历，直接就是字典序
        cout << kv.first << " " << kv.second << "\n";
    }
    return 0;
}
