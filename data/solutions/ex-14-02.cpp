#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN], ans[MAXN];          // ans[i] 存"i 右边第一个更大元素的下标"

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    stack<int> st;               // 存下标；对应数值从栈底到栈顶递减
    for (int i = 1; i <= n; i++) {
        while (!st.empty() && a[st.top()] < a[i]) {
            ans[st.top()] = i;   // 栈顶那个人终于等到比他高的
            st.pop();
        }
        st.push(i);
    }
    while (!st.empty()) {        // 栈里剩下的，右边没有更大的了
        ans[st.top()] = 0;
        st.pop();
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << " ";
        cout << (ans[i] == 0 ? -1 : a[ans[i]]);
    }
    cout << "\n";
    return 0;
}
