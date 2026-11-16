#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    int cnt = 0;
    for (int i = 1; i <= n; i++) {
        int s = 0, x = i;
        while (x) { s += x % 10; x /= 10; }
        if (s % 9 == 0) cnt++;
    }
    cout << cnt << "\n";
    return 0;
}
