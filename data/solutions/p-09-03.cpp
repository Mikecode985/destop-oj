#include <bits/stdc++.h>
using namespace std;
int n, a[10];
bool used[10];
int ans[10];
void dfs(int d) {
    if (d == n) {
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? '\n' : ' ');
        return;
    }
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        used[i] = true;
        ans[d] = a[i];
        dfs(d + 1);
        used[i] = false;
    }
}
int main() {
    cin >> n;
    for (int i = 0; i < n; i++) cin >> a[i];
    sort(a, a + n);
    dfs(0);
    return 0;
}
