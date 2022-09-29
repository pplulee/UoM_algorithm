from enum import Enum
import config
import sys

class darray:
    def __init__(self):
        self.array = []
        self.sorted = False
        
    def insert(self, string):
        self.array.append(string)
        
        # changing the array means it may no longer be sorted
        self.sorted = False
        
    def find(self, value):
        if (config.mode == SearchModes.LINEAR_SEARCH.value):
            for string in self.array:
                if (value == string):
                    return True
            return False
        else:
            if (not self.sorted):
                if (config.verbose > 0):
                    print("Dynamic Array not sorted, sorting... \n")
                    
                self.sort(config.mode)
                if (config.verbose > 0):
                    print("Dynamic Array sorted\n")
                
                self.sorted = True
            first = 0
            last = len(self.array) - 1
            middle = int((first + last)/2)
            
            while (first <= last):
                if (self.array[middle] < value):
                    first = middle + 1
                elif (self.array[middle] == value):
                    return True
                else:
                    last = middle - 1
                middle = int((first + last)/2)
                
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
        n = len(self.array)
        for i in range(n):
            key = self.array[i]
            j = i - 1
            while (j >= 0 and self.array[j] > key):
                self.array[j + 1] = self.array[j]
                j = j - 1
            self.array[j + 1] = key
            
        
    # Hint: you probably want to define a help function for the recursive call
    def quick_sort_recursive(self, start, end):
        if (start >= end):
            return
        mid = self.array[end]
        left = start
        right = end - 1
        while (left < right):
            while (self.array[left] < mid and left < right):
                left = left + 1
            while (self.array[right] >= mid and left < right):
                right = right - 1
            self.swap(left, right)
            
        if (self.array[left] >= self.array[end]):
            self.swap(left, end)
        else:
            left = left + 1
        
        if (left > 0):
            self.quick_sort_recursive(start, left - 1)
        self.quick_sort_recursive(left + 1, end)
    
    def quick_sort(self):
        self.quick_sort_recursive(0, len(self.array) - 1)

            
    
            
    
class SearchModes(Enum):
    LINEAR_SEARCH = 0
    BINARY_SEARCH_ONE = 1
    BINARY_SEARCH_TWO = 2
    BINARY_SEARCH_THREE = 3
    BINARY_SEARCH_FOUR = 4
    BINARY_SEARCH_FIVE = 5
    
