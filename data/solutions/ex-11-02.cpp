#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
int n, m;
char g[MAXN][MAXN];
int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

void dfs(int x, int y) {
    if (x < 1 || x > n || y < 1 || y > m) return;   // 出界
    if (g[x][y] != '.') return;                     // 不是草坪（或已访问）
    g[x][y] = '#';                                  // 淹掉，兼作访问标记
    for (int k = 0; k < 4; k++) dfs(x + dx[k], y + dy[k]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) cin >> g[i][j];

    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (g[i][j] == '.') {
                cnt++;              // 新的一块
                dfs(i, j);          // 把整块淹掉
            }
        }
    }
    cout << cnt << "\n";
    return 0;
}
