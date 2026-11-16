#include <bits/stdc++.h>
using namespace std;
const int N = 200000;
vector<int> primes;
bool comp[N + 1];
void init() {
    for (int i = 2; i <= N; i++) {
        if (!comp[i]) {
            primes.push_back(i);
            for (long long j = 1LL * i * i; j <= N; j += i) comp[j] = true;
        }
    }
}
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    init();
    const int MODE = 1;
    int n; cin >> n;
    if (MODE == 0) {
        cout << upper_bound(primes.begin(), primes.end(), n) - primes.begin() << "\n";
    } else if (MODE == 1) {
        cout << primes[n - 1] << "\n";
    } else if (MODE == 2) {
        int x = n; bool first = true;
        for (int p = 2; 1LL * p * p <= x; p++) if (x % p == 0) {
            int e = 0; while (x % p == 0) { x /= p; e++; }
            if (!first) cout << " "; cout << p << "^" << e; first = false;
        }
        if (x > 1) { if (!first) cout << " "; cout << x << "^1"; }
        cout << "\n";
    } else if (MODE == 3) {
        int cnt = 0;
        for (int p : primes) {
            if (p > n - p) break;
            int q = n - p;
            if (!comp[q]) cnt++;
        }
        cout << cnt << "\n";
    } else {
        cout << *lower_bound(primes.begin(), primes.end(), n) << "\n";
    }
    return 0;
}
