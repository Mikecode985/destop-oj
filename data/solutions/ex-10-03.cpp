#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN];

// 在 a[l..r] 中找整个数组第 k 小的数（k 从 1 开始）
int quickSelect(int l, int r, int k) {
    if (l == r) return a[l];
    int pivot = a[l + (r - l) / 2];      // 取中间值当基准，避开最坏情况
    int i = l, j = r;
    while (i <= j) {
        while (a[i] < pivot) i++;        // 左边找第一个 >= 基准的
        while (a[j] > pivot) j--;        // 右边找第一个 <= 基准的
        if (i <= j) {
            swap(a[i], a[j]);
            i++;
            j--;
        }
    }
    // 此时 a[l..j] <= 基准 <= a[i..r]
    if (k <= j) return quickSelect(l, j, k);        // 答案在左段
    if (k >= i) return quickSelect(i, r, k);        // 答案在右段
    return a[k];                                    // 答案就是基准这一层
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    for (int i = 1; i <= n; i++) cin >> a[i];
    cout << quickSelect(1, n, k) << "\n";
    return 0;
}
