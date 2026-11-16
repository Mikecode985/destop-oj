#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];
int indeg[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;                   // u 是 v 的先修课
        g[u].push_back(v);
        indeg[v]++;                      // v 多了一门前置课
    }
    queue<int> q;
    for (int i = 1; i <= n; i++)
        if (indeg[i] == 0) q.push(i);    // 没有先修课的，先排
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);              // 出队顺序就是拓扑序
        for (int v : g[u]) {
            if (--indeg[v] == 0) q.push(v);   // 先修课都排完了
        }
    }
    if ((int)order.size() < n) {         // 还有点在环里，排不出来
        cout << "No\n";
        return 0;
    }
    for (int i = 0; i < n; i++) {
        if (i) cout << " ";
        cout << order[i];
    }
    cout << "\n";
    return 0;
}
