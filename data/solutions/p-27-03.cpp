#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pre[i] = pre[i - 1] + x;
    }
    deque<int> dq;
    dq.push_back(0);
    long long ans = LLONG_MIN;
    for (int i = 1; i <= n; i++) {
        while (!dq.empty() && dq.front() < i - k) dq.pop_front();
        ans = max(ans, pre[i] - pre[dq.front()]);
        while (!dq.empty() && pre[dq.back()] >= pre[i]) dq.pop_back();
        dq.push_back(i);
    }
    cout << ans << "\n";
    return 0;
}
