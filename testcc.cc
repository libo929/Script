#include <chrono>
#include <iostream>

using namespace std;

long calc(int n, int i = 0, long cols = 0, long diags = 0, long trans = 0) {
    if (i == n) {
        return 1;
    } else {
        long rt = 0;
        for (int j = 0; j < n; j++) {
            long col = (1 << j);
            long diag = (1 << (i - j + n - 1));
            long tran = (1 << (i + j));
            if (!(col & cols) && !(diag & diags) && !(tran & trans)) {
                rt += calc(n, i + 1, col | cols, diag | diags, tran | trans);
            }
        }
        return rt;
    }
}

int main() {
    auto t = chrono::system_clock::now();
    cout << calc(13) << endl;
    cout << (chrono::system_clock::now() - t).count() * 1e-6 << endl;
    return 0;
}
