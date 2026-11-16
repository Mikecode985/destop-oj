#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN];

// 返回第一个满足 a[i] >= x 的下标；不存在返回 n + 1
int lowerBound(int n, int x) {
    int l = 1, r = n, ans = n + 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;   // 不写 (l + r) / 2，防溢出
        if (a[mid] >= x) {
            ans = mid;               // 记下候选答案
            r = mid - 1;             // 再往左找更靠前的
        } else {
            l = mid + 1;             // a[mid] 太小，答案在右边
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];

    while (q--) {
        int x;
        cin >> x;
        int mine = lowerBound(n, x);
        // STL 版返回迭代器，减去 a 得到 1-indexed 下标
        int stl = int(lower_bound(a + 1, a + n + 1, x) - a);
        cout << mine << " " << stl << "\n";
    }
    return 0;
}
