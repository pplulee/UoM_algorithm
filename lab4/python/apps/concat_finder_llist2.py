import concat_finder
import sys
sys.path.append("..")
import llist2

def initialize_pq(size):
    return llist2.llist()

concat_finder.concat_finder(sys.argv, initialize_pq)
