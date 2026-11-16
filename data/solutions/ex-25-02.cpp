#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<int> tails;      // tails[k]：长度 k+1 的上升子序列能取到的最小结尾
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        // 找第一个 >= x 的位置
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);   // 比所有结尾都大，长度加一
        else *it = x;                                // 用更小的结尾顶掉它
    }
    cout << tails.size() << "\n";                    // 数组长度就是答案
    return 0;
}
