import tests
import sys
import llist2

def initialize_pq(size):
    return llist2.llist()

tests.run_tests(sys.argv, initialize_pq)
