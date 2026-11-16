#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<long long> pos(n + 1), w(n + 1);
    vector<long long> xs;
    xs.reserve(n);
    for (int i = 1; i <= n; i++) {
        cin >> pos[i] >> w[i];
        xs.push_back(pos[i]);
    }

    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());   // 去重，k 个不同坐标
    int k = int(xs.size());

    vector<long long> sum(k, 0);        // 0-indexed：压缩后的坐标
    for (int i = 1; i <= n; i++) {
        int id = int(lower_bound(xs.begin(), xs.end(), pos[i]) - xs.begin());
        sum[id] += w[i];                // 同一坐标的人合并
    }
    vector<long long> pre(k + 1, 0);    // pre[i] = 前 i 个坐标的人数
    for (int i = 0; i < k; i++) pre[i + 1] = pre[i] + sum[i];

    while (m--) {
        long long L, R;
        cin >> L >> R;
        int l = int(lower_bound(xs.begin(), xs.end(), L) - xs.begin());   // 第一个 >= L
        int r = int(upper_bound(xs.begin(), xs.end(), R) - xs.begin());   // 第一个 > R
        cout << pre[r] - pre[l] << "\n";
    }
    return 0;
}
