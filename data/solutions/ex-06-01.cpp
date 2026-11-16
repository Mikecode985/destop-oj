#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;                                 // n 元买 n 件

    const int MAXANS = 100005;
    int ra[MAXANS], rb[MAXANS], rc[MAXANS];
    int ans = 0;

    // 只枚举前两种，小葱由“总数 n”直接算出来
    for (int a = 1; a <= n / 5; a++) {
        for (int b = 1; b <= (n - 5 * a) / 3; b++) {
            int c = n - a - b;                // 小葱件数
            if (c < 1) continue;              // 每种至少 1 件
            if (c % 3 != 0) continue;         // 小葱 3 把一组
            if (5 * a + 3 * b + c / 3 != n) continue;
            ra[ans] = a;
            rb[ans] = b;
            rc[ans] = c;
            ans++;
        }
    }

    cout << ans << "\n";
    for (int i = 0; i < ans; i++) {
        cout << ra[i] << " " << rb[i] << " " << rc[i] << "\n";
    }
    return 0;
}
