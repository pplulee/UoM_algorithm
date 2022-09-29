import concat_finder
import sys
sys.path.append("..")
import avltree

def initialize_pq(size):
    return avltree.avltree()

concat_finder.concat_finder(sys.argv, initialize_pq)
