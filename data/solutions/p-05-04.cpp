#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<vector<int>> a(n, vector<int>(n, 0));
    int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
    int x = 0, y = 0, d = 0;
    for (int k = 1; k <= n * n; k++) {
        a[x][y] = k;
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= n || ny < 0 || ny >= n || a[nx][ny]) {
            d = (d + 1) % 4;
            nx = x + dx[d];
            ny = y + dy[d];
        }
        x = nx;
        y = ny;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) cout << a[i][j] << (j == n - 1 ? '\n' : ' ');
    }
    return 0;
}
