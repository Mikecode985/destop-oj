#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    int d = 0, best = 0;
    for (char c : s) {
        if (c == '(') d++;
        else d--;
        best = max(best, d);
    }
    cout << best << "\n";
    return 0;
}
