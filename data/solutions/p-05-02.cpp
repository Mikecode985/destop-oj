#include <bits/stdc++.h>
using namespace std;
int main() {
    long long t;
    cin >> t;
    int r = (int)(t % 90);
    if (r < 30) cout << "绿灯\n";
    else if (r < 33) cout << "黄灯\n";
    else cout << "红灯\n";
    return 0;
}
