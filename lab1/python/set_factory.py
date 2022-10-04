from darray import darray
#from bstree import bstree
#from hashset import hashset
import config
    
def initialise_set():
    if (config.set_type == config.SetType.DARRAY):
        return darray()

