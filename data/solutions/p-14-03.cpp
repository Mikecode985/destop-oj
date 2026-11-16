#include <bits/stdc++.h>
using namespace std;
int main() {
    int n;
    cin >> n;
    vector<long long> h(n);
    for (auto &x : h) cin >> x;
    h.push_back(0);
    vector<int> st;
    long long ans = 0;
    for (int i = 0; i <= n; i++) {
        while (!st.empty() && h[st.back()] >= h[i]) {
            long long ht = h[st.back()];
            st.pop_back();
            int left = st.empty() ? -1 : st.back();
            ans = max(ans, ht * (i - left - 1));
        }
        st.push_back(i);
    }
    cout << ans << "\n";
    return 0;
}
