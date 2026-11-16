# -*- coding: utf-8 -*-
"""第 23～24 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-23-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    long long f[75];
    f[0] = 1;
    for (int i = 1; i <= n; i++) {
        f[i] = 0;
        for (int k = 1; k <= 3; k++)
            if (i - k >= 0) f[i] += f[i - k];
    }
    cout << f[n] << "\n";
    return 0;
}
'''

SOL["p-23-02"] = r'''#include <bits/stdc++.h>
using namespace std;
long long a[1005][1005], f[1005][1005];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= i; j++) cin >> a[i][j];
    for (int j = 1; j <= n; j++) f[n][j] = a[n][j];
    for (int i = n - 1; i >= 1; i--)
        for (int j = 1; j <= i; j++)
            f[i][j] = a[i][j] + max(f[i + 1][j], f[i + 1][j + 1]);
    cout << f[1][1] << "\n";
    int j = 1;
    for (int i = 1; i <= n; i++) {
        cout << j << (i == n ? '\n' : ' ');
        if (i == n) break;
        if (f[i + 1][j + 1] > f[i + 1][j]) j++;
    }
    return 0;
}
'''

SOL["p-23-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long best = 0, cur = 0, x;
    cin >> x;
    best = cur = x;
    for (int i = 1; i < n; i++) {
        cin >> x;
        cur = max(x, cur + x);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}
'''

SOL["p-23-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> d;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        auto it = upper_bound(d.begin(), d.end(), x);
        if (it == d.end()) d.push_back(x);
        else *it = x;
    }
    cout << d.size() << "\n";
    return 0;
}
'''

SOL["p-23-05"] = r'''#include <bits/stdc++.h>
using namespace std;
long long solve(const vector<long long> &a, int l, int r) {
    long long take = 0, skip = 0;
    for (int i = l; i <= r; i++) {
        long long nt = skip + a[i];
        long long ns = max(take, skip);
        take = nt;
        skip = ns;
    }
    return max(take, skip);
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    if (n == 1) { cout << a[0] << "\n"; return 0; }
    cout << max(solve(a, 0, n - 2), solve(a, 1, n - 1)) << "\n";
    return 0;
}
'''

SOL["p-24-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, W;
    cin >> n >> W;
    vector<char> ok(W + 1, 0);
    ok[0] = 1;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        for (int j = W; j >= v; j--)
            if (ok[j - v]) ok[j] = 1;
    }
    for (int j = W; j >= 0; j--)
        if (ok[j]) { cout << j << "\n"; return 0; }
    return 0;
}
'''

SOL["p-24-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, W;
    cin >> n >> W;
    vector<int> c(n);
    for (auto &x : c) cin >> x;
    const int INF = 1e9;
    vector<int> dp(W + 1, INF);
    dp[0] = 0;
    for (int j = 1; j <= W; j++)
        for (int i = 0; i < n; i++)
            if (j >= c[i] && dp[j - c[i]] + 1 < dp[j]) dp[j] = dp[j - c[i]] + 1;
    cout << (dp[W] >= INF ? -1 : dp[W]) << "\n";
    return 0;
}
'''

SOL["p-24-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W;
    cin >> n >> W;
    vector<vector<long long>> dp(W + 1, vector<long long>(2, 0));
    for (int g = 0; g < n; g++) {
        int k;
        cin >> k;
        for (int j = 0; j <= W; j++) dp[j][1] = dp[j][0];
        for (int t = 0; t < k; t++) {
            int w, v;
            cin >> w >> v;
            for (int j = W; j >= w; j--)
                dp[j][1] = max(dp[j][1], dp[j - w][0] + v);
        }
        for (int j = 0; j <= W; j++) dp[j][0] = dp[j][1];
    }
    long long ans = 0;
    for (int j = 0; j <= W; j++) ans = max(ans, dp[j][0]);
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-24-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, W;
    cin >> n >> W;
    const long long NEG = -(long long)4e18;
    vector<long long> dp(W + 1, NEG);
    dp[0] = 0;
    for (int i = 0; i < n; i++) {
        int w, v;
        cin >> w >> v;
        for (int j = W; j >= w; j--)
            if (dp[j - w] > NEG / 2) dp[j] = max(dp[j], dp[j - w] + v);
    }
    cout << (dp[W] <= NEG / 2 ? -1 : dp[W]) << "\n";
    return 0;
}
'''

SOL["p-24-05"] = r'''#include <bits/stdc++.h>
using namespace std;
long long dp[505][505];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W1, W2;
    cin >> n >> W1 >> W2;
    for (int i = 0; i < n; i++) {
        int w1, w2, v;
        cin >> w1 >> w2 >> v;
        for (int a = W1; a >= w1; a--)
            for (int b = W2; b >= w2; b--)
                dp[a][b] = max(dp[a][b], dp[a - w1][b - w2] + v);
    }
    cout << dp[W1][W2] << "\n";
    return 0;
}
'''

SOL["p-24-06"] = r'''#include <bits/stdc++.h>
using namespace std;
long long dp[505][505];
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, B, T;
    cin >> n >> B >> T;
    for (int i = 0; i < n; i++) {
        int c, t, v;
        cin >> c >> t >> v;
        for (int a = B; a >= c; a--)
            for (int b = T; b >= t; b--)
                dp[a][b] = max(dp[a][b], dp[a - c][b - t] + v);
    }
    cout << dp[B][T] << "\n";
    return 0;
}
'''
