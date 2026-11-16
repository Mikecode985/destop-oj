#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<pair<int, long long>>> g(n + 1);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
    auto far = [&](int s) {
        vector<long long> d(n + 1, -1);
        vector<int> st{s};
        d[s] = 0;
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            for (auto &e : g[u])
                if (d[e.first] == -1) { d[e.first] = d[u] + e.second; st.push_back(e.first); }
        }
        int best = 1;
        for (int i = 2; i <= n; i++)
            if (d[i] > d[best]) best = i;
        return make_pair(best, d[best]);
    };
    if (n == 1) { cout << 0 << "\n"; return 0; }
    int a = far(1).first;
    cout << far(a).second << "\n";
    return 0;
}
