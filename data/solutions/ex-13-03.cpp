#include <bits/stdc++.h>
using namespace std;

int a[10][10];
bool row[10][10], col[10][10], box[10][10];

int boxId(int r, int c) {                    // 3×3 宫编号 1..9
    return (r - 1) / 3 * 3 + (c - 1) / 3 + 1;
}

bool solve(int pos) {                        // pos：0..80，按行优先扫描
    if (pos == 81) return true;              // 81 格全部填完
    int r = pos / 9 + 1, c = pos % 9 + 1;
    if (a[r][c] != 0) return solve(pos + 1); // 题目给的数，直接下一格
    for (int v = 1; v <= 9; v++) {
        int b = boxId(r, c);
        if (row[r][v] || col[c][v] || box[b][v]) continue;  // 三个条件都不许
        a[r][c] = v;                          // 做选择
        row[r][v] = col[c][v] = box[b][v] = true;
        if (solve(pos + 1)) return true;      // 一旦找到解就收工
        a[r][c] = 0;                          // 撤销选择
        row[r][v] = col[c][v] = box[b][v] = false;
    }
    return false;                             // 1～9 都放不了，这格无解
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    for (int i = 1; i <= 9; i++) {
        string line;
        cin >> line;                          // 读一整行 9 个字符
        for (int j = 1; j <= 9; j++) {
            int v = line[j - 1] - '0';
            a[i][j] = v;
            if (v != 0) {                     // 题目给的数，记进三个标记数组
                int b = boxId(i, j);
                row[i][v] = col[j][v] = box[b][v] = true;
            }
        }
    }
    solve(0);
    for (int i = 1; i <= 9; i++) {
        for (int j = 1; j <= 9; j++) {
            if (j > 1) cout << " ";
            cout << a[i][j];
        }
        cout << "\n";
    }
    return 0;
}
