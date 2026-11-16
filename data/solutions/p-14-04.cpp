#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    deque<int> q;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
        while (!q.empty() && a[q.back()] >= a[i]) q.pop_back();
        q.push_back(i);
        while (q.front() <= i - k) q.pop_front();
        if (i >= k - 1) cout << a[q.front()] << (i == n - 1 ? '\n' : ' ');
    }
    return 0;
}
