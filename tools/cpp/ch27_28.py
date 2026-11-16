# -*- coding: utf-8 -*-
"""第 27～28 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-27-01"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    int n, m;
    cin >> n >> m;
    vector<long long> f(m + 1, 0);
    f[1] = 1;
    for (int i = 1; i <= n; i++)
        for (int j = 2; j <= m; j++) {
            f[j] += f[j - 1];
            if (f[j] >= MOD) f[j] -= MOD;
        }
    cout << f[m] % MOD << "\n";
    return 0;
}
'''

SOL["p-27-02"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
int main() {
    int n;
    cin >> n;
    vector<long long> dp(n + 1, 0);
    dp[0] = 1;
    long long S = 1;  // S[i] = dp[i-1] + ... + dp[i-8]
    for (int i = 1; i <= n; i++) {
        dp[i] = S % MOD;
        S += dp[i];
        if (i - 8 >= 0) S -= dp[i - 8];
        S %= MOD;
        if (S < 0) S += MOD;
    }
    cout << dp[n] % MOD << "\n";
    return 0;
}
'''

SOL["p-27-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pre[i] = pre[i - 1] + x;
    }
    deque<int> dq;
    dq.push_back(0);
    long long ans = LLONG_MIN;
    for (int i = 1; i <= n; i++) {
        while (!dq.empty() && dq.front() < i - k) dq.pop_front();
        ans = max(ans, pre[i] - pre[dq.front()]);
        while (!dq.empty() && pre[dq.back()] >= pre[i]) dq.pop_back();
        dq.push_back(i);
    }
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-28-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> w(n);
    for (auto &s : w) cin >> s;
    sort(w.begin(), w.end());
    int q;
    cin >> q;
    while (q--) {
        string t;
        cin >> t;
        auto r = equal_range(w.begin(), w.end(), t);
        cout << r.second - r.first << "\n";
    }
    return 0;
}
'''

SOL["p-28-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> w(n);
    for (auto &s : w) cin >> s;
    sort(w.begin(), w.end());
    int q;
    cin >> q;
    while (q--) {
        string p;
        cin >> p;
        string hi = p;
        hi.back() = hi.back() + 1;  // 比所有以 p 开头的串都大
        cout << lower_bound(w.begin(), w.end(), hi) - lower_bound(w.begin(), w.end(), p) << "\n";
    }
    return 0;
}
'''

SOL["p-28-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    int n = s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    int p = n - pi[n - 1];
    cout << (n % p == 0 ? p : n) << "\n";
    return 0;
}
'''

SOL["p-28-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> w(n);
    for (auto &s : w) cin >> s;
    sort(w.begin(), w.end());
    int q;
    cin >> q;
    while (q--) {
        string p;
        cin >> p;
        auto it = lower_bound(w.begin(), w.end(), p);
        if (it == w.end() || it->compare(0, p.size(), p) != 0) cout << "NONE\n";
        else cout << *it << "\n";
    }
    return 0;
}
'''

SOL["p-28-05"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s, p;
    cin >> s >> p;
    int m = p.size();
    vector<int> pi(m, 0);
    for (int i = 1; i < m; i++) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j]) j = pi[j - 1];
        if (p[i] == p[j]) j++;
        pi[i] = j;
    }
    int j = 0;
    long long cnt = 0;
    for (char c : s) {
        while (j > 0 && c != p[j]) j = pi[j - 1];
        if (c == p[j]) j++;
        if (j == m) { cnt++; j = pi[j - 1]; }
    }
    cout << cnt << "\n";
    return 0;
}
'''
