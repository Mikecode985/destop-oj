#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1005;
int a[MAXN], b[MAXN], c[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s, t;
    cin >> s >> t;
    int n = (int)s.size(), m = (int)t.size();
    for (int i = 1; i <= n; i++) a[i] = s[n - i] - '0';   // 低位放前面
    for (int i = 1; i <= m; i++) b[i] = t[m - i] - '0';

    int len = max(n, m);
    int carry = 0;
    for (int i = 1; i <= len; i++) {
        int sum = a[i] + b[i] + carry;
        c[i] = sum % 10;
        carry = sum / 10;
    }
    if (carry > 0) c[++len] = carry;   // 最高位还有进位

    for (int i = len; i >= 1; i--) cout << c[i];
    cout << "\n";
    return 0;
}
