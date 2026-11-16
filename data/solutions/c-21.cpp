#include <bits/stdc++.h>
using namespace std;
int fa[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++) fa[i] = i;
    while (m--) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) fa[a] = b;
    }
    while (q--) {
        int u, v;
        cin >> u >> v;
        cout << (find(u) == find(v) ? "Yes\n" : "No\n");
    }
    return 0;
}
