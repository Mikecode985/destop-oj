#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    // 小根堆：堆顶是"前 k 大"里最小的那个，也就是第 k 大
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pq.push(x);
        if ((int)pq.size() > k) pq.pop();   // 超出 k 个，弹掉最小的
        if (i < k) {
            if (i > 1) cout << " ";
            cout << -1;
        } else {
            if (i > 1) cout << " ";
            cout << pq.top();
        }
    }
    cout << "\n";
    return 0;
}
