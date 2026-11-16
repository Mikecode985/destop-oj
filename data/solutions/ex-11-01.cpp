#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
int n, m, sx, sy, ex, ey;
char g[MAXN][MAXN];
bool vis[MAXN][MAXN];
int dx[4] = {-1, 1, 0, 0};       // 上、下、左、右
int dy[4] = {0, 0, -1, 1};

bool dfs(int x, int y) {
    if (x < 1 || x > n || y < 1 || y > m) return false;   // 出界
    if (g[x][y] == '#' || vis[x][y]) return false;        // 墙或走过
    if (x == ex && y == ey) return true;                  // 到终点了
    vis[x][y] = true;                                     // 打记号，防止绕圈
    for (int k = 0; k < 4; k++) {
        if (dfs(x + dx[k], y + dy[k])) return true;       // 找到一条就够了
    }
    return false;                                         // 四个方向都走不通
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++) cin >> g[i][j];
    cin >> sx >> sy >> ex >> ey;

    cout << (dfs(sx, sy) ? "YES" : "NO") << "\n";
    return 0;
}
