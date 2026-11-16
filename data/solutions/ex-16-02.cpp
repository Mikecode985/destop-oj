#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pq.push(x);
    }
    long long total = 0;
    while (pq.size() > 1) {
        long long a = pq.top();
        pq.pop();
        long long b = pq.top();
        pq.pop();
        total += a + b;          // 这一趟合并消耗 a+b
        pq.push(a + b);          // 新堆放回去，参与后面的合并
    }
    cout << total << "\n";
    return 0;
}
