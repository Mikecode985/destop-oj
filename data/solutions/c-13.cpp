#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    int best = 0;
    vector<int> dx{1, -1, 0, 0}, dy{0, 0, 1, -1};
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] != '1') continue;
            int cnt = 0;
            deque<pair<int, int>> q;
            q.push_back({i, j});
            g[i][j] = '0';
            while (!q.empty()) {
                auto [x, y] = q.front();
                q.pop_front();
                cnt++;
                for (int d = 0; d < 4; d++) {
                    int nx = x + dx[d], ny = y + dy[d];
                    if (nx < 0 || ny < 0 || nx >= n || ny >= m || g[nx][ny] != '1') continue;
                    g[nx][ny] = '0';
                    q.push_back({nx, ny});
                }
            }
            best = max(best, cnt);
        }
    cout << best << "\n";
    return 0;
}
