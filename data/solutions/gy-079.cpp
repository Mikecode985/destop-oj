#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 3;
    string s; cin >> s;
    int x = 0, y = 0, maxd = 0, first = -1;
    set<pair<int,int>> seen; seen.insert({0,0});
    int minx = 0, maxx = 0, miny = 0, maxy = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == 'U') y++;
        else if (s[i] == 'D') y--;
        else if (s[i] == 'L') x--;
        else x++;
        seen.insert({x, y});
        maxd = max(maxd, abs(x) + abs(y));
        minx = min(minx, x); maxx = max(maxx, x);
        miny = min(miny, y); maxy = max(maxy, y);
        if (first < 0 && x == 0 && y == 0) first = i + 1;
    }
    if (MODE == 0) cout << x << " " << y << "\n";
    else if (MODE == 1) cout << maxd << "\n";
    else if (MODE == 2) cout << seen.size() << "\n";
    else if (MODE == 3) cout << first << "\n";
    else cout << 1LL * (maxx - minx + 1) * (maxy - miny + 1) << "\n";
    return 0;
}
