#include <bits/stdc++.h>
using namespace std;

bool isLeap(int y) {
    return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int year, month, day;
    cin >> year >> month >> day;

    const int days[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    int ans = 0;
    for (int m = 1; m < month; m++) {
        ans += days[m];
        if (m == 2 && isLeap(year)) ans += 1;   // 闰年的二月多一天
    }
    ans += day;

    cout << ans << "\n";
    return 0;
}
