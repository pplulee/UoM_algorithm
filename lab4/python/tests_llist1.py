import tests
import sys
import llist1

def initialize_pq(size):
    return llist1.llist()

tests.run_tests(sys.argv, initialize_pq)
