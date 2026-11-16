#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    for (int i = 1; i <= n; i++) cin >> a[i];
    deque<int> dq;                       // 存下标；对应值从队头到队尾递减
    for (int i = 1; i <= n; i++) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();  // 挤出窗口
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();  // 更小的没用了
        dq.push_back(i);
        if (i >= k) {                    // 第一个完整窗口出现了
            if (i > k) cout << " ";
            cout << a[dq.front()];       // 队头就是窗口内的最大值
        }
    }
    cout << "\n";
    return 0;
}
