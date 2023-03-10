#
# 'make depend' uses makedepend to automatically generate dependencies
#               (dependencies are added to end of Makefile)
# 'make'        build executable file 'mycc'
# 'make clean'  removes all .o and executable files
#

# define the C compiler to use
CC = gcc

# define any compile-time flags
CFLAGS = -Wall -g

# define any directories containing header files other than /usr/include
#
INCLUDES =

# define library paths in addition to /usr/lib
#   if I wanted to include libraries not in /usr/lib I'd specify
#   their path using -Lpath, something like:
LFLAGS =

# define any libraries to link into executable:
#   if I want to link in libraries (libx.so or libx.a) I use the -llibname
#   option, something like (this will link in libmylib.so and libm.so:
LIBS = -lm

# define the C source files
# SRCS = main.c graph.c pq.c dijkstra.c general.c hashmap.c airports.c
SRCS = weight.c graph.c pq.c general.c hashmap.c airports.c sp_algorithms.c shortest_path.c

# define the C object files
#
# This uses Suffix Replacement within a macro:
#   $(name:string1=string2)
#         For each word in 'name' replace 'string1' with 'string2'
# Below we are replacing the suffix .c of all words in the macro SRCS
# with the .o suffix
#
OBJS = $(SRCS:.c=.o)

# define the executable file
MAIN = ap sp simple_graph_test

#
# The following part of the makefile is generic; it can be used to
# build any executable just by changing the definitions above and by
# deleting dependencies appended to the file from 'make depend'
#

.PHONY: depend clean

all:    $(MAIN)

$(MAIN): $(OBJS)

$(MAIN): %: %.o
	$(CC) $(CFLAGS) $(INCLUDES) $< $(OBJS) $(LFLAGS) $(LIBS) -o $@

# this is a suffix replacement rule for building .o's from .c's
# it uses automatic variables $<: the name of the prerequisite of
# the rule(a .c file) and $@: the name of the target of the rule (a .o file)
# (see the gnu make manual section about automatic variables)
.c.o:
	$(CC) $(CFLAGS) $(INCLUDES) -c $<  -o $@

clean:
	$(RM) *.o *~ $(MAIN) Makefile.bak

depend: $(SRCS)
	makedepend -Y $(INCLUDES) $^

# DO NOT DELETE THIS LINE -- make depend needs it

weight.o: general.h weight.h
graph.o: general.h graph.h weight.h
pq.o: general.h graph.h weight.h pq.h
general.o: general.h
hashmap.o: hashmap.h general.h
airports.o: hashmap.h general.h graph.h weight.h airports.h
sp_algorithms.o: graph.h weight.h pq.h general.h sp_algorithms.h
sp_algorithms.o: shortest_path.h
shortest_path.o: graph.h weight.h pq.h general.h shortest_path.h
shortest_path.o: sp_algorithms.h
