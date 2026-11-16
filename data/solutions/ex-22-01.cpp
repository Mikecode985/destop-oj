#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
vector<int> g[MAXN];      // 邻接表：g[u] 里是 u 的所有邻居
int dist[MAXN];           // dist[i] 是从起点到 i 的边数，-1 表示没走到

// 从 start 出发遍历整棵树，返回离 start 最远的结点编号
int farthestFrom(int start, int n) {
    for (int i = 1; i <= n; i++) dist[i] = -1;   // 每趟都要清零，别用上一趟的旧值
    vector<int> stk;
    stk.push_back(start);
    dist[start] = 0;
    int best = start;                             // 目前最远的点
    while (!stk.empty()) {
        int u = stk.back();
        stk.pop_back();
        if (dist[u] > dist[best]) best = u;       // 边扫边更新最远点
        for (int v : g[u]) {
            if (dist[v] == -1) {                  // 没访问过才走，等价于不看父亲
                dist[v] = dist[u] + 1;
                stk.push_back(v);
            }
        }
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }
    int a = farthestFrom(1, n);      // 第一趟：从任意点找到直径的一端
    int b = farthestFrom(a, n);      // 第二趟：从这一端找到另一端
    cout << dist[b] << "\n";         // 第二趟后 dist 存的是到 a 的距离
    return 0;
}
