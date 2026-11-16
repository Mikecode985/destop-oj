#include <bits/stdc++.h>
using namespace std;

const int MAXN = 2005;
int a[MAXN], b[MAXN], c[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    cin >> s >> t;
    int n = (int)s.size(), m = (int)t.size();
    for (int i = 1; i <= n; i++) a[i] = s[n - i] - '0';
    for (int i = 1; i <= m; i++) b[i] = t[m - i] - '0';

    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            c[i + j - 1] += a[i] * b[j];   // 先累加，暂不进位

    int len = n + m;
    for (int i = 1; i < len; i++) {        // 从低位到高位统一进位
        c[i + 1] += c[i] / 10;
        c[i] %= 10;
    }
    while (len > 1 && c[len] == 0) len--;  // 去掉前导零

    for (int i = len; i >= 1; i--) cout << c[i];
    cout << "\n";
    return 0;
}
