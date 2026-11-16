#include <bits/stdc++.h>
using namespace std;
int n;
bool isp[25];
bool used[10];
int ans[10];
bool found = false;
void dfs(int d, int last) {
    if (d == n) {
        found = true;
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? '\n' : ' ');
        return;
    }
    for (int v = 1; v <= n; v++) {
        if (used[v]) continue;
        if (d > 0 && !isp[last + v]) continue;
        used[v] = true;
        ans[d] = v;
        dfs(d + 1, v);
        used[v] = false;
    }
}
int main() {
    cin >> n;
    for (int i = 2; i <= 2 * n; i++) {
        bool p = true;
        for (int j = 2; j * j <= i; j++)
            if (i % j == 0) { p = false; break; }
        isp[i] = p;
    }
    dfs(0, 0);
    if (!found) cout << "No\n";
    return 0;
}
