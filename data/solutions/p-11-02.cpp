#include <bits/stdc++.h>
using namespace std;
int n, k;
vector<int> cur;
void dfs(int start) {
    if ((int)cur.size() == k) {
        for (int i = 0; i < k; i++) cout << cur[i] << (i == k - 1 ? '\n' : ' ');
        return;
    }
    for (int v = start; v <= n; v++) {
        if (n - v + 1 < k - (int)cur.size()) break;
        cur.push_back(v);
        dfs(v + 1);
        cur.pop_back();
    }
}
int main() {
    cin >> n >> k;
    dfs(1);
    return 0;
}
