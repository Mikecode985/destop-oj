#include <bits/stdc++.h>
using namespace std;
int n;
vector<int> a, tmp;
long long inv, eq;
void msort(int l, int r) {
    if (l >= r) return;
    int mid = (l + r) / 2;
    msort(l, mid);
    msort(mid + 1, r);
    int i = l, j = mid + 1, k = l;
    while (i <= mid && j <= r) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else { inv += mid - i + 1; tmp[k++] = a[j++]; }
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= r) tmp[k++] = a[j++];
    for (int t = l; t <= r; t++) a[t] = tmp[t];
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    a.resize(n);
    tmp.resize(n);
    for (auto &x : a) cin >> x;
    msort(0, n - 1);
    // 相等对：排序后每组相同元素两两配对
    int i = 0;
    while (i < n) {
        int j = i;
        while (j + 1 < n && a[j + 1] == a[i]) j++;
        long long c = j - i + 1;
        eq += c * (c - 1) / 2;
        i = j + 1;
    }
    long long all = (long long)n * (n - 1) / 2;
    cout << all - inv - eq << "\n";
    return 0;
}
