from enum import Enum
import config
import sys

class darray:
    def __init__(self):
        self.array = []
        self.sorted = False
        self.mode = config.mode
        self.verbose = config.verbose
        
    def insert(self, string):
        self.array.append(string)
        
        # changing the array means it may no longer be sorted
        self.sorted = False
        
    def find(self, value):
        if (self.mode == SearchModes.LINEAR_SEARCH.value):
            # TODO implement linear search through list
            print("Linear search not yet implemented")
        else:
            if (not self.sorted):
                if (self.verbose > 0):
                    print("Dynamic Array not sorted, sorting... \n")
                    
                self.sort(self.mode)
                if (self.verbose > 0):
                    print("Dynamic Array sorted\n")
                
                self.sorted = True
            # TODO implement binary search through array
        return False
        
    def print_set(self):
        print("DArray:\n")
        for i in range(len(self.array)):
            print("\t%s\n" % self.array[i])
            
    def print_stats(self):
        print("Dynamic array contains %d elements\n" % len(self.array))
        
    def sort(self, select):
        if (select == SearchModes.BINARY_SEARCH_ONE.value):
            self.insertion_sort()
        elif (select == SearchModes.BINARY_SEARCH_TWO.value):
            self.quick_sort()
        elif (select == SearchModes.BINARY_SEARCH_THREE.value):
            print("Nothing Implemented\n")
        elif (select == SearchModes.BINARY_SEARCH_FOUR.value):
            print("Nothing Implemented\n")
        elif (select == SearchModes.BINARY_SEARCH_FIVE.value):
             print("Nothing Implemented\n")
       #  Add your own choices here
        else:
            sys.stderr.write("The value %d is not supported\n" % select)
            sys.exit(23)
            
    # You may find this helpful
    # It swaps the element at index a and the element at index b in array
    def swap(self, a, b):
        temp = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = temp
        
    def insertion_sort(self):
        sys.stderr.write("Not implemented\n")
        sys.exit(-1)
        
    # Hint: you probably want to define a help function for the recursive call    
    def quick_sort(self):
        sys.stderr.write("Not implemented\n")
        sys.exit(-1)

            
    
            
    
class SearchModes(Enum):
    LINEAR_SEARCH = 0
    BINARY_SEARCH_ONE = 1
    BINARY_SEARCH_TWO = 2
    BINARY_SEARCH_THREE = 3
    BINARY_SEARCH_FOUR = 4
    BINARY_SEARCH_FIVE = 5
    
