#include <bits/stdc++.h>
using namespace std;

// f(n)：还剩 n 级台阶时的走法数
long long climb(int n) {
    if (n <= 1) return 1;                 // 终止条件：0 级或 1 级都只有 1 种
    return climb(n - 1) + climb(n - 2);   // 递推关系：最后一步迈 1 级或 2 级
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cout << climb(n) << "\n";
    return 0;
}
