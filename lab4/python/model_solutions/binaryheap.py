import sys

# 0-based operations
# This could be updated to be 1-based if you wanted, what else would need to change?
FIRST = 0

def parent(i):
    return int((i - 1)/2)
def left(i):
    return (2*i) +1
def right(i):
    return (2*i) + 2

class binaryHeap:
    def __init__(self, size):
        self.num_elem = size
        self.heap_size = 0
        # This isn't a very pythonic way of doing things but we are following the c code
        self.weights = [None]*size
        self.elements = [None]*size
        
    # Helper function for swapping nodes in the tree
    def swap(self, i, j):
        t = self.elements[i]
        self.elements[i] = self.elements[j]
        self.elements[j] = t
        
        w = self.weights[i]
        self.weights[i] = self.weights[j]
        self.weights[j] = w
        
    def sift_up(self, i):
        while (i > 0 and self.weights[i] < self.weights[parent(i)]):
            self.swap(i, parent(i))
            i = parent(i)
        
    def sift_down(self, i):
        while (True):
            l = left(i)
            r = right(i)
            if (l >= self.heap_size and r >= self.heap_size):
                # No children, we're finisehd
                return
                
            smallest = l
            if (r < self.heap_size and self.weights[r] < self.weights[l]):
                smallest = r
                
            if (self.weights[smallest] < self.weights[i]):
                self.swap(i, smallest)
            else:
                # children not smaller, we're finished
                return
                
            i = smallest
            
    def contains(self, u, priority):
        # Linear Search required as unordered
        for i in range(FIRST, self.heap_size):
            if (self.elements[i] == u and self.weights[i] == priority):
                return True
        return False
        
    def expand(self):
        self.num_elem = self.num_elem*2
        # Not very pythonic but following the c code
        new_weights = [None]*self.num_elem
        new_elements = [None]*self.num_elem
        for i in range(len(self.weights)):
            new_weights[i] = self.weights[i]
            new_elements[i] = self.elements[i]
        self.weights=new_weights
        self.elements = new_elements
        
        
        
    def last_idx(self):
        last = self.heap_size
        # if we ever query outside the heap just expand it
        if (last >= self.num_elem):
            self.expand()
        return last
        
    def insert(self, u, w):
        li = self.last_idx()
        self.weights[li] = w
        self.elements[li] = u
        
        self.sift_up(li)
        
        self.heap_size = self.heap_size + 1
        
    def is_empty(self):
        return self.heap_size == 0
        
    def pop_min(self):
        if (self.is_empty()):
            sys.stderr.write("Error: pop_min from empty binaryHeap\n")
            sys.exit(-1)
            
        self.heap_size = self.heap_size - 1
        li = self.last_idx()
        self.swap(FIRST, li)
        res = self.elements[li]
        self.sift_down(FIRST)
        return res
        
    def print(self):
        sys.stderr.write("BinaryHeap has %d elements with %d size\n" % (self.num_elem, self.heap_size))
        for i in range(FIRST, self.heap_size):
            sys.stdout.write("(%s,%d)\n" % (self.elements[i], self.weights[i]))

    
