# -*- coding: utf-8 -*-
"""第 15～16 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-15-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    unordered_map<long long, int> cnt;
    for (auto &x : a) {
        cin >> x;
        cnt[x]++;
    }
    for (auto x : a)
        if (cnt[x] == 1) { cout << x << "\n"; return 0; }
    cout << -1 << "\n";
    return 0;
}
'''

SOL["p-15-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long target;
    cin >> n >> target;
    set<long long> s;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        s.insert(x);
    }
    bool any = false;
    for (auto x : s) {
        long long y = target - x;
        if (y > x && s.count(y)) {
            cout << x << " " << y << "\n";
            any = true;
        }
    }
    if (!any) cout << "No\n";
    return 0;
}
'''

SOL["p-15-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n), b;
    for (auto &x : a) cin >> x;
    b = a;
    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());
    for (int i = 0; i < n; i++) {
        int r = lower_bound(b.begin(), b.end(), a[i]) - b.begin() + 1;
        cout << r << (i == n - 1 ? '\n' : ' ');
    }
    return 0;
}
'''

SOL["p-16-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    priority_queue<long long, vector<long long>, greater<long long>> q;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        if ((int)q.size() < k) q.push(x);
        else if (x > q.top()) { q.pop(); q.push(x); }
    }
    cout << q.top() << "\n";
    return 0;
}
'''

SOL["p-16-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<long long, long long>> a(n);
    for (auto &p : a) cin >> p.second >> p.first;  // (截止, 耗时)
    sort(a.begin(), a.end());
    priority_queue<long long> q;
    long long t = 0;
    for (auto &p : a) {
        q.push(p.second);
        t += p.second;
        if (t > p.first) {
            t -= q.top();
            q.pop();
        }
    }
    cout << q.size() << "\n";
    return 0;
}
'''

SOL["p-16-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    priority_queue<long long, vector<long long>, greater<long long>> q;
    set<long long> seen;
    q.push(1);
    seen.insert(1);
    long long x = 1;
    for (int i = 0; i < n; i++) {
        x = q.top();
        q.pop();
        for (long long m : {2LL, 3LL, 5LL}) {
            long long y = x * m;
            if (seen.insert(y).second) q.push(y);
        }
    }
    cout << x << "\n";
    return 0;
}
'''

SOL["p-16-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    priority_queue<long long> L;                            // 大根堆，存较小的一半
    priority_queue<long long, vector<long long>, greater<long long>> R;  // 小根堆，存较大的一半
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        if (L.empty() || x <= L.top()) L.push(x);
        else R.push(x);
        if ((int)L.size() > (int)R.size() + 1) { R.push(L.top()); L.pop(); }
        if ((int)L.size() < (int)R.size()) { L.push(R.top()); R.pop(); }
        long long med;
        if ((i + 1) % 2 == 1) med = L.top();
        else med = max(L.top(), R.top());
        cout << med << "\n";
    }
    return 0;
}
'''
