#include <bits/stdc++.h>
using namespace std;
int main() {
    long long n;
    cin >> n;
    long long cnt = 0;
    int c[4] = {10, 5, 2, 1};
    for (int i = 0; i < 4; i++) {
        cnt += n / c[i];
        n %= c[i];
    }
    cout << cnt << "\n";
    return 0;
}
