#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long sum = 0, mx = -1;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        sum += x;
        if (x > mx) { mx = x; pos = i; }
    }
    cout << sum << "\n" << pos << "\n";
    return 0;
}
