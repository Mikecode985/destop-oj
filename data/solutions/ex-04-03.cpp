#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    long long capacity = 0;   // 当前容量
    long long copies = 0;     // 累计拷贝的元素个数
    long long grows = 0;      // 扩容次数

    for (int i = 1; i <= n; i++) {
        if ((long long)i - 1 == capacity) {   // 装满了，需要扩容
            if (capacity == 0) capacity = 1;
            else capacity *= 2;
            copies += (long long)i - 1;       // 旧元素全部搬到新空间
            grows++;
        }
    }

    cout << copies << " " << grows << "\n";
    return 0;
}
