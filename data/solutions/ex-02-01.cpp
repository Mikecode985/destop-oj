#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;   // 多开 5 个，给写错的下标留余量
int a[MAXN];               // 全局数组：空间大，而且自动清零

int main() {
    ios::sync_with_stdio(false);   // 关掉与 C 输入的同步
    cin.tie(nullptr);              // 读入前不再刷新输出

    int n;
    long long p;                   // 票价也用 long long，防止以后改题面
    cin >> n >> p;

    long long total = 0;           // 总票款会到 10^14，int 装不下
    int best = 0;                  // 单日最高客流

    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        total += (long long)a[i] * p;   // 先转 64 位，再相乘
        if (a[i] > best) best = a[i];
    }

    cout << total << "\n";
    cout << best << "\n";
    return 0;
}
