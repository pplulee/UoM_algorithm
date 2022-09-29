import concat_finder
import sys
sys.path.append("..")
import skiplist

def initialize_pq(size):
    return skiplist.skiplist()

concat_finder.concat_finder(sys.argv, initialize_pq)
