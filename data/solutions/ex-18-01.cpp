#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int n, tree[MAXN];

void add(int pos, int val) {
    for (; pos <= n; pos += pos & -pos) tree[pos] += val;
}

int query(int pos) {                        // 求 a[1..pos] 的和
    int sum = 0;
    for (; pos > 0; pos -= pos & -pos) sum += tree[pos];
    return sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    long long ans = 0;                      // 逆序对最多约 n^2/2 个，会超过 int
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        ans += (i - 1) - query(x);          // 前面比 x 大的数
        add(x, 1);                          // 把 x 的出现次数加一
    }
    cout << ans << "\n";
    return 0;
}
