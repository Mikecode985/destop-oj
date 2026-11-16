#include <bits/stdc++.h>
using namespace std;
string sub(const string &a, const string &b) {
    string r;
    int i = a.size() - 1, j = b.size() - 1, borrow = 0;
    while (i >= 0) {
        int d = (a[i] - '0') - borrow - (j >= 0 ? b[j] - '0' : 0);
        if (d < 0) { d += 10; borrow = 1; } else borrow = 0;
        r.push_back('0' + d);
        i--;
        j--;
    }
    while (r.size() > 1 && r.back() == '0') r.pop_back();
    reverse(r.begin(), r.end());
    return r;
}
int main() {
    string a, b;
    cin >> a >> b;
    // 去掉前导零
    while (a.size() > 1 && a[0] == '0') a.erase(a.begin());
    while (b.size() > 1 && b[0] == '0') b.erase(b.begin());
    cout << sub(a, b) << "\n";
    return 0;
}
