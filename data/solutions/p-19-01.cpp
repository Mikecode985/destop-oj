#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> deg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        deg[u]++;
        deg[v]++;
    }
    int best = 1;
    for (int i = 1; i <= n; i++) {
        cout << deg[i] << "\n";
        if (deg[i] > deg[best]) best = i;
    }
    cout << best << "\n";
    return 0;
}
