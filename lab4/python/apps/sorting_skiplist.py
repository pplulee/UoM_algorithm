import sorting
import sys
sys.path.append("..")
import skiplist

def initialize_pq(size):
    return skiplist.skiplist()

sorting.sorting(sys.argv, initialize_pq)
