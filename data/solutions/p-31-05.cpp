#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    vector<int> d{0};
    for (char c : s) {
        int carry = c - '0';
        for (int i = 0; i < (int)d.size(); i++) {
            int v = d[i] * 2 + carry;
            d[i] = v % 10;
            carry = v / 10;
        }
        while (carry) { d.push_back(carry % 10); carry /= 10; }
    }
    while (d.size() > 1 && d.back() == 0) d.pop_back();
    for (int i = d.size() - 1; i >= 0; i--) cout << d[i];
    cout << "\n";
    return 0;
}
