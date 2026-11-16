#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    stack<char> st;
    bool ok = true;
    for (char ch : s) {
        if (ch == '(' || ch == '[' || ch == '{') {
            st.push(ch);                     // 左括号先存着，等它的右括号
        } else {
            if (st.empty()) {                // 没有左括号可配
                ok = false;
                break;
            }
            char top = st.top();
            if ((ch == ')' && top != '(') ||
                (ch == ']' && top != '[') ||
                (ch == '}' && top != '{')) {
                ok = false;                  // 配错款了
                break;
            }
            st.pop();                        // 配对成功，一起消掉
        }
    }
    if (!st.empty()) ok = false;             // 左括号剩下了，没配完
    cout << (ok ? "YES" : "NO") << "\n";
    return 0;
}
