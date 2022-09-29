import tests
import sys
import avltree

def initialize_pq(size):
    return avltree.avltree()

tests.run_tests(sys.argv, initialize_pq)
