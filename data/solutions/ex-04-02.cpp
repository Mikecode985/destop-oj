#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    cin >> n;

    const long long LIMIT = 256LL * 1024 * 1024;   // 256 MB 换成字节
    long long bytes = n * 4;                        // 每个 int 占 4 字节

    cout << bytes << "\n";
    if (bytes <= LIMIT) {
        cout << "YES\n";
    } else {
        cout << "NO\n";
    }
    return 0;
}
