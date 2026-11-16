#include <bits/stdc++.h>
using namespace std;
int n;
bool col[12], d1[24], d2[24];
int board[12];
bool dfs(int r) {
    if (r == n) return true;
    for (int c = 0; c < n; c++) {
        if (col[c] || d1[r + c] || d2[r - c + n]) continue;
        col[c] = d1[r + c] = d2[r - c + n] = true;
        board[r] = c;
        if (dfs(r + 1)) return true;
        col[c] = d1[r + c] = d2[r - c + n] = false;
    }
    return false;
}
int main() {
    cin >> n;
    if (!dfs(0)) { cout << "No\n"; return 0; }
    for (int r = 0; r < n; r++) {
        for (int c = 0; c < n; c++) cout << (board[r] == c ? 'Q' : '.');
        cout << "\n";
    }
    return 0;
}
