#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<char> comp(n + 1, 0);
    int cnt = 0;
    for (int i = 2; i <= n; i++) {
        if (comp[i]) continue;
        cnt++;
        for (long long j = (long long)i * i; j <= n; j += i) comp[j] = 1;
    }
    cout << cnt << "\n";
    return 0;
}
