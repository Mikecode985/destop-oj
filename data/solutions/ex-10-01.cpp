#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN], tmp[MAXN];

void mergeSort(int l, int r) {
    if (l >= r) return;                  // 最多一个元素，天然有序
    int mid = l + (r - l) / 2;

    mergeSort(l, mid);                   // 分：排好左半段
    mergeSort(mid + 1, r);               // 分：排好右半段

    int i = l, j = mid + 1, k = l;       // 合：两个有序段拉链式合并
    while (i <= mid && j <= r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];   // 相等先取左边，保证稳定
        else tmp[k++] = a[j++];
    }
    while (i <= mid) tmp[k++] = a[i++];        // 左段剩下的一股脑接上
    while (j <= r) tmp[k++] = a[j++];          // 右段剩下的一股脑接上

    for (int p = l; p <= r; p++) a[p] = tmp[p];   // 写回原数组
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    mergeSort(1, n);

    for (int i = 1; i <= n; i++) cout << a[i] << (i == n ? '\n' : ' ');
    return 0;
}
