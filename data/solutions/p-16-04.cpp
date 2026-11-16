#include <bits/stdc++.h>
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
