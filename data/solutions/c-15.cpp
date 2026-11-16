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
    deque<pair<int, int>> q;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (g[i][j] == '2') { d[i][j] = 0; q.push_back({i, j}); }
    vector<int> dx{1, -1, 0, 0}, dy{0, 0, 1, -1};
    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop_front();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || ny < 0 || nx >= n || ny >= m) continue;
            if (g[nx][ny] == '1' || d[nx][ny] != -1) continue;
            d[nx][ny] = d[x][y] + 1;
            q.push_back({nx, ny});
        }
    }
    int ans = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            if (g[i][j] == '0') {
                if (d[i][j] == -1) { cout << -1 << "\n"; return 0; }
                ans = max(ans, d[i][j]);
            }
    cout << ans << "\n";
    return 0;
}
