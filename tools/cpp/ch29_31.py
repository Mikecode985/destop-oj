# -*- coding: utf-8 -*-
"""第 29～31 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-29-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<char> comp(n + 1, 0);
    vector<int> pr;
    pr.reserve(n / 10);
    for (int i = 2; i <= n; i++) {
        if (!comp[i]) pr.push_back(i);
        for (int p : pr) {
            if ((long long)i * p > n) break;
            comp[i * p] = 1;
            if (i % p == 0) break;
        }
    }
    cout << pr.size() << "\n";
    return 0;
}
'''

SOL["p-29-04"] = r'''#include <bits/stdc++.h>
using namespace std;
long long pw(long long a, long long b, long long m) {
    long long r = 1 % m;
    a %= m;
    while (b > 0) {
        if (b & 1) r = (__int128)r * a % m;
        a = (__int128)a * a % m;
        b >>= 1;
    }
    return r;
}
int main() {
    long long a, b, m;
    cin >> a >> b >> m;
    cout << pw(a, b, m) << "\n" << pw(a, m - 2, m) << "\n";
    return 0;
}
'''

SOL["p-29-05"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
struct Mat { long long a[2][2]; };
Mat mul(const Mat &x, const Mat &y) {
    Mat z{};
    for (int i = 0; i < 2; i++)
        for (int k = 0; k < 2; k++) {
            if (!x.a[i][k]) continue;
            for (int j = 0; j < 2; j++)
                z.a[i][j] = (z.a[i][j] + (__int128)x.a[i][k] * y.a[k][j]) % MOD;
        }
    return z;
}
int main() {
    long long n;
    cin >> n;
    if (n == 0) { cout << 0 << "\n"; return 0; }
    Mat r{{{1, 0}, {0, 1}}}, b{{{1, 1}, {1, 0}}};
    long long e = n - 1;
    while (e > 0) {
        if (e & 1) r = mul(r, b);
        b = mul(b, b);
        e >>= 1;
    }
    // [F(n), F(n-1)] = b^(n-1) * [F(1), F(0)]
    cout << r.a[0][0] % MOD << "\n";
    return 0;
}
'''

SOL["p-29-06"] = r'''#include <bits/stdc++.h>
using namespace std;
long long exgcd(long long a, long long b, long long &x, long long &y) {
    if (!b) { x = 1; y = 0; return a; }
    long long d = exgcd(b, a % b, y, x);
    y -= a / b * x;
    return d;
}
int main() {
    int k;
    cin >> k;
    vector<long long> a(k), m(k);
    long long M = 1;
    for (int i = 0; i < k; i++) {
        cin >> a[i] >> m[i];
        M *= m[i];
    }
    long long ans = 0;
    for (int i = 0; i < k; i++) {
        long long Mi = M / m[i], x, y;
        exgcd(Mi, m[i], x, y);
        x = (x % m[i] + m[i]) % m[i];
        ans = (ans + (__int128)a[i] * Mi % M * x) % M;
    }
    cout << ans % M << "\n";
    return 0;
}
'''

SOL["p-30-02"] = r'''#include <bits/stdc++.h>
using namespace std;
long long pw(long long a, long long b, long long m) {
    long long r = 1 % m;
    a %= m;
    while (b) {
        if (b & 1) r = (__int128)r * a % m;
        a = (__int128)a * a % m;
        b >>= 1;
    }
    return r;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    long long n, m, p;
    while (q--) {
        cin >> n >> m >> p;
        if (m > n) { cout << 0 << "\n"; continue; }
        long long cur = 1, fm = 1, fnm = 1;
        for (long long i = 1; i <= n; i++) {
            cur = (__int128)cur * i % p;
            if (i == m) fm = cur;
            if (i == n - m) fnm = cur;
        }
        long long ans = (__int128)cur * pw((__int128)fm * fnm % p, p - 2, p) % p;
        cout << ans << "\n";
    }
    return 0;
}
'''

SOL["p-30-03"] = r'''#include <bits/stdc++.h>
using namespace std;
long long cnt(long long n, long long d) { return n / d; }
int main() {
    long long n;
    cin >> n;
    long long ans = cnt(n, 2) + cnt(n, 3) + cnt(n, 5)
                  - cnt(n, 6) - cnt(n, 10) - cnt(n, 15)
                  + cnt(n, 30);
    cout << n - ans << "\n";
    return 0;
}
'''

SOL["p-30-04"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long pw(long long a, long long b) {
    long long r = 1;
    a %= MOD;
    while (b) {
        if (b & 1) r = (__int128)r * a % MOD;
        a = (__int128)a * a % MOD;
        b >>= 1;
    }
    return r;
}
int main() {
    int n;
    cin >> n;
    if (n == 0) { cout << 1 << "\n"; return 0; }
    long long f = 1;
    for (int i = 1; i <= 2 * n; i++) f = (__int128)f * i % MOD;
    long long g = 1;
    for (int i = 1; i <= n; i++) g = (__int128)g * i % MOD;
    long long h = 1;
    for (int i = 1; i <= n + 1; i++) h = (__int128)h * i % MOD;
    long long g2 = (__int128)g * g % MOD;
    long long den = g2 * (n + 1) % MOD;
    long long ans = (long long)((__int128)f * pw(den, MOD - 2) % MOD);
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-30-05"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long D[100005];
int main() {
    int n;
    cin >> n;
    D[0] = 1;
    if (n >= 1) D[1] = 0;
    for (int i = 2; i <= n; i++) D[i] = (i - 1) * ((D[i - 1] + D[i - 2]) % MOD) % MOD;
    cout << D[n] % MOD << "\n";
    return 0;
}
'''

SOL["p-31-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    unsigned long long n;
    cin >> n;
    cout << __builtin_popcountll(n) << "\n";
    return 0;
}
'''

SOL["p-31-03"] = r'''#include <bits/stdc++.h>
using namespace std;
string sub(const string &a, const string &b) {
    string r;
    int i = a.size() - 1, j = b.size() - 1, borrow = 0;
    while (i >= 0) {
        int d = (a[i] - '0') - borrow - (j >= 0 ? b[j] - '0' : 0);
        if (d < 0) { d += 10; borrow = 1; } else borrow = 0;
        r.push_back('0' + d);
        i--;
        j--;
    }
    while (r.size() > 1 && r.back() == '0') r.pop_back();
    reverse(r.begin(), r.end());
    return r;
}
int main() {
    string a, b;
    cin >> a >> b;
    // 去掉前导零
    while (a.size() > 1 && a[0] == '0') a.erase(a.begin());
    while (b.size() > 1 && b[0] == '0') b.erase(b.begin());
    cout << sub(a, b) << "\n";
    return 0;
}
'''

SOL["p-31-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string a;
    long long b;
    cin >> a >> b;
    vector<int> q;
    long long rem = 0;
    for (char c : a) {
        rem = rem * 10 + (c - '0');
        q.push_back(rem / b);
        rem %= b;
    }
    int i = 0;
    while (i < (int)q.size() - 1 && q[i] == 0) i++;
    for (; i < (int)q.size(); i++) cout << q[i];
    cout << "\n" << rem << "\n";
    return 0;
}
'''

SOL["p-31-05"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    vector<int> d{0};
    for (char c : s) {
        int carry = c - '0';
        for (int i = 0; i < (int)d.size(); i++) {
            int v = d[i] * 2 + carry;
            d[i] = v % 10;
            carry = v / 10;
        }
        while (carry) { d.push_back(carry % 10); carry /= 10; }
    }
    while (d.size() > 1 && d.back() == 0) d.pop_back();
    for (int i = d.size() - 1; i >= 0; i--) cout << d[i];
    cout << "\n";
    return 0;
}
'''
