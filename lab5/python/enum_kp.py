import sys
import math

from knapsack import knapsack


class enum_knapsack(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)

    def enumerate(self):
        # Do an exhaustive search (aka enumeration) of all possible ways to pack
        # the knapsack.
        # This is achived by creating every "binary" solution vectore of length Nitems.
        # For each solution vector, its value and weight is calculated

        solution = [False] * (self.Nitems + 1)  # (binary/ true/false) solution vectore representing items pack
        best_solution = [False] * (self.Nitems + 1)  # (binary) solution veectore for best solution found
        j = 0.0

        self.QUIET = True
        best_value = 0  # total value packed in the best solution
        current_progress = 0.0

        while not self.next_binary(solution, self.Nitems):
            current_progress_int = int(current_progress * 100)
            j = j + 1.0
            current_progress = j / math.pow(2, self.Nitems)
            if not self.QUIET:
                print("done %g of the full enumeration" % current_progress)
            if current_progress_int!=int(current_progress * 100):
                print("\r", end="")
                print(
                    f"program running status: {int(current_progress * 100)}% | [{'▋' * (int(current_progress * 100) // 2)}{' ' * (50-(int(current_progress * 100) // 2))}]",
                    end="")

            infeasible = self.check_evaluate_and_print_sol(solution)

            if (not infeasible) and self.total_value > best_value:
                best_value = self.total_value

                for i in range(1, self.Nitems + 1):
                    best_solution[i] = solution[i]

            if not self.QUIET:
                print("best so far has value %d" % best_value)

        self.QUIET = False
        print("Finished.\nPack the following items for optimal")
        self.check_evaluate_and_print_sol(best_solution)

    def next_binary(self, sol, Nitems):
        # Called with a "binary" vector of length Nitems, this
        # method "adds 1" to the vector, e.g. 0001 would turn to 0010.
        # If the string overflows, then the function returs True, else it returns False
        i = Nitems
        while i > 0:
            if sol[i]:
                sol[i] = False
                i = i - 1
            else:
                sol[i] = True
                break
        if i == 0:
            return True
        else:
            return False


knapsk = enum_knapsack(sys.argv[1])
knapsk.print_instance()
knapsk.enumerate()
