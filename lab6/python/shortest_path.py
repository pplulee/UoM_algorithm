from graph import graph_t, path_t, INVALID_NODE
from pq import DPQ_t
# import sp_algorithms

#
 # The main components of a single-source shortest path result are a predecessor map and a distance map (encoded as arrays).
 #
 # The distance map assigns each node to its distance from the source node.
 #    If the node is unreachable, the distance is inf.
 #    If the node is reachable via a negative weight cycle, the distance is -inf.
 #
 # The predecessor map assigns nodes to predecessor nodes on a shortest path or negative cycle.
 #    If the node is unreachable, the predecessor must be INVALID_NODE.
 #    If the node has finite distance, its predecessor must be the previous node on a shortest path. EXCEPTION: The predecessor of the start node is the start node itself.
 #    If the node has -inf distance, following the predecessors must yield a negative-weight cycle. NOTE: In this case, there is no exception for the start node!
 #
 #/
class sssp_result_t:
    def __init__(self, N, src, dst, ncyc, p, d, c):
        self.N = N # Number of nodes, to make result more self contained
        self.src = src # Start node
        self.dst = dst # If != INVALID_NODE, this is a partial result, only accurate for dst
        self.pred = p # Predecessor map
        self.has_negative_cycle = ncyc # True if negative cycle was detected. Pred and dist are NULL then.
        self.dist = d # Distance map
        self.relax_count=c # Number of relaxed edges
        
    # Convert sssp to sp result.
    def sssp_to_sp_result(self, dst):
        p = None
        
        assert(self.dst == INVALID_NODE or self.dst == dst)
        
        if (not self.pred[dst] == INVALID_NODE):
            p = path_t(self.pred,dst)
            
        r = sp_result_t(self.src, dst, p, self.dist[dst], self.relax_count)
        
        return r
        
    def print_sssp_result(self, f):
        N = self.N
        if (N<10):
            NN = N
        else:
            NN = 10
       
        f.write("Distmap:")
        for i in range(0, NN):
            f.write(" ")
            self.dist[i].print_weight(f)
        
        if (N < NN):
            f.write("...\n")
        else:
            f.write("\n")
        
        
##
 # Structure describing the result of a shortest path search between two nodes
 #/        
class sp_result_t:
    def __init__(self, src, dst, p, d, c):
        self.src = src                      # Start node
        self.dst = dst                       # Target node
        self.path = p                     # Result path, None if unreachable
        self.dist = d                   # Distance, INF if unreachable
        self.relax_count = c   # Number of relaxed edges
        
    def print_sp_result(self, f):
        f.write("Distance: ")
        self.dist.print_weight(f)
        f.write("\n")
        
        f.write("Path: ")
        print_path(f, self.path)
        f.write("\n")
        
        f.write("# Relaxed nodes: %d\n" % (self.relax_count))
        
def print_path(f, p):
    if (p == None):
        f.write("NULL")
    elif (p.path_len() == 0):
        f.write("EMP")
    else:
        f.write("%d " % (p.path_get(0)))
        for i in range(1, p.path_len()):
            f.write("%d " % (p.path_get(i)))
            

        

