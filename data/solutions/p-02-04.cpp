#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<string> name(n);
    vector<int> price(n);
    for (int i = 0; i < n; i++) cin >> name[i] >> price[i];
    vector<int> used(n, 0);
    int out = min(n, 3);
    for (int k = 0; k < out; k++) {
        int best = -1;
        for (int i = 0; i < n; i++) {
            if (used[i]) continue;
            if (best == -1 || price[i] > price[best]) best = i;
        }
        used[best] = 1;
        cout << name[best] << " " << price[best] << "\n";
    }
    return 0;
}
