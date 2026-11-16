#include <bits/stdc++.h>
using namespace std;
int main() {
    string s;
    cin >> s;
    vector<int> st;
    st.push_back(-1);
    int best = 0;
    for (int i = 0; i < (int)s.size(); i++) {
        if (s[i] == '(') st.push_back(i);
        else {
            st.pop_back();
            if (st.empty()) st.push_back(i);
            else best = max(best, i - st.back());
        }
    }
    cout << best << "\n";
    return 0;
}
