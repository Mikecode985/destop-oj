#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000005;
char s[MAXN], p[MAXN];   // 从下标 1 开始存
int nxt[MAXN];           // nxt[i]：p[1..i] 的最长相等真前后缀长度

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> (s + 1) >> (p + 1);
    int n = (int)strlen(s + 1), m = (int)strlen(p + 1);

    nxt[1] = 0;
    for (int i = 2, j = 0; i <= m; i++) {
        while (j > 0 && p[i] != p[j + 1]) j = nxt[j];
        if (p[i] == p[j + 1]) j++;
        nxt[i] = j;
    }

    int cnt = 0;
    for (int i = 1, j = 0; i <= n; i++) {
        while (j > 0 && s[i] != p[j + 1]) j = nxt[j];
        if (s[i] == p[j + 1]) j++;
        if (j == m) {
            cnt++;           // 找到一次完整匹配
            j = nxt[j];      // 继续找下一处，允许前后重叠
        }
    }
    cout << cnt << "\n";
    return 0;
}
