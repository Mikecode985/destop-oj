#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long k;
    cin >> n >> k;

    map<long long, long long> cnt;   // 前缀和 -> 出现次数
    cnt[0] = 1;                      // 空的前缀，子段从第 1 个数开始时会用到

    long long prefix = 0, ans = 0;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        prefix += x;
        // 前面出现过多少次 prefix - k，就有多少个以 i 结尾、和为 k 的子段
        auto it = cnt.find(prefix - k);
        if (it != cnt.end()) ans += it->second;
        cnt[prefix]++;
    }

    cout << ans << "\n";
    return 0;
}
