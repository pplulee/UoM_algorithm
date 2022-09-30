import sys

import general
from hashmap import hashmap_t
import airports
import weight
from sp_algorithms import bfs, bellman_ford, dijkstra, astar_search
from shortest_path import sssp_result_t

def msg0(s):
    general.msg(0, s)
def msg1(s):
    general.msg(1, s)
    
count = 0
    
def count_aux(u, visited):
    global count
    if (visited[u]):
        return
    visited[u] = True
    count = count + 1
    
    g = airports.ap_get_graph()
    
    for tgt in g.get_graph_succs(u):
        count_aux(tgt.v, visited)

def count_reachable(code):
    id = airports.ap_get_id(code)
    visited = [False]*airports.ap_get_num_ids()
    
    count_aux(id, visited)
    
    print("%d airports reachable from %s" % (count, code))
    
def path_dist(p):
    dist = weight.weight_t(0)
    
    for i in range(0, p.path_len()-1):
        dist = weight.weight_add(dist, airports.ap_get_dist(p.path_get(i), p.path_get(i+1)))
        
    return dist
    
def print_ap_path(p):
    for i in range(1, p.path_len()):
        u = p.path_get(i-1)
        v = p.path_get(i)
        print("%s to %s (%dkm)" % (airports.ap_get_code(u), airports.ap_get_code(v), airports.ap_get_dist(u, v).weight_to_int()))
        
def print_route(res):
    if (res.path != None):
        print_ap_path(res.path)
        print("Total = %dkm" % path_dist(res.path).weight_to_int())
    else:
        print("No route from %s to %s" % (airports.ap_get_code(res.src), airports.ap_get_code(res.dst)))
    msg0("relaxed %d edges\n" % res.relax_count)
    
def compute_route(algo, scode, dcode):
    s = airports.ap_get_id(scode)
    d = airports.ap_get_id(dcode)
    g = airports.ap_get_graph()
    
    h = [None]*g.graph_get_num_nodes()
    for u in range(0, g.graph_get_num_nodes()):
        if (airports.ap_is_valid_id(u)):
            h[u] = airports.ap_get_dist(u,d)
        else:
            h[u] = weight.weight_inf()
    
    if (algo == "bellman-ford"):
        print_route(bellman_ford(g,s).sssp_to_sp_result(d))
    elif (algo == "dijkstra"):
        print_route(dijkstra(g,s,d).sssp_to_sp_result(d))
    elif (algo == "astar"):
        print_route(astar_search(g,s,d,h))
    elif (algo == "bfs"):
        print_route(bfs(g,s,d).sssp_to_sp_result(d))
    else:
        general.error("Invalid algorithm name: %s" % algo)
    
airports.ap_std_init()

if (len(sys.argv) == 5 and sys.argv[1] == "route"):
    compute_route(sys.argv[2], sys.argv[3], sys.argv[4])
elif (len(sys.argv) == 3 and sys.argv[1] == "count"):
    count_reachable(sys.argv[2])
else:
    general.error("Invalid command line")
    
    
