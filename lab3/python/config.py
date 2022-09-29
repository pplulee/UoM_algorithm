from enum import Enum

class SetType(Enum):
    DARRAY = 1,
    BSTREE = 2,
    HASH = 3

set_type = SetType.DARRAY
prog_name = "speller_darray.py"
DEFAULT_DICT_FILE = "sample-dictionary"
verbose = 0
mode = 0
init_size = 509
