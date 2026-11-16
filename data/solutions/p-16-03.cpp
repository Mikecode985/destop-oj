#include <bits/stdc++.h>
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
