#include <bits/stdc++.h>
using namespace std;
int fa[100005];
int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) fa[i] = i;
    int cnt = n;
    while (m--) {
        int u, v;
        cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) { fa[a] = b; cnt--; }
    }
    cout << cnt << "\n";
    return 0;
}
