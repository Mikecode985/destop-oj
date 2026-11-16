#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    int low = n & (-n);              // lowbit：最低位的 1
    int cnt = 0;
    for (int x = n; x > 0; x >>= 1) cnt += (x & 1);
    int setBit = n | (1 << k);       // 第 k 位置 1
    int removeLow = n & (n - 1);     // 去掉最低位的 1

    cout << low << "\n" << cnt << "\n" << setBit << "\n" << removeLow << "\n";
    return 0;
}
