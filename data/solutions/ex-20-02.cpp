#include <bits/stdc++.h>
using namespace std;

const int MAXN = 305;
const long long INF = (long long)1e18;
long long d[MAXN][MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++)
            d[i][j] = (i == j ? 0 : INF);
    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        d[u][v] = min(d[u][v], w);       // 重边只留最短的那条
        d[v][u] = min(d[v][u], w);
    }
    for (int k = 1; k <= n; k++)         // k 必须是最外层
        for (int i = 1; i <= n; i++)
            for (int j = 1; j <= n; j++)
                if (d[i][k] < INF && d[k][j] < INF)
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
    while (q--) {
        int s, t;
        cin >> s >> t;
        cout << (d[s][t] == INF ? -1 : d[s][t]) << "\n";
    }
    return 0;
}
