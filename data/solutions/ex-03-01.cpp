#include <bits/stdc++.h>
using namespace std;

struct Stall {
    string name;   // 摊位名
    int price;     // 单价
};

bool cmp(const Stall &a, const Stall &b) {
    if (a.price != b.price) return a.price < b.price;   // 第一关键字：价格
    return a.name < b.name;                             // 第二关键字：名称
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;
    vector<Stall> stalls(m);
    for (int i = 0; i < m; i++) {
        cin >> stalls[i].name >> stalls[i].price;
    }

    sort(stalls.begin(), stalls.end(), cmp);   // 一行完成多关键字排序

    long long total = 0;
    int cheap = 0;
    for (const auto &s : stalls) {
        cout << s.name << " " << s.price << "\n";
        total += s.price;
        if (s.price <= 20) cheap++;
    }
    cout << "total " << total << "\n";
    cout << "cheap " << cheap << "\n";
    return 0;
}
