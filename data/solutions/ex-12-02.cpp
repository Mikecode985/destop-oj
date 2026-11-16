#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
char g[MAXN][MAXN];
int fireTime[MAXN][MAXN];
int n, m;
int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    queue<pair<int, int>> q;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> g[i][j];
            fireTime[i][j] = -1;          // -1：还没烧到
            if (g[i][j] == 'F') {
                fireTime[i][j] = 0;       // 关键：所有火源一起入队
                q.push({i, j});
            }
        }
    }
    while (!q.empty()) {
        int x = q.front().first;
        int y = q.front().second;
        q.pop();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k];
            int ny = y + dy[k];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            if (g[nx][ny] == '#' || fireTime[nx][ny] != -1) continue;
            fireTime[nx][ny] = fireTime[x][y] + 1;
            q.push({nx, ny});
        }
    }
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (j > 1) cout << " ";
            cout << fireTime[i][j];
        }
        cout << "\n";
    }
    return 0;
}
