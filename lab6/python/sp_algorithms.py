import graph
import pq
import general
from shortest_path import sssp_result_t, sp_result_t
import weight

def bfs(g, src, dst):
    stat_edges_explored = 0
    
    N = g.graph_get_num_nodes()
    pred = [graph.INVALID_NODE]*N
    dist = [weight.weight_inf()]*N
    
    general.error("Not implemented")
    
    return sssp_result_t(N, src, dst, False, pred, dist, stat_edges_explored)
    
def bellman_ford(g, src):
    general.error("Not implemented")
    
def dijkstra(g, src, dst):
    general.error("Not implemented")
    
def astar_search(g, src, dst, h):
    general.error("Not implemented")
