import sorting
import sys
sys.path.append("..")
import binaryheap

def initialize_pq(size):
    return binaryheap.binaryHeap(size)

sorting.sorting(sys.argv, initialize_pq)
