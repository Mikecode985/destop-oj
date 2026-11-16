#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005, MAXM = 200005;
struct Edge { int u, v; long long w; };
Edge edges[MAXM];
bool cmp(const Edge &a, const Edge &b) { return a.w < b.w; }
int fa[MAXN];

int findRoot(int x) {
    if (fa[x] == x) return x;
    return fa[x] = findRoot(fa[x]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++)
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
    sort(edges, edges + m, cmp);           // 先按造价从低到高
    for (int i = 1; i <= n; i++) fa[i] = i;
    long long total = 0;
    int used = 0;
    for (int i = 0; i < m && used < n - 1; i++) {
        int ru = findRoot(edges[i].u), rv = findRoot(edges[i].v);
        if (ru != rv) {                    // 两端还不通，修它不会成环
            fa[ru] = rv;
            total += edges[i].w;
            used++;
        }
    }
    if (used < n - 1) cout << -1 << "\n";  // 图不连通，没有生成树
    else cout << total << "\n";
    return 0;
}
