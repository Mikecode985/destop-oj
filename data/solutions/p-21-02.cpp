#include <bits/stdc++.h>
using namespace std;
long long g[205][205];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) cin >> g[i][j];
    const long long INF = (long long)4e18;
    vector<long long> d(n + 1, INF);
    vector<int> vis(n + 1, 0);
    d[1] = 0;
    long long total = 0;
    for (int it = 1; it <= n; it++) {
        int u = -1;
        for (int i = 1; i <= n; i++)
            if (!vis[i] && (u == -1 || d[i] < d[u])) u = i;
        if (u == -1 || d[u] >= INF) { cout << -1 << "\n"; return 0; }
        vis[u] = 1;
        total += d[u];
        for (int v = 1; v <= n; v++)
            if (!vis[v] && g[u][v] > 0 && g[u][v] < d[v]) d[v] = g[u][v];
    }
    cout << total << "\n";
    return 0;
}
