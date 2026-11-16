#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false); cin.tie(nullptr);
    const int MODE = 4;
    int n; cin >> n; vector<int> a(n);
    for (int &x : a) cin >> x;
    if (MODE == 0 || MODE == 1 || MODE == 3) {
        vector<int> ans(n, 0);
        stack<int> st;
        for (int i = n - 1; i >= 0; i--) {
            while (!st.empty() && a[st.top()] <= a[i]) st.pop();
            if (!st.empty()) ans[i] = (MODE == 1 ? st.top() + 1 : (MODE == 3 ? st.top() - i : a[st.top()]));
            st.push(i);
        }
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? "\n" : " ");
    } else if (MODE == 2) {
        vector<int> ans(n, 0);
        stack<int> st;
        for (int i = 0; i < n; i++) {
            while (!st.empty() && a[st.top()] <= a[i]) st.pop();
            if (!st.empty()) ans[i] = a[st.top()];
            st.push(i);
        }
        for (int i = 0; i < n; i++) cout << ans[i] << (i == n - 1 ? "\n" : " ");
    } else {
        long long cnt = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (a[i] < a[j]) cnt++;
        cout << cnt << "\n";
    }
    return 0;
}
