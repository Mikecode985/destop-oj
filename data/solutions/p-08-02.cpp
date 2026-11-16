#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, d;
    cin >> n >> d;
    vector<pair<double, double>> seg;
    for (int i = 0; i < n; i++) {
        int x, y;
        cin >> x >> y;
        if (y > d) { cout << -1 << "\n"; return 0; }
        double half = sqrt((double)d * d - (double)y * y);
        seg.push_back({x + half, x - half});
    }
    sort(seg.begin(), seg.end());
    int cnt = 0;
    double last = -1e18;
    for (auto &s : seg) {
        if (s.second > last) {
            cnt++;
            last = s.first;
        }
    }
    cout << cnt << "\n";
    return 0;
}
