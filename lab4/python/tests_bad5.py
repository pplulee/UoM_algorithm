import tests
import sys
# Modify this line with the bad implementation you want to check
import bad5 as bad

def initialize_pq(size):
    return bad.llist()

tests.run_tests(sys.argv, initialize_pq)

