#include <bits/stdc++.h>
using namespace std;
int main() {
    double lo = 1.0, hi = 2.0;
    for (int i = 0; i < 100; i++) {
        double mid = (lo + hi) / 2;
        if (mid * mid * mid - mid - 1 >= 0) hi = mid;
        else lo = mid;
    }
    cout << (long long)((lo + hi) / 2 * 1000000.0) << "\n";
    return 0;
}
