#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    while (cin >> n) {           // 读不到 n 就退出：这就是"读到文件结尾"
        long long sum = 0;       // 每组重新清零，千万别写到循环外面
        for (int i = 1; i <= n; i++) {
            long long x;
            cin >> x;
            sum += x;
        }
        cout << sum << "\n";
    }
    return 0;
}
