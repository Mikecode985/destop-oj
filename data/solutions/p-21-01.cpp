#include <bits/stdc++.h>
using namespace std;
struct Edge { int u, v; long long w; };
int par[100005];
int find(int x) {
    while (par[x] != x) { par[x] = par[par[x]]; x = par[x]; }
    return x;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<Edge> e(m);
    for (auto &x : e) cin >> x.u >> x.v >> x.w;
    sort(e.begin(), e.end(), [](const Edge &a, const Edge &b) { return a.w < b.w; });
    for (int i = 1; i <= n; i++) par[i] = i;
    long long total = 0;
    int used = 0;
    for (auto &x : e) {
        int a = find(x.u), b = find(x.v);
        if (a == b) continue;
        par[a] = b;
        total += x.w;
        if (++used == n - 1) break;
    }
    cout << (used == n - 1 ? total : -1) << "\n";
    return 0;
}
