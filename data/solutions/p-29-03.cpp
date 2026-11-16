#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<char> comp(n + 1, 0);
    vector<int> pr;
    pr.reserve(n / 10);
    for (int i = 2; i <= n; i++) {
        if (!comp[i]) pr.push_back(i);
        for (int p : pr) {
            if ((long long)i * p > n) break;
            comp[i * p] = 1;
            if (i % p == 0) break;
        }
    }
    cout << pr.size() << "\n";
    return 0;
}
