#include <bits/stdc++.h>
using namespace std;
int main() {
    int n, W;
    cin >> n >> W;
    vector<char> ok(W + 1, 0);
    ok[0] = 1;
    for (int i = 0; i < n; i++) {
        int v;
        cin >> v;
        for (int j = W; j >= v; j--)
            if (ok[j - v]) ok[j] = 1;
    }
    for (int j = W; j >= 0; j--)
        if (ok[j]) { cout << j << "\n"; return 0; }
    return 0;
}
