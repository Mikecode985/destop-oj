#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> h(n);
    for (auto &x : h) cin >> x;
    vector<int> ans(n, 0);
    vector<int> st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && h[st.back()] <= h[i]) st.pop_back();
        if (!st.empty()) ans[i] = st.back() + 1;
        st.push_back(i);
    }
    for (int i = 0; i < n; i++) cout << ans[i] << (i + 1 == n ? '\n' : ' ');
    return 0;
}
