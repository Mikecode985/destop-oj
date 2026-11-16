#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long a[1005];
    for (int i = 1; i <= n; i++) cin >> a[i];

    long long ans = a[1];                     // 初始值取第一个元素
    for (int l = 1; l <= n; l++) {            // 枚举左端点
        long long sum = 0;
        for (int r = l; r <= n; r++) {        // 枚举右端点，边扩边加
            sum += a[r];
            ans = max(ans, sum);
        }
    }
    cout << ans << "\n";
    return 0;
}
