#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    sort(a.begin(), a.end());                            // 1. 排序
    a.erase(unique(a.begin(), a.end()), a.end());        // 2. 去重

    if (k >= 1 && k <= (int)a.size()) {
        cout << a[k - 1] << "\n";       // 第 k 小在 0-indexed 的 k-1 处
    } else {
        cout << "NO\n";
    }
    return 0;
}
