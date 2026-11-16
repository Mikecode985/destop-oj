#include <bits/stdc++.h>
using namespace std;
struct Item { string name; long long price; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Item> v(n);
    for (auto &it : v) cin >> it.name >> it.price;
    sort(v.begin(), v.end(), [](const Item &a, const Item &b) {
        if (a.price != b.price) return a.price < b.price;
        return a.name < b.name;
    });
    for (auto &it : v) cout << it.name << " " << it.price << "\n";
    return 0;
}
