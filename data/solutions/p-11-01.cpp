#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    vector<vector<int>> vis(n, vector<int>(m, 0));
    int dx[8] = {-1, -1, -1, 0, 0, 1, 1, 1};
    int dy[8] = {-1, 0, 1, -1, 1, -1, 0, 1};
    int comp = 0;
    vector<pair<int, int>> st;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (g[i][j] != '1' || vis[i][j]) continue;
            comp++;
            vis[i][j] = 1;
            st.push_back({i, j});
            while (!st.empty()) {
                pair<int, int> u = st.back();
                st.pop_back();
                for (int d = 0; d < 8; d++) {
                    int x = u.first + dx[d], y = u.second + dy[d];
                    if (x < 0 || x >= n || y < 0 || y >= m) continue;
                    if (g[x][y] == '1' && !vis[x][y]) {
                        vis[x][y] = 1;
                        st.push_back({x, y});
                    }
                }
            }
        }
    cout << comp << "\n";
    return 0;
}
