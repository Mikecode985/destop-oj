#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    const int MAXN = 105;
    char g[MAXN][MAXN];
    for (int i = 1; i <= n; i++) {
        string row;
        cin >> row;                       // 每行没有空格，整行读入
        for (int j = 1; j <= m; j++) {
            g[i][j] = row[j - 1];         // 字符串下标从 0 开始
        }
    }

    string s;
    cin >> s;

    int r = 1, c = 1, moved = 0;
    for (char op : s) {
        int nr = r, nc = c;
        if (op == 'U') nr--;
        else if (op == 'D') nr++;
        else if (op == 'L') nc--;
        else nc++;                        // 剩下的按 'R' 处理

        // 先判断再访问：越界或撞墙就停在原地
        if (nr >= 1 && nr <= n && nc >= 1 && nc <= m && g[nr][nc] == '.') {
            r = nr;
            c = nc;
            moved++;
        }
    }

    cout << r << " " << c << " " << moved << "\n";
    return 0;
}
