#include <bits/stdc++.h>
using namespace std;

// 按简化规则计算票价：分段递减，超过 18 公里后每 8 公里加 1 元
int fare(int d) {
    if (d <= 4) return 2;
    if (d <= 8) return 3;
    if (d <= 12) return 4;
    if (d <= 18) return 5;
    int extra = (d - 18 + 7) / 8;   // 向上取整：不足 8 公里也算 1 元
    return 5 + extra;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    for (int i = 1; i <= T; i++) {
        int d;
        cin >> d;
        cout << fare(d) << "\n";
    }
    return 0;
}
