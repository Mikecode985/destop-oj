#include <bits/stdc++.h>
using namespace std;
int main() {
    long long n;
    cin >> n;
    for (long long a = 0; a * a <= n; a++)
        for (long long b = a; a * a + b * b <= n; b++)
            for (long long c = b; a * a + b * b + c * c <= n; c++) {
                long long r = n - a * a - b * b - c * c;
                long long d = (long long)sqrt((double)r);
                while (d * d > r) d--;
                while ((d + 1) * (d + 1) <= r) d++;
                if (d >= c && d * d == r) {
                    cout << a << " " << b << " " << c << " " << d << "\n";
                    return 0;
                }
            }
    cout << -1 << "\n";
    return 0;
}
