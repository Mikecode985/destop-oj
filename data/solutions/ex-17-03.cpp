#include <bits/stdc++.h>
using namespace std;

const int MAXN = 50005;
int fa[MAXN], rel[MAXN];   // rel：0 同类，1 x 吃上级，2 上级吃 x

int findRoot(int x) {
    if (fa[x] == x) return x;
    int p = fa[x];                     // 先存旧上级
    int root = findRoot(p);
    rel[x] = (rel[x] + rel[p]) % 3;    // 拼出 x 到根的关系
    return fa[x] = root;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        fa[i] = i;
        rel[i] = 0;
    }
    int lie = 0;
    for (int i = 0; i < k; i++) {
        int op, x, y;
        cin >> op >> x >> y;
        if (x > n || y > n) { lie++; continue; }          // 编号根本不存在
        if (op == 2 && x == y) { lie++; continue; }        // 自己吃自己，必假
        int rx = findRoot(x), ry = findRoot(y);
        int want = (op == 1 ? 0 : 1);                      // 期望的 x 对 y 关系
        int now = (rel[x] - rel[y] + 3) % 3;               // 现在已知的关系
        if (rx == ry) {
            if (now != want) lie++;
        } else {
            fa[rx] = ry;
            rel[rx] = (want - now + 3) % 3;                // 让 rx 对 ry 满足 want
        }
    }
    cout << lie << "\n";
    return 0;
}
