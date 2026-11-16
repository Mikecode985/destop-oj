#include <bits/stdc++.h>
using namespace std;
int n, m;
vector<int> adj[25];
int col[25];
bool dfs(int u) {
    if (u == n + 1) return true;
    for (int c = 1; c <= 4; c++) {
        bool ok = true;
        for (int v : adj[u])
            if (col[v] == c) { ok = false; break; }
        if (!ok) continue;
        col[u] = c;
        if (dfs(u + 1)) return true;
        col[u] = 0;
    }
    return false;
}
int main() {
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    if (!dfs(1)) { cout << "No\n"; return 0; }
    for (int i = 1; i <= n; i++) cout << col[i] << "\n";
    return 0;
}
