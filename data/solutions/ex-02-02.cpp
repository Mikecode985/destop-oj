#include <bits/stdc++.h>
using namespace std;

struct Stall {
    string name;   // 摊位名（不含空格）
    int price;     // 单价
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;

    const int MAXN = 105;
    Stall a[MAXN];
    for (int i = 1; i <= m; i++) {
        cin >> a[i].name >> a[i].price;
    }

    // 选择排序：每轮挑出价格最低的摊位，换到当前位置
    for (int i = 1; i <= m; i++) {
        int best = i;
        for (int j = i + 1; j <= m; j++) {
            if (a[j].price < a[best].price) best = j;
        }
        if (best != i) {
            Stall t = a[i];       // 结构体整体交换，三行不能省
            a[i] = a[best];
            a[best] = t;
        }
    }

    for (int i = 1; i <= m; i++) {
        cout << a[i].name << " " << a[i].price << "\n";
    }
    return 0;
}
