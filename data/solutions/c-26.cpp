#include <bits/stdc++.h>
using namespace std;
int fa[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
struct E { int u, v; long long w; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<E> e(m);
    for (auto &x : e) cin >> x.u >> x.v >> x.w;
    sort(e.begin(), e.end(), [](const E &a, const E &b) { return a.w < b.w; });
    for (int i = 1; i <= n; i++) fa[i] = i;
    long long tot = 0;
    int used = 0;
    for (auto &x : e) {
        int a = find(x.u), b = find(x.v);
        if (a == b) continue;
        fa[a] = b;
        tot += x.w;
        if (++used == n - 1) break;
    }
    cout << (used == n - 1 ? tot : -1) << "\n";
    return 0;
}
