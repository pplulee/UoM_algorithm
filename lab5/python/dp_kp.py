import sys
import time

from knapsack import knapsack


class dp(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        self.time = 0

    def DP(self, solution):
        start_time = time.time()
        # Renaming things to keep track of them wrt. names used in algorithm
        v = self.item_values
        wv = self.item_weights
        n = self.Nitems
        W = self.Capacity

        # the dynamic programming function for the knapsack problem
        # the code was adapted from p17 of http://www.es.ele.tue.nl/education/5MC10/solutions/knapsack.pdf

        # v array holds the values / profits / benefits of the items
        # wv array holds the sizes / weights of the items
        # n is the total number of items
        # W is the constraint (the weight capacity of the knapsack)
        # solution: True in position n means pack item number n+1. False means do not pack it.

        # V and Keep should be 2d arrays for use in the dynamic programming solution
        # They are both of size (n + 1)*(W + 1)

        # Initialise V and keep
        V = [[0 for x in range(W + 1)] for y in range(n + 1)]
        Keep = [[False for x in range(W + 1)] for y in range(n + 1)]
        # main dynamic programming loops, adding on item at a time and looping through weights from 0 to W
        for i in range(1, n + 1):
            for j in range(0, W + 1):
                if (wv[i] <= j) and (v[i] + V[i - 1][j - wv[i]] > V[i - 1][j]):
                    V[i][j] = v[i] + V[i - 1][j - wv[i]]
                    Keep[i][j] = True
                else:
                    V[i][j] = V[i - 1][j]
        K = W
        # now discover which items were in the optimal solution
        for i in range(n, 0, -1):
            if Keep[i][K]:
                print("Item %d is in the knapsack" % i)
                solution[i] = True
                K = K - wv[i]
        end_time = time.time()
        self.time = end_time - start_time
        return V[n][W]


knapsk = dp(sys.argv[1])
solution = [False] * (knapsk.Nitems + 1)
knapsk.DP(solution)
knapsk.check_evaluate_and_print_sol(solution)
