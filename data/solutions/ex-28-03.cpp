#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
const int MOD1 = 1000000007, MOD2 = 998244353;
const int BASE = 131;
long long pw1[MAXN], pw2[MAXN];
long long hf1[MAXN], hf2[MAXN];   // 正向哈希
long long hr1[MAXN], hr2[MAXN];   // 反向哈希

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();
    string t(s.rbegin(), s.rend());    // 反转串

    pw1[0] = pw2[0] = 1;
    for (int i = 1; i <= n; i++) {
        pw1[i] = pw1[i - 1] * BASE % MOD1;
        pw2[i] = pw2[i - 1] * BASE % MOD2;
    }
    for (int i = 1; i <= n; i++) {
        hf1[i] = (hf1[i - 1] * BASE + s[i - 1]) % MOD1;
        hf2[i] = (hf2[i - 1] * BASE + s[i - 1]) % MOD2;
        hr1[i] = (hr1[i - 1] * BASE + t[i - 1]) % MOD1;
        hr2[i] = (hr2[i - 1] * BASE + t[i - 1]) % MOD2;
    }

    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        int L = n - r + 1, R = n - l + 1;   // 反转串里对应的区间
        int len = r - l + 1;
        long long a1 = (hf1[r] - hf1[l - 1] * pw1[len] % MOD1 + MOD1) % MOD1;
        long long a2 = (hf2[r] - hf2[l - 1] * pw2[len] % MOD2 + MOD2) % MOD2;
        long long b1 = (hr1[R] - hr1[L - 1] * pw1[len] % MOD1 + MOD1) % MOD1;
        long long b2 = (hr2[R] - hr2[L - 1] * pw2[len] % MOD2 + MOD2) % MOD2;
        cout << (a1 == b1 && a2 == b2 ? "YES" : "NO") << "\n";
    }
    return 0;
}
