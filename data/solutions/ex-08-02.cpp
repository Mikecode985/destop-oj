#include <bits/stdc++.h>
using namespace std;

const int MAXN = 2005;
int a[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    sort(a + 1, a + n + 1);          // 从小到大

    int m = n;                       // 当前还剩几堆
    long long total = 0;
    for (int step = 1; step <= n - 1; step++) {
        long long sum = a[1] + a[2]; // 最小的两堆
        total += sum;
        for (int i = 3; i <= m; i++) a[i - 2] = a[i];   // 去掉前两堆
        m -= 2;
        int pos = m + 1;             // 把新堆插回有序位置
        while (pos > 1 && a[pos - 1] > sum) {
            a[pos] = a[pos - 1];
            pos--;
        }
        a[pos] = (int)sum;
        m++;
    }
    cout << total << "\n";
    return 0;
}
