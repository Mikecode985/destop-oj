#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int fa[MAXN], sz[MAXN];

int findRoot(int x) {
    if (fa[x] == x) return x;
    return fa[x] = findRoot(fa[x]);        // 路径压缩：回来时直接挂到根上
}

void unite(int a, int b) {
    int ra = findRoot(a), rb = findRoot(b);
    if (ra == rb) return;
    if (sz[ra] < sz[rb]) swap(ra, rb);     // 小树挂到大树下面，控制树高
    fa[rb] = ra;
    sz[ra] += sz[rb];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++) {
        fa[i] = i;
        sz[i] = 1;
    }
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        unite(a, b);
    }
    while (q--) {
        int a, b;
        cin >> a >> b;
        cout << (findRoot(a) == findRoot(b) ? "Yes" : "No") << "\n";
    }
    return 0;
}
