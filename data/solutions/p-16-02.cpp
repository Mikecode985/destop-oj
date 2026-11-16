#include <bits/stdc++.h>
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
