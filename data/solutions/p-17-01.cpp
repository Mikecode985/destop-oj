#include <bits/stdc++.h>
using namespace std;
int par[100005], sz[100005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) { par[i] = i; sz[i] = 1; }
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) {
            if (sz[a] < sz[b]) swap(a, b);
            par[b] = a;
            sz[a] += sz[b];
        }
    }
    int cnt = 0, mx = 0;
    for (int i = 1; i <= n; i++)
        if (find(i) == i) { cnt++; mx = max(mx, sz[i]); }
    cout << cnt << " " << mx << "\n";
    return 0;
}
