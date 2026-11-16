#include <bits/stdc++.h>
using namespace std;
int n;
long long W, best = 0;
struct Item { long long w, v; double r; } it[25];
bool cmp(const Item &a, const Item &b) { return a.r > b.r; }
void dfs(int i, long long cw, long long cv) {
    best = max(best, cv);
    if (i == n) return;
    if (cw + it[i].w <= W) dfs(i + 1, cw + it[i].w, cv + it[i].v);
    dfs(i + 1, cw, cv);
}
int main() {
    cin >> n >> W;
    for (int i = 0; i < n; i++) {
        cin >> it[i].w >> it[i].v;
        it[i].r = (double)it[i].v / it[i].w;
    }
    sort(it, it + n, cmp);
    dfs(0, 0, 0);
    cout << best << "\n";
    return 0;
}
