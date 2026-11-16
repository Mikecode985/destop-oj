#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
bool vis[MAXN][MAXN];       // 状态 (x, y)：0 升也合法，所以从 0 开始编号

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int a, b, c;
    cin >> a >> b >> c;

    queue<pair<int, int>> q;
    vis[0][0] = true;
    q.push({0, 0});
    int step = 0;
    while (!q.empty()) {
        int sz = q.size();            // 记下这一层有多少个状态
        while (sz--) {
            int x = q.front().first;
            int y = q.front().second;
            q.pop();
            if (x == c || y == c) {   // 目标可能出现在 B 桶，别只判一个桶
                cout << step << "\n";
                return 0;
            }
            int pourXY = min(x, b - y);   // A 倒给 B：受两个上限约束
            int pourYX = min(y, a - x);   // B 倒给 A
            int nx[6] = {a, x, 0, x, x - pourXY, x + pourYX};
            int ny[6] = {y, b, y, 0, y + pourXY, y - pourYX};
            for (int k = 0; k < 6; k++) {
                if (!vis[nx[k]][ny[k]]) {
                    vis[nx[k]][ny[k]] = true;
                    q.push({nx[k], ny[k]});
                }
            }
        }
        step++;                       // 这一层处理完，步数加一
    }
    cout << -1 << "\n";
    return 0;
}
