import tests
import sys
import skiplist

def initialize_pq(size):
    return skiplist.skiplist()

tests.run_tests(sys.argv, initialize_pq)
