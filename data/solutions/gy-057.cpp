#include <bits/stdc++.h>
using namespace std;
int par[20];
int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 1;
    int n, m; cin >> n >> m;
    for (int i = 1; i <= n; i++) par[i] = i;
    int red = 0;
    for (int i = 0; i < m; i++) {
        int a, b; cin >> a >> b;
        int ra = find(a), rb = find(b);
        if (ra == rb) red++; else par[ra] = rb;
    }
    map<int,int> sz;
    for (int i = 1; i <= n; i++) sz[find(i)]++;
    if (MODE == 0) cout << sz.size() << "\n";
    else if (MODE == 1) { int best = 0; for (auto &p : sz) best = max(best, p.second); cout << best << "\n"; }
    else if (MODE == 2) cout << (find(1) == find(n) ? "YES" : "NO") << "\n";
    else if (MODE == 3) cout << red << "\n";
    else {
        long long ans = 0;
        for (auto &p : sz) ans += 1LL * p.second * (p.second - 1) / 2;
        cout << ans << "\n";
    }
    return 0;
}
