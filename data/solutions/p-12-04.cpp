#include <bits/stdc++.h>
using namespace std;
int main() {
    int a[9];
    char c;
    for (int i = 0; i < 9; i++) { cin >> c; a[i] = c - '0'; }
    int inv = 0;
    for (int i = 0; i < 9; i++) {
        if (a[i] == 0) continue;
        for (int j = i + 1; j < 9; j++) {
            if (a[j] == 0) continue;
            if (a[i] > a[j]) inv++;
        }
    }
    cout << (inv % 2 == 0 ? "Yes" : "No") << "\n";
    return 0;
}
