#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 1;
    int n, m; cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    if (MODE == 3) {
        vector<vector<int>> d(n, vector<int>(m, 1e9));
        d[0][0] = g[0][0] - '0';
        priority_queue<tuple<int,int,int>, vector<tuple<int,int,int>>, greater<>> pq;
        pq.push({d[0][0], 0, 0});
        int dx[4] = {1,-1,0,0}, dy[4] = {0,0,1,-1};
        while (!pq.empty()) {
            auto [du, x, y] = pq.top(); pq.pop();
            if (du != d[x][y]) continue;
            for (int k = 0; k < 4; k++) {
                int nx = x + dx[k], ny = y + dy[k];
                if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
                int nd = du + (g[nx][ny] - '0');
                if (nd < d[nx][ny]) { d[nx][ny] = nd; pq.push({nd, nx, ny}); }
            }
        }
        cout << d[n-1][m-1] << "\n";
        return 0;
    }
    if (g[0][0] == '1') { cout << (MODE == 1 ? "0\n" : "-1\n"); return 0; }
    vector<vector<int>> d(n, vector<int>(m, -1)), w(n, vector<int>(m, 0));
    d[0][0] = 0; w[0][0] = 1;
    queue<pair<int,int>> q; q.push({0,0});
    int dx8[8] = {1,-1,0,0,1,1,-1,-1}, dy8[8] = {0,0,1,-1,1,-1,1,-1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        int dirs = (MODE == 2 ? 8 : 4);
        for (int k = 0; k < dirs; k++) {
            int nx = x + (MODE == 2 ? dx8[k] : dx8[k]), ny = y + (MODE == 2 ? dy8[k] : dy8[k]);
            if (nx < 0 || nx >= n || ny < 0 || ny >= m || g[nx][ny] == '1') continue;
            if (d[nx][ny] < 0) {
                d[nx][ny] = d[x][y] + 1; w[nx][ny] = w[x][y]; q.push({nx, ny});
            } else if (d[nx][ny] == d[x][y] + 1) {
                w[nx][ny] = (w[nx][ny] + w[x][y]) % 1000000007;
            }
        }
    }
    if (MODE == 1) {
        int cnt = 0;
        for (int i = 0; i < n; i++) for (int j = 0; j < m; j++) if (d[i][j] >= 0) cnt++;
        cout << cnt << "\n";
    } else if (MODE == 4) {
        cout << (d[n-1][m-1] < 0 ? 0 : w[n-1][m-1]) << "\n";
    } else {
        cout << d[n-1][m-1] << "\n";
    }
    return 0;
}
