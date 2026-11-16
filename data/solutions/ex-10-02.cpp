#include <bits/stdc++.h>
using namespace std;

const int MAXN = 100005;
int a[MAXN], tmp[MAXN];
long long invCnt = 0;                    // 逆序对可能到 5e9，用 long long

void mergeSort(int l, int r) {
    if (l >= r) return;
    int mid = l + (r - l) / 2;
    mergeSort(l, mid);
    mergeSort(mid + 1, r);

    int i = l, j = mid + 1, k = l;
    while (i <= mid && j <= r) {
        if (a[i] <= a[j]) {
            tmp[k++] = a[i++];
        } else {
            // a[j] 比左段剩下的 mid-i+1 个都小，一次数完
            invCnt += mid - i + 1;
            tmp[k++] = a[j++];
        }
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int p = l; p <= r; p++) a[p] = tmp[p];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    mergeSort(1, n);
    cout << invCnt << "\n";
    return 0;
}
