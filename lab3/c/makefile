CFLAGS=-g -Wall 
LDFLAGS=-lm
CC=gcc

# "make darray", "make bstree" or "make hash" to compile your code

bstree:
	$(CC) $(CFLAGS) -DBSTREE global.c speller.c bstree.c $(LDFLAGS) -o speller_bstree

hashset:
	$(CC) $(CFLAGS) -DHASH global.c speller.c hashset.c $(LDFLAGS) -o speller_hashset


tidy:
	-rm *.o speller_darray speller_bstree speller_hashset

.PHONY: bstree hashset

################################################################################
# Comment out the next line once you have debugged your code
RUN=valgrind
# Uncomment the next line to time your code (instead of using valgrind)
#RUN=time
# If you comment out both RUNs above you can run your program by itself

# to test: e.g. "make testdarray"

MODE=-m 0

# small dictionaries that give trees that are unbalanced in various ways
testtree: bstree
	$(RUN) ./speller_bstree -d data/LLdictionary $(MODE) -vvv data/sample-file-tree
	$(RUN) ./speller_bstree -d data/LRdictionary $(MODE) -vvv data/sample-file-tree
	$(RUN) ./speller_bstree -d data/RLdictionary $(MODE) -vvv data/sample-file-tree
	$(RUN) ./speller_bstree -d data/RRdictionary $(MODE) -vvv data/sample-file-tree
	@echo
	$(RUN) ./speller_bstree -d data/sample-dictionary $(MODE) -vv data/sample-file

testhash: hash
	$(RUN) ./speller_hashset -d data/sample-dictionary -s 13 $(MODE) -vv data/sample-file
	@echo "This mightd fail as the dictionary is bigger than the hashtable"
	$(RUN) ./speller_hashset -d data/sample-dictionary -s 5 $(MODE) -vvv data/sample-file

