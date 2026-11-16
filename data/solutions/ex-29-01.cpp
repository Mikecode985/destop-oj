#include <bits/stdc++.h>
using namespace std;

const int MAXR = 1000005;
bool isComp[MAXR];        // 1..sqrt(R) 范围内的合数标记
vector<int> primes;       // 小素数表
bool seg[MAXR];           // 区间 [L, R] 的合数标记，seg[i] 对应 L+i

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long L, R;
    cin >> L >> R;

    long long lim = 1;                       // lim = floor(sqrt(R))
    while ((lim + 1) * (lim + 1) <= R) lim++;

    isComp[0] = isComp[1] = true;
    for (int i = 2; i <= lim; i++) {         // 线性筛出 2..lim 的素数
        if (!isComp[i]) primes.push_back(i);
        for (int p : primes) {
            if (1LL * i * p > lim) break;
            isComp[i * p] = true;
            if (i % p == 0) break;
        }
    }

    int len = (int)(R - L + 1);
    for (int i = 0; i < len; i++) seg[i] = false;
    if (L == 1) seg[0] = true;               // 1 不是素数
    for (int p : primes) {
        long long start = max(2LL, (L + p - 1) / p) * p;   // 区间内第一个 p 的倍数
        for (long long x = start; x <= R; x += p) {
            if (x != p) seg[x - L] = true;   // p 本身是素数，不能划掉
        }
    }

    long long cnt = 0, sum = 0;
    for (int i = 0; i < len; i++) {
        if (!seg[i]) {
            cnt++;
            sum += L + i;
        }
    }
    cout << cnt << "\n" << sum << "\n";
    return 0;
}
