#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef unsigned long long ull;
// typedef __int128_t ell;
// typedef __uint128_t uell;
#define delay(time) this_thread::sleep_for(std::chrono::seconds(time)

const int mxW = 8000;

vector<bool> Knapsack(vector<int>& weig, vector<int>& val) {
  int N = weig.size();
  int dp[N][mxW + 1];
  bool take[N][mxW + 1];
  memset(dp, 0, sizeof(dp));
  memset(take, 0, sizeof(take));

  dp[0][weig[0]] = val[0];
  take[0][weig[0]] = true;

  for (int phase = 1; phase < N; ++phase) {
    int idx = phase;
    for (int w = 0; w <= mxW; ++w) {
      // Dont take
      dp[idx][w] = dp[idx - 1][w];

      // Take
      if (weig[idx] <= w && dp[idx - 1][w - weig[idx]] + val[idx] >= dp[idx][w]) {
        dp[idx][w] = dp[idx - 1][w - weig[idx]] + val[idx];
        take[idx][w] = true;
      }
    }
  }
  int best_val = *max_element(dp[N - 1], dp[N - 1] + mxW + 1);

  // Build the solution
  int current_weig = -1;
  for (int w = 0; w <= mxW; ++w) {
    if (best_val == dp[N - 1][w]) {
      current_weig = w;
      break;
    }
  }
  assert(current_weig > -1);
  int check_val = 0;
  vector<bool> X(N, false);
  for (int i = N - 1; i >= 0; --i) {
    if (take[i][current_weig]) {
      X[i] = true;
      current_weig -= weig[i];
      check_val += val[i];
    }
  }
  assert(current_weig == 0);
  assert(best_val == check_val);
  return X;
}

void solve() {
  vector<int> W = {601, 7902, 6, 4520, 112, 7890, 334, 1200, 5600, 45, 6780, 230, 4400, 900, 3100, 7200, 50, 88, 3900, 7500, 2100, 6400, 500, 4200, 7700, 150, 3300, 120, 5900, 6800, 2500, 400, 7100, 950, 4800, 10, 6200, 3500, 800, 5500, 2700, 600, 7300, 1800, 4900, 7600, 320, 5400, 2200, 110};
  vector<int> V = {100, 567, 802, 345, 999, 120, 450, 670, 230, 890, 410, 560, 320, 770, 150, 600, 950, 430, 210, 500, 820, 390, 700, 480, 110, 660, 370, 920, 280, 530, 740, 400, 850, 190, 620, 980, 300, 550, 790, 440, 250, 690, 360, 810, 460, 130, 720, 260, 510, 930};
  vector<bool> mask = Knapsack(W, V);

  int best_val = 0;
  int best_weig = 0;

  cout << "Los componentes a desplegar en AWS son: " << endl;
  for (int i = 0; i < mask.size(); ++i) {
    if (mask[i]) {
      cout << i << ",\n"[i + 1 == mask.size()] << " \n"[i + 1 == mask.size()];
      best_val += V[i];
      best_weig += W[i];
    }
  }

  cout << "Mejor valor de impacto lograble con 8000MB = " << best_val << " puntos" << endl;
  cout << "Memoria RAM usada = " << best_weig << "MB" << endl;
}

signed main() {
  ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
  int T = 1;
  // cin >> T;
  while (T--) solve();
  return 0;
}
