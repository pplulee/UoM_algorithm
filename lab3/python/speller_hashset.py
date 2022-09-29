import speller
import sys
import config

config.set_type = config.SetType.HASH
config.prog_name = "speller_hashset.py"

speller.spelling(sys.argv)
