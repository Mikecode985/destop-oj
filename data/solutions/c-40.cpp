#include <bits/stdc++.h>
using namespace std;
int main() {
    string a, b;
    cin >> a >> b;
    if (a.size() < b.size()) swap(a, b);
    string r;
    int i = a.size() - 1, j = b.size() - 1, carry = 0;
    while (i >= 0) {
        int d = (a[i] - '0') + (j >= 0 ? b[j] - '0' : 0) + carry;
        r.push_back('0' + d % 10);
        carry = d / 10;
        i--;
        j--;
    }
    if (carry) r.push_back('0' + carry);
    reverse(r.begin(), r.end());
    cout << r << "\n";
    return 0;
}
