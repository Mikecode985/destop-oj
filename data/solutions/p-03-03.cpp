#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> a(n, vector<int>(m));
    for (int i = 0; i < n; i++) {
        long long s = 0;
        for (int j = 0; j < m; j++) {
            cin >> a[i][j];
            s += a[i][j];
        }
        cout << s << "\n";
    }
    return 0;
}
