#include <bits/stdc++.h>
using namespace std;
int n, cnt;
bool col[20], d1[40], d2[40];
void dfs(int r) {
    if (r == n) { cnt++; return; }
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r + c] || d2[r - c + n]) continue;
        col[c] = d1[r + c] = d2[r - c + n] = true;
        dfs(r + 1);
        col[c] = d1[r + c] = d2[r - c + n] = false;
    }
}
int main() {
    cin >> n;
    dfs(0);
    cout << cnt << "\n";
    return 0;
}
