#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];
int color[MAXN];                  // -1 未染色，0 和 1 是两组

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);        // 无向边，两个方向都加
    }
    for (int i = 1; i <= n; i++) color[i] = -1;
    bool ok = true;
    for (int s = 1; s <= n && ok; s++) {
        if (color[s] != -1) continue;
        queue<int> q;
        q.push(s);
        color[s] = 0;
        while (!q.empty() && ok) {
            int u = q.front();
            q.pop();
            for (int v : g[u]) {
                if (color[v] == -1) {
                    color[v] = color[u] ^ 1;   // 染成相反颜色
                    q.push(v);
                } else if (color[v] == color[u]) {
                    ok = false;                // 相邻两点同色，矛盾
                    break;
                }
            }
        }
    }
    cout << (ok ? "Yes" : "No") << "\n";
    return 0;
}
