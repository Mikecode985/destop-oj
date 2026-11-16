#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 1; i < n; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    auto far = [&](int s) {
        vector<long long> d(n + 1, -1);
        deque<int> q;
        d[s] = 0;
        q.push_back(s);
        int best = s;
        while (!q.empty()) {
            int u = q.front();
            q.pop_front();
            if (d[u] > d[best]) best = u;
            for (auto [v, w] : g[u])
                if (d[v] == -1) { d[v] = d[u] + w; q.push_back(v); }
        }
        return make_pair(best, d[best]);
    };
    int a = far(1).first;
    cout << far(a).second << "\n";
    return 0;
}
