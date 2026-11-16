#include <bits/stdc++.h>
using namespace std;

const int MAXNODE = 200005;
int ch[MAXNODE][26];   // ch[u][c]：结点 u 经过字母 c 走到的结点编号，0 表示没有
int pass[MAXNODE];     // pass[u]：有多少个词经过结点 u
int tot = 0;           // 已经用掉的结点数，根固定是 0

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    while (n--) {
        string w;
        cin >> w;
        int u = 0;
        for (char c : w) {
            int k = c - 'a';
            if (ch[u][k] == 0) ch[u][k] = ++tot;   // 没有这条路就新建一个结点
            u = ch[u][k];
            pass[u]++;                            // 这个词经过了 u
        }
    }

    int q;
    cin >> q;
    while (q--) {
        string s;
        cin >> s;
        int u = 0;
        bool ok = true;
        for (char c : s) {
            int k = c - 'a';
            if (ch[u][k] == 0) { ok = false; break; }
            u = ch[u][k];
        }
        cout << (ok ? pass[u] : 0) << "\n";
    }
    return 0;
}
