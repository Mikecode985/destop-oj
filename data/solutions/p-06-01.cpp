#include <bits/stdc++.h>
using namespace std;
int main() {
    int cnt = 0;
    for (int x = 1; x <= 100; x++)
        for (int y = 1; y <= 100; y++) {
            int z = 100 - x - y;
            if (z < 1 || z % 3 != 0) continue;
            if (5 * x + 3 * y + z / 3 == 100) {
                cout << x << " " << y << " " << z << "\n";
                cnt++;
            }
        }
    cout << cnt << "\n";
    return 0;
}
