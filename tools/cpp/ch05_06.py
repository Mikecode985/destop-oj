# -*- coding: utf-8 -*-
"""第 5～6 章习题的 C++ 参考答案"""

SOL = {}

SOL["p-05-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int cur = 1;
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        int t;
        cin >> t;
        ans += abs(t - cur) + 1;
        cur = t;
    }
    cout << ans << " " << cur << "\n";
    return 0;
}
'''

SOL["p-05-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    long long t;
    cin >> t;
    int r = (int)(t % 90);
    if (r < 30) cout << "绿灯\n";
    else if (r < 33) cout << "黄灯\n";
    else cout << "红灯\n";
    return 0;
}
'''

SOL["p-05-03"] = r'''#include <bits/stdc++.h>
using namespace std;
bool leap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }
long long days(int y, int m, int d) {
    long long s = 0;
    for (int i = 1; i < y; i++) s += leap(i) ? 366 : 365;
    int md[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    for (int i = 1; i < m; i++) s += md[i - 1] + (i == 2 && leap(y) ? 1 : 0);
    s += d - 1;
    return s;
}
int main() {
    int y1, m1, d1, y2, m2, d2;
    cin >> y1 >> m1 >> d1 >> y2 >> m2 >> d2;
    long long a = days(y1, m1, d1), b = days(y2, m2, d2);
    cout << llabs(a - b) << "\n";
    return 0;
}
'''

SOL["p-05-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<vector<int>> a(n, vector<int>(n, 0));
    int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
    int x = 0, y = 0, d = 0;
    for (int k = 1; k <= n * n; k++) {
        a[x][y] = k;
        int nx = x + dx[d], ny = y + dy[d];
        if (nx < 0 || nx >= n || ny < 0 || ny >= n || a[nx][ny]) {
            d = (d + 1) % 4;
            nx = x + dx[d];
            ny = y + dy[d];
        }
        x = nx;
        y = ny;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) cout << a[i][j] << (j == n - 1 ? '\n' : ' ');
    }
    return 0;
}
'''

SOL["p-05-05"] = r'''#include <bits/stdc++.h>
using namespace std;
long long fdiv(long long a, long long b) {
    long long q = a / b;
    if (a % b != 0 && ((a < 0) != (b < 0))) q--;
    return q;
}
int main() {
    string s;
    getline(cin, s);
    vector<long long> num;
    vector<char> op;
    string t;
    for (char c : s + "+") {
        if (c >= '0' && c <= '9') t += c;
        else if (c == '+' || c == '-' || c == '*' || c == '/') {
            if (!t.empty()) { num.push_back(stoll(t)); t.clear(); }
            op.push_back(c);
        }
    }
    vector<long long> a;
    vector<char> b;
    a.push_back(num[0]);
    for (size_t i = 0; i + 1 < op.size(); i++) {
        if (op[i] == '*') a.back() = a.back() * num[i + 1];
        else if (op[i] == '/') a.back() = fdiv(a.back(), num[i + 1]);
        else { b.push_back(op[i]); a.push_back(num[i + 1]); }
    }
    long long ans = a[0];
    for (size_t i = 0; i < b.size(); i++) ans = b[i] == '+' ? ans + a[i + 1] : ans - a[i + 1];
    cout << ans << "\n";
    return 0;
}
'''

SOL["p-06-01"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int cnt = 0;
    for (int x = 1; x <= 100; x++)
        for (int y = 1; y <= 100; y++) {
            int z = 100 - x - y;
            if (z < 1 || z % 3 != 0) continue;
            if (5 * x + 3 * y + z / 3 == 100) {
                cout << x << " " << y << " " << z << "\n";
                cnt++;
            }
        }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["p-06-02"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    for (long long mask = 0; mask < (1LL << n); mask++) {
        long long s = 0;
        for (int i = 0; i < n; i++)
            if (mask >> i & 1) s += a[i];
        if (s == S) { cout << "YES\n"; return 0; }
    }
    cout << "NO\n";
    return 0;
}
'''

SOL["p-06-03"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    long long n;
    cin >> n;
    for (long long a = 0; a * a <= n; a++)
        for (long long b = a; a * a + b * b <= n; b++)
            for (long long c = b; a * a + b * b + c * c <= n; c++) {
                long long r = n - a * a - b * b - c * c;
                long long d = (long long)sqrt((double)r);
                while (d * d > r) d--;
                while ((d + 1) * (d + 1) <= r) d++;
                if (d >= c && d * d == r) {
                    cout << a << " " << b << " " << c << " " << d << "\n";
                    return 0;
                }
            }
    cout << -1 << "\n";
    return 0;
}
'''

SOL["p-06-04"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        int s = 0, x = i;
        while (x) { s += x % 10; x /= 10; }
        if (s % 9 == 0) cnt++;
    }
    cout << cnt << "\n";
    return 0;
}
'''

SOL["p-06-05"] = r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int half = n / 2;
    vector<long long> L{0}, R{0};
    for (int i = 0; i < half; i++) {
        int sz = L.size();
        for (int j = 0; j < sz; j++) L.push_back(L[j] + a[i]);
    }
    for (int i = half; i < n; i++) {
        int sz = R.size();
        for (int j = 0; j < sz; j++) R.push_back(R[j] + a[i]);
    }
    sort(L.begin(), L.end());
    long long ans = 0;
    for (long long s : R)
        ans += upper_bound(L.begin(), L.end(), S - s) - lower_bound(L.begin(), L.end(), S - s);
    cout << ans << "\n";
    return 0;
}
'''
