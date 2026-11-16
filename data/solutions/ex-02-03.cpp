#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cin.ignore();                  // 吃掉 n 后面的换行，否则第一行读成空串

    const int MAXN = 105;
    string name[MAXN];
    for (int i = 1; i <= n; i++) {
        getline(cin, name[i]);     // 整行读入，空格原样保留
    }

    for (int i = n; i >= 1; i--) {
        cout << name[i] << "\n";
    }
    return 0;
}
