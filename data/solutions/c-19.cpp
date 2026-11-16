#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    unordered_set<int> st;
    st.reserve(n * 2);
    int x, rep = -1;
    for (int i = 0; i < n; i++) {
        cin >> x;
        if (!st.insert(x).second) rep = x;
    }
    cout << rep << "\n";
    return 0;
}
