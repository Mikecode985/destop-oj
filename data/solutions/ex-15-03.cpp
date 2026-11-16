#include <bits/stdc++.h>
using namespace std;
using ull = unsigned long long;

const int MAXN = 100005;
ull h[MAXN], pw[MAXN];           // h：前缀哈希；pw：base 的幂
const ull BASE = 131;            // 比字符集大的质数，冲突概率低

ull getHash(int l, int r) {      // 子串 s[l..r] 的哈希（1-indexed）
    return h[r] - h[l - 1] * pw[r - l + 1];   // 无符号溢出 = 对 2^64 取模
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    int n = (int)s.size();
    pw[0] = 1;
    for (int i = 1; i <= n; i++) {
        h[i] = h[i - 1] * BASE + (ull)s[i - 1];  // 逐位"进位"求前缀哈希
        pw[i] = pw[i - 1] * BASE;
    }
    int q;
    cin >> q;
    while (q--) {
        int l1, r1, l2, r2;
        cin >> l1 >> r1 >> l2 >> r2;
        if (getHash(l1, r1) == getHash(l2, r2)) cout << "YES\n";
        else cout << "NO\n";
    }
    return 0;
}
