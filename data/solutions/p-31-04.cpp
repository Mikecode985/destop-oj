#include <bits/stdc++.h>
using namespace std;
int main() {
    string a;
    long long b;
    cin >> a >> b;
    vector<int> q;
    long long rem = 0;
    for (char c : a) {
        rem = rem * 10 + (c - '0');
        q.push_back(rem / b);
        rem %= b;
    }
    int i = 0;
    while (i < (int)q.size() - 1 && q[i] == 0) i++;
    for (; i < (int)q.size(); i++) cout << q[i];
    cout << "\n" << rem << "\n";
    return 0;
}
