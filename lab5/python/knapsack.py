#
# set of functions that are used by two or more of the knapsack solution
# methods: enum, branch-and-bound, dynamic programming and greedy
#

class knapsack:
        
    def __init__(self, filename):
        self.QUIET = False
        # Note: knapsack intems in the input files are numbered from 1 to N
        # We shall use arrays of size N+1 to store the indexes, weights and values
        # of the items.  So w[1] and v[1] stored the weight and value of the first item.
        
        try:
            f = open (filename)
            self.Nitems = int(f.readline())
            self.item_weights = [None]*(self.Nitems + 1)
            self.item_values = [None]*(self.Nitems + 1)
            self.temp_indexes = [0]*(self.Nitems + 1)

            for i in range(1, self.Nitems + 1):
                (index_string, value_string, weight_string) = f.readline().split()
                self.temp_indexes[i] = int(index_string)
                self.item_values[i] = int(value_string)
                self.item_weights[i] = int(weight_string)
                
            self.Capacity = int(f.readline())
            return
        except:
            print("Problem reading from file and/or allocating arrays")
            exit(1)
            
    def print_instance(self):
        print("item\tW\tV")
        for i in range(1, self.Nitems + 1):
            print("%d\t%d\t%d" % (self.temp_indexes[i], self.item_weights[i], self.item_values[i]))
        print("%d" % self.Capacity)
        
    def sort_by_ratio(self):
        # sort the item indexes
        self.temp_indexes.sort(key=self.mycomp, reverse=True)
        
        # Sadly the above puts the None first item at the end of the list move the end to the start
        # I'm sure there's a better way to do this
        start = self.temp_indexes.pop()
        self.temp_indexes.insert(0, start)
        
        
        for i in range(1, self.Nitems + 1):
            print("%d\t%d\t" % (self.item_weights[self.temp_indexes[i]], self.item_values[self.temp_indexes[i]]), end="")
            print("%f" % (self.item_weights[self.temp_indexes[i]] / self.item_values[self.temp_indexes[i]]))
        
    def mycomp(self, ia):
        if (self.item_values[ia] == None):
            return 0
        return self.item_values[ia]/self.item_weights[ia]
        
    def check_evaluate_and_print_sol(self, sol):
        # This function prints out the items packed in a solution, in ascending order.
        # Since items may have been sorted in a different order (using temp_indexes), it first reverses this mapping


        # The vector sol is a "binary" vector of length Nitems, describing the items to be put in the knapsack.
        # The (global) temp_indexes array maps item i to temp_indexes[i].
        # So sol[i]=True really means item temp_indexes[i] should be taken.
        # In order to print out the item numbers referred to by sol in ascending order, we
        # copy them accross to an auxiliary array "pack" and then print the
        # items in pack in ascending order.
        
        self.total_value = 0 # total value packed
        self.total_weight = 0 # total weight packed
        pack = [None]*(self.Nitems + 1) # auxilliary array to do reverse-mapping
        
        # First pass: unamp the mapping using pack
        for i in range(1, self.Nitems + 1):
            if (sol[i]):
                pack[self.temp_indexes[i]] = True
            else:
                pack[self.temp_indexes[i]] = False
                
        # Second pass: now print out item numbers of items to be packed in ascending order
        if (not self.QUIET):
            print("Pack items: ", end="")
            
        for i in range(1, self.Nitems + 1):
            if (pack[i]):
                if (not self.QUIET):
                    print("%d " % i, end="")
                self.total_value += self.item_values[i]
                self.total_weight += self.item_weights[i]
                
        # Finally, print out the value, weight and Capacity, and feasibility
        if (not self.QUIET):
            if (self.total_weight > self.Capacity):
                print("\nvalue=%d weight=%d > Capacity=%d: Infeasible" % (self.total_value, self.total_weight, self.Capacity))
            else:
                print("\nvalue=%d weight=%d <= Capacity=%d: Feasible" % (self.total_value, self.total_weight, self.Capacity))
        if (self.total_weight > self.Capacity):
            return True # return True for infeasible solutions
        else:
            return False # return True for feasible solutions

