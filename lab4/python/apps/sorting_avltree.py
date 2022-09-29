import sorting
import sys
sys.path.append("..")
import avltree

def initialize_pq(size):
    return avltree.avltree()

sorting.sorting(sys.argv, initialize_pq)
