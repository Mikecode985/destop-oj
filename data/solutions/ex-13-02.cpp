#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
int a[MAXN], n, target, cnt = 0;
vector<int> path;

void dfs(int start, int remain) {
    if (remain == 0) {                    // 正好凑够，输出一组
        for (size_t i = 0; i < path.size(); i++) {
            if (i > 0) cout << " ";
            cout << path[i];
        }
        cout << "\n";
        cnt++;
        return;
    }
    for (int i = start; i <= n; i++) {
        if (a[i] > remain) break;         // 已排序：后面的更大，直接剪枝
        if (i > start && a[i] == a[i - 1]) continue;  // 同层跳过重复值
        path.push_back(a[i]);             // 做选择
        dfs(i + 1, remain - a[i]);        // 每个数最多用一次，从 i+1 继续
        path.pop_back();                  // 撤销选择
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> target;
    for (int i = 1; i <= n; i++) cin >> a[i];
    sort(a + 1, a + n + 1);
    dfs(1, target);
    cout << cnt << "\n";
    return 0;
}
