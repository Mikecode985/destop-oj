# -*- coding: utf-8 -*-
"""第 9～10 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-09-01"] = r'''#include <bits/stdc++.h>
using namespace std;
long long f(int n) {
    if (n <= 1) return 1;
    return n * f(n - 1);
}
int main() {
    int n;
    cin >> n;
    cout << f(n) << "\n";
    return 0;
}
'''

SOL["p-09-02"] = r'''#include <bits/stdc++.h>
using namespace std;
const long long MOD = 1000000007LL;
long long pw(long long a, long long n) {
    if (n == 0) return 1;
    long long t = pw(a, n / 2);
    t = t * t % MOD;
    if (n % 2) t = t * (a % MOD) % MOD;
    return t;
}
int main() {
    long long a, n;
    cin >> a >> n;
    cout << pw(a, n) << "\n";
    return 0;
}
'''

SOL["p-09-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int n, a[10];
bool used[10];
int ans[10];
void dfs(int d) {
    if (d == n) {
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? '\n' : ' ');
        return;
    }
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        used[i] = true;
        ans[d] = a[i];
        dfs(d + 1);
        used[i] = false;
    }
}
int main() {
    cin >> n;
    for (int i = 0; i < n; i++) cin >> a[i];
    sort(a, a + n);
    dfs(0);
    return 0;
}
'''

SOL["p-10-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<long long> a(n), b(m);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    int i = 0, j = 0;
    vector<long long> c;
    c.reserve(n + m);
    while (i < n && j < m) {
        if (a[i] <= b[j]) c.push_back(a[i++]);
        else c.push_back(b[j++]);
    }
    while (i < n) c.push_back(a[i++]);
    while (j < m) c.push_back(b[j++]);
    for (size_t k = 0; k < c.size(); k++) cout << c[k] << (k + 1 == c.size() ? '\n' : ' ');
    return 0;
}
'''

SOL["p-10-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int n;
vector<int> a, tmp;
long long inv, eq;
void msort(int l, int r) {
    if (l >= r) return;
    int mid = (l + r) / 2;
    msort(l, mid);
    msort(mid + 1, r);
    int i = l, j = mid + 1, k = l;
    while (i <= mid && j <= r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else { inv += mid - i + 1; tmp[k++] = a[j++]; }
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int t = l; t <= r; t++) a[t] = tmp[t];
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    a.resize(n);
    tmp.resize(n);
    for (auto &x : a) cin >> x;
    msort(0, n - 1);
    // 相等对：排序后每组相同元素两两配对
    int i = 0;
    while (i < n) {
        int j = i;
        while (j + 1 < n && a[j + 1] == a[i]) j++;
        long long c = j - i + 1;
        eq += c * (c - 1) / 2;
        i = j + 1;
    }
    long long all = (long long)n * (n - 1) / 2;
    cout << all - inv - eq << "\n";
    return 0;
}
'''

SOL["p-10-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    nth_element(a.begin(), a.begin() + (n - k), a.end());
    cout << a[n - k] << "\n";
    return 0;
}
'''
