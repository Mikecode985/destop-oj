#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long target;
    cin >> n >> target;
    unordered_map<long long, int> pos;   // 值 → 第一次出现的下标
    for (int j = 1; j <= n; j++) {
        long long x;
        cin >> x;
        auto it = pos.find(target - x);  // 先查补数，再存自己
        if (it != pos.end()) {
            cout << it->second << " " << j << "\n";
            return 0;                    // 题目保证唯一解，找到就收工
        }
        if (pos.find(x) == pos.end()) pos[x] = j;  // 只记第一次出现
    }
    cout << -1 << "\n";
    return 0;
}
