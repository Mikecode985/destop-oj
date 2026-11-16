#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int t[MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> t[i];
    sort(t + 1, t + n + 1);          // 接水快的先上

    long long wait = 0;              // 总等待时间
    long long prefix = 0;            // 前面所有人接水花的时间
    for (int i = 1; i <= n; i++) {
        wait += prefix;              // 第 i 个人要等 prefix 分钟
        prefix += t[i];
    }
    cout << wait << "\n";
    return 0;
}
