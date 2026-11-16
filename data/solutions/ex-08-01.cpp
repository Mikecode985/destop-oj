#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
struct Act {
    int s, e;               // 开始时间、结束时间
} a[MAXN];

// 结束早的排前面；结束时间相同，开始早的排前面（让结果稳定）
bool cmp(const Act &x, const Act &y) {
    if (x.e != y.e) return x.e < y.e;
    return x.s < y.s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i].s >> a[i].e;
    sort(a + 1, a + n + 1, cmp);     // 关键：按结束时间排序

    int cnt = 0, lastEnd = -1;       // lastEnd：上一场选中活动的结束时间
    for (int i = 1; i <= n; i++) {
        if (a[i].s >= lastEnd) {     // 上一场结束后才能开始这一场
            cnt++;
            lastEnd = a[i].e;
        }
    }
    cout << cnt << "\n";
    return 0;
}
