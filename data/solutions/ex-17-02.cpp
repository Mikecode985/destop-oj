#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
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
    for (int i = 1; i <= n; i++) fa[i] = i;
    int comp = n;                    // 一开始每个点自成一伙
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        int ra = findRoot(a), rb = findRoot(b);
        if (ra != rb) {              // 只有真的合并成功，伙数才减一
            fa[rb] = ra;
            comp--;
        }
    }
    cout << comp << "\n" << comp - 1 << "\n";   // 第二行：最少加几条边
    return 0;
}
