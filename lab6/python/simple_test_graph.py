import sys

import general
from hashmap import hashmap_t
from graph import graph_t
import weight
from sp_algorithms import bfs, bellman_ford, dijkstra, astar_search
from shortest_path import sssp_result_t, print_path

def msg0(s):
    general.msg(0, s)
def msg1(s):
    general.msg(1, s)
    
    
def compute_path(algo, src, dst):
    s = int(src)
    d = int(dst)
    g = graph_t(10)
    g.graph_add_edge(0, weight.weight_t(1), 1)
    g.graph_add_edge(1, weight.weight_t(2), 2)
    g.graph_add_edge(2, weight.weight_t(3), 3)
    g.graph_add_edge(3, weight.weight_t(1), 4)
    g.graph_add_edge(5, weight.weight_t(1), 6)
    g.graph_add_edge(6, weight.weight_t(1), 8)
    g.graph_add_edge(8, weight.weight_t(2), 9)
    g.graph_add_edge(5, weight.weight_t(9), 9)
    if (algo == "bellman-ford-neg"):
        g.graph_add_edge(3, weight.weight_t(-1), 0)
        g.graph_add_edge(5, weight.weight_t(-5), 7)
    else:
        g.graph_add_edge(3, weight.weight_t(4), 0)
        g.graph_add_edge(5, weight.weight_t(5), 7)
        
    
    h = [None]*g.graph_get_num_nodes()
    for u in range(0, g.graph_get_num_nodes()):
        h[u] = weight.weight_t(abs(d - u))
    
    if (algo == "bellman-ford"):
        bellman_ford(g,s).sssp_to_sp_result(d).print_sp_result(sys.stdout)
    elif (algo == "bellman-ford-neg"):
        bellman_ford(g,s).sssp_to_sp_result(d).print_sp_result(sys.stdout)
    elif (algo == "dijkstra"):
        dijkstra(g,s,d).sssp_to_sp_result(d).print_sp_result(sys.stdout)
    elif (algo == "astar"):
        astar_search(g,s,d,h).print_sp_result(sys.stdout)
    elif (algo == "bfs"):
        bfs(g,s,d).sssp_to_sp_result(d).print_sp_result(sys.stdout)
    else:
        general.error("Invalid algorithm name: %s" % algo)
    
if (len(sys.argv) == 4):
    compute_path(sys.argv[1], sys.argv[2], sys.argv[3])
elif (len(sys.argv) == 5):
    if (sys.argv[4] == "-v"):
        general.set_msg_verb(0)
    elif (sys.argv[4] == "-vv"):
        general.set_msg_verb(1)
    elif (sys.argv[4] == "-vvv"):
        general.set_msg_verb(2)
    compute_path(sys.argv[1], sys.argv[2], sys.argv[3])

else:
    general.error("Invalid command line")
    
    
