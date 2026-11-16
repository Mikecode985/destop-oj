#include <bits/stdc++.h>
using namespace std;

int n, ans = 0;
bool col[20], diag1[40], diag2[40];

void dfs(int row) {                       // 准备放第 row 行的皇后
    if (row > n) {                        // n 行都放好了，是一个合法方案
        ans++;
        return;
    }
    for (int c = 1; c <= n; c++) {
        int d1 = row - c + n;             // 主对角线编号，加 n 防负数
        int d2 = row + c;                 // 副对角线编号
        if (col[c] || diag1[d1] || diag2[d2]) continue;   // 冲突，换一列
        col[c] = diag1[d1] = diag2[d2] = true;            // 做选择
        dfs(row + 1);
        col[c] = diag1[d1] = diag2[d2] = false;           // 撤销选择
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    dfs(1);
    cout << ans << "\n";
    return 0;
}
