#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long sum = 0;              // 10^14 量级，必须用 long long
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        sum += x;
    }
    cout << sum << "\n";
    return 0;
}
