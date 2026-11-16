#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    vector<vector<int>> d(n, vector<int>(m, -1));
    queue<pair<int, int>> q;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (g[i][j] == 'X') { d[i][j] = 0; q.push({i, j}); }
    int dx[4] = {-1, 1, 0, 0}, dy[4] = {0, 0, -1, 1};
    while (!q.empty()) {
        pair<int, int> u = q.front();
        q.pop();
        for (int k = 0; k < 4; k++) {
            int x = u.first + dx[k], y = u.second + dy[k];
            if (x < 0 || x >= n || y < 0 || y >= m) continue;
            if (g[x][y] == '#' || d[x][y] != -1) continue;
            d[x][y] = d[u.first][u.second] + 1;
            q.push({x, y});
        }
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '#') cout << '#';
            else cout << d[i][j];
            cout << (j == m - 1 ? '\n' : ' ');
        }
    }
    return 0;
}
