#include <bits/stdc++.h>
using namespace std;
int n, m, sx, sy, ex, ey;
vector<string> g;
bool vis[10][10];
long long cnt = 0;
int dx[4] = {-1, 1, 0, 0}, dy[4] = {0, 0, -1, 1};
void dfs(int x, int y) {
    if (x == ex && y == ey) { cnt++; return; }
    for (int k = 0; k < 4; k++) {
        int nx = x + dx[k], ny = y + dy[k];
        if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
        if (g[nx][ny] == '#' || vis[nx][ny]) continue;
        vis[nx][ny] = true;
        dfs(nx, ny);
        vis[nx][ny] = false;
    }
}
int main() {
    cin >> n >> m;
    g.resize(n);
    for (auto &s : g) cin >> s;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] == 'S') { sx = i; sy = j; }
            if (g[i][j] == 'E') { ex = i; ey = j; }
        }
    vis[sx][sy] = true;
    dfs(sx, sy);
    cout << cnt << "\n";
    return 0;
}
