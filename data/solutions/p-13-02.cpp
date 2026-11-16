#include <bits/stdc++.h>
using namespace std;
int n;
string cur;
void dfs(int open, int close) {
    if ((int)cur.size() == 2 * n) {
        cout << cur << "\n";
        return;
    }
    if (open < n) {
        cur.push_back('(');
        dfs(open + 1, close);
        cur.pop_back();
    }
    if (close < open) {
        cur.push_back(')');
        dfs(open, close + 1);
        cur.pop_back();
    }
}
int main() {
    cin >> n;
    dfs(0, 0);
    return 0;
}
