#include <bits/stdc++.h>
using namespace std;

// 把 n 个盘子从 from 移到 to，借助 aux，返回移动步数
long long hanoi(int n, char from, char aux, char to) {
    if (n == 0) return 0;                       // 没有盘子，不用动
    long long cnt = 0;
    cnt += hanoi(n - 1, from, to, aux);         // 上面 n-1 个先挪到中转站
    cnt += 1;                                   // 最大的那个挪一步
    cnt += hanoi(n - 1, aux, from, to);         // 再把这 n-1 个挪到终点
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cout << hanoi(n, 'A', 'B', 'C') << "\n";
    return 0;
}
