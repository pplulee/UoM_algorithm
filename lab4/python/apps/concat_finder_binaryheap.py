import concat_finder
import sys
sys.path.append("..")
import binaryheap

def initialize_pq(size):
    return binaryheap.binaryHeap(size)

concat_finder.concat_finder(sys.argv, initialize_pq)
