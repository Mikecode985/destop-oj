#include <bits/stdc++.h>
using namespace std;
int main() {
    long long x, sum = 0;
    int days = 0;
    for (int i = 0; i < 7; i++) {
        cin >> x;
        if (x != -1) { days++; sum += x; }
    }
    cout << days << "\n" << sum << "\n" << (days ? sum / days : 0) << "\n";
    return 0;
}
