import sorting
import sys
sys.path.append("..")
import llist1

def initialize_pq(size):
    return llist1.llist()

sorting.sorting(sys.argv, initialize_pq)
