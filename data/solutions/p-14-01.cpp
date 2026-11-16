#include <bits/stdc++.h>
using namespace std;
int main() {
    string tok;
    vector<long long> st;
    while (cin >> tok) {
        if (tok == "+" || tok == "-" || tok == "*" || tok == "/") {
            long long b = st.back(); st.pop_back();
            long long a = st.back(); st.pop_back();
            if (tok == "+") st.push_back(a + b);
            else if (tok == "-") st.push_back(a - b);
            else if (tok == "*") st.push_back(a * b);
            else st.push_back(a / b);
        } else {
            st.push_back(stoll(tok));
        }
    }
    cout << st.back() << "\n";
    return 0;
}
