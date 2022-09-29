import tests
import sys
import binaryheap

def initialize_pq(size):
    return binaryheap.binaryHeap(size)

tests.run_tests(sys.argv, initialize_pq)
