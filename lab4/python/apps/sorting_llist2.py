import sorting
import sys
sys.path.append("..")
import llist2

def initialize_pq(size):
    return llist2.llist()

sorting.sorting(sys.argv, initialize_pq)
