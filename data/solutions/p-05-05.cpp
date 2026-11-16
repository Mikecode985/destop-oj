#include <bits/stdc++.h>
using namespace std;
long long fdiv(long long a, long long b) {
    long long q = a / b;
    if (a % b != 0 && ((a < 0) != (b < 0))) q--;
    return q;
}
int main() {
    string s;
    getline(cin, s);
    vector<long long> num;
    vector<char> op;
    string t;
    for (char c : s + "+") {
        if (c >= '0' && c <= '9') t += c;
        else if (c == '+' || c == '-' || c == '*' || c == '/') {
            if (!t.empty()) { num.push_back(stoll(t)); t.clear(); }
            op.push_back(c);
        }
    }
    vector<long long> a;
    vector<char> b;
    a.push_back(num[0]);
    for (size_t i = 0; i + 1 < op.size(); i++) {
        if (op[i] == '*') a.back() = a.back() * num[i + 1];
        else if (op[i] == '/') a.back() = fdiv(a.back(), num[i + 1]);
        else { b.push_back(op[i]); a.push_back(num[i + 1]); }
    }
    long long ans = a[0];
    for (size_t i = 0; i < b.size(); i++) ans = b[i] == '+' ? ans + a[i + 1] : ans - a[i + 1];
    cout << ans << "\n";
    return 0;
}
