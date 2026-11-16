#include <bits/stdc++.h>
using namespace std;
int main() {
    int s;
    cin >> s;
    int price;
    if (s <= 4) price = 2;
    else if (s <= 9) price = 3;
    else if (s <= 15) price = 4;
    else {
        int extra = (s - 15 + 4) / 5;
        price = 4 + extra;
        if (price > 8) price = 8;
    }
    cout << price << "\n";
    return 0;
}
