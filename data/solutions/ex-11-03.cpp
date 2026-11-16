#include <bits/stdc++.h>
using namespace std;

int n;
int path[10];              // 当前选出的序列
bool used[10];             // 数字 i 有没有被用过

void dfs(int depth) {      // 已经选好了 depth 个数
    if (depth == n) {      // 选满了，输出一种排列
        for (int i = 0; i < n; i++) cout << path[i] << (i == n - 1 ? '\n' : ' ');
        return;
    }
    for (int x = 1; x <= n; x++) {
        if (used[x]) continue;      // 这个数已经用过了
        used[x] = true;             // 做出选择
        path[depth] = x;
        dfs(depth + 1);             // 往下走一层
        used[x] = false;            // 回溯：撤销选择
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    dfs(0);
    return 0;
}
