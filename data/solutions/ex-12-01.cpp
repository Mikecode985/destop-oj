#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
char g[MAXN][MAXN];
int dist[MAXN][MAXN];
int n, m, sx, sy, ex, ey;
int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

int bfs() {
    for (int i = 1; i <= n; i++)          // 初始化：-1 表示没访问过
        for (int j = 1; j <= m; j++) dist[i][j] = -1;
    queue<pair<int, int>> q;
    dist[sx][sy] = 0;                     // 起点距离为 0，别忘了这一句
    q.push({sx, sy});
    while (!q.empty()) {
        int x = q.front().first;
        int y = q.front().second;
        q.pop();
        if (x == ex && y == ey) return dist[x][y];   // 第一次到终点就是最短
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k];
            int ny = y + dy[k];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;  // 先判越界
            if (g[nx][ny] == '#' || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
    return -1;                            // 队列空了还没到，就是走不通
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> g[i][j];
            if (g[i][j] == 'S') { sx = i; sy = j; }
            if (g[i][j] == 'E') { ex = i; ey = j; }
        }
    }
    cout << bfs() << "\n";
    return 0;
}
