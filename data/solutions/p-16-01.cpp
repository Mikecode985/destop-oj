#include <bits/stdc++.h>
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
