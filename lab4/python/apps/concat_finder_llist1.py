import concat_finder
import sys
sys.path.append("..")
import llist1

def initialize_pq(size):
    return llist1.llist()

concat_finder.concat_finder(sys.argv, initialize_pq)
