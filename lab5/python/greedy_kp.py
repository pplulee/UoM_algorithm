import sys

from knapsack import knapsack


class greedy(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)

    def greedy(self):
        self.total_weight = 0  # current total weight of the items in the knapsack
        self.total_value = 0  # current total profit of the items in the knapsack
        solution = [None] * (self.Nitems + 1)

        self.sort_by_ratio()  # sort by profit-to-weight ratio

        # ADD CODE HERE TO COMPUTE THE GREEDY SOLUTION

        # THE CODE SHOULD: take the items in descending
        # profit-to-weight ratio order (by using temp_indexes) and,
        # if an item fits, add it to the knapscak, and
        # do not stop at the first item that doesn't fit
        # - but keep going until all items have been tried.
        for i in range(1, self.Nitems + 1):
            if self.total_weight + self.item_weights[self.temp_indexes[i]] <= self.Capacity:
                solution[self.temp_indexes[i]] = True
                self.total_weight += self.item_weights[self.temp_indexes[i]]
                self.total_value += self.item_values[self.temp_indexes[i]]
            else:
                solution[self.temp_indexes[i]] = False

        print("The greedy solution - not necessarily optimal - is:")
        self.check_evaluate_and_print_sol(solution)

        # NOTE: If the result to you get when you use the check_ ...() function
        # is not what you expected, if could be because you mapped to the sorted
        # order TWICE
        # Use
        #   solution[i] = Trye
        # in order to "pack" the iths most value-dense item,
        # not solution[temp_indexes[i]]


knapsk = greedy(sys.argv[1])
knapsk.print_instance()
knapsk.greedy()
