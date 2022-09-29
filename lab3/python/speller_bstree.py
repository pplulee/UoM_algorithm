import speller
import sys
import config

sys.setrecursionlimit(10005)

config.set_type = config.SetType.BSTREE
config.prog_name = "speller_bstree.py"

speller.spelling(sys.argv)
