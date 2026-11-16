#include <bits/stdc++.h>
using namespace std;
bool leap(int y) { return (y % 4 == 0 && y % 100 != 0) || y % 400 == 0; }
long long days(int y, int m, int d) {
    long long s = 0;
    for (int i = 1; i < y; i++) s += leap(i) ? 366 : 365;
    int md[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    for (int i = 1; i < m; i++) s += md[i - 1] + (i == 2 && leap(y) ? 1 : 0);
    s += d - 1;
    return s;
}
int main() {
    int y1, m1, d1, y2, m2, d2;
    cin >> y1 >> m1 >> d1 >> y2 >> m2 >> d2;
    long long a = days(y1, m1, d1), b = days(y2, m2, d2);
    cout << llabs(a - b) << "\n";
    return 0;
}
