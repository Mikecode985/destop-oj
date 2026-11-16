#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    priority_queue<long long> lo;          // 左半：大根堆
    priority_queue<long long, vector<long long>, greater<long long>> hi;  // 右半：小根堆
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        lo.push(x);
        hi.push(lo.top());                 // 左边最大的挪到右边，保证有序分割
        lo.pop();
        if (hi.size() > lo.size()) {       // 左半只允许比右半多 0 或 1 个
            lo.push(hi.top());
            hi.pop();
        }
        cout << lo.top() << "\n";          // 左堆顶就是中位数
    }
    return 0;
}
