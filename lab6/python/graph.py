import sys

import general

# Marker for invalid node.
INVALID_NODE = sys.maxsize

# Graph Data Structure

# def scan_node(f):

# def scan_raw_weight(f):

# def scan_weight(f):

##
 # Edge out from a node.
 #
 # Each successor is represented by a weight and a target node.
 #/
class edge_tgt_t:
    def __init__(self, w, v):
        self.w = w
        self.v = v

    def _tgt_is_invalid(self):
        return self.v == INVALID_NODE
            
class succs_t:
    def __init__(self):
        self.n = 0
        self.capacity = 0
        self.a = []
        
    def succs_add(self, tgt):
        if (self.n >= self.capacity):
            self.capacity = (self.capacity + 1)*2
            aa = [None]*self.capacity
            for i in range(0, self.n):
                aa[i] = self.a[i]
            self.a = aa
        assert(self.n < self.capacity)
        self.a[self.n] = tgt
        self.n = self.n + 1

# Class for graphs.
class graph_t:
    def __init__(self, num_nodes):
        assert(num_nodes < sys.maxsize)
        self.num_nodes = num_nodes
        if (not num_nodes == None):
            self.adjs = [None]*num_nodes
        else:
            self.adjs = None
        for i in range(0, num_nodes):
            self.adjs[i] = succs_t()
            
    def graph_check_node(self, u):
        if (not u < self.num_nodes):
            general.error("Node out of range: %d", u)

    ##
     # Get number of nodes.
     #/
    def graph_get_num_nodes(self):
        return self.num_nodes

    ##
    # Add edge to graph
    # @pre Nodes must be in range, i.e., u,v < num_nodes
    # @pre Weight must be finite
    # @pre Self-loop edges not allowed, i.e., u != v
    #/
    def graph_add_edge(self, u, w, v):
        assert (not (u == v)), "self loop edge %d -> %d" % (u, v)
        assert(w.weight_is_finite())
        
        self.graph_check_node(u)
        self.graph_check_node(v)
        
        self.adjs[u].succs_add(edge_tgt_t(w, v))

    ##
     # Get sucessors of specified node
     #
     # Each successor is represented by a weight and a target node.
     # One can query the number of successors, and array of successors
     #
     # For example, the following code snippet iterates over all successors of node u in graph g
     #
     #      for tgt in g.get_graph_succs(u):
     #          # use tgt.v and tgt.w to access target node and edge weight 
     #
     #/
    def graph_num_succs(self, u):
        return self.adjs[u].n
        
    def get_graph_succs(self, i):
        return self.adjs[i].a[0:self.adjs[i].n]
        
    # Create graph from file. The file is a text file containing the positive integer numbers:
    #
    # num_nodes
    # num_edges
    # u_1 v_1 w_1
    # ...
    #
    # i.e., the number of nodes, then the number of edges, and then, for each edge, the source node, target node, and weight.
    #
    # Everything content after the last edge will be ignored.
    #
    # The function outputs an error message for files not adhering to this format!
    #/
    # graph_read - not implemented since not needed for practcal

    ##
     # Write graph to file. Uses format described in @ref graph_read.
     #/
    def graph_write(self, f):
        N = self.graph_get_num_nodes()
        num_edges = 0
        
        for u in range(0, N):
            num_edges += self.graph_num_succs(u)
            
        f.write("%d\n%d\n" % (N, num_edges))
        
        for u in range(0, N):
            for tgt in self.get_graph_succs(u):
                if (not tgt == None):
                    f.write("%d %d %d\n" % (u, tgt.v, tgt.w.weight_to_int()))
                else:
                    f.write("NONE\n")
#/// Paths
##
 # A path is a sequence of nodes with a specified length.
 #/
class path_t:
    def set_up(self, len):
        self.len = len
        self.nodes = [None]*len
        for i in range(0, len):
            self.nodes[i] = INVALID_NODE

    ##
     # Extract path from predecessor array. Convention: Start node points to itself.
     #/
    def __init__(self, pred, v):
        # Determine length
        len = 0
        u = v
        
        while (True):
            len = len + 1
            if (u == pred[u]):
                break
            u = pred[u]
            
        self.set_up(len)
        u = v
        
        while (True):
            len = len - 1
            self.path_set(len, u)
            if (u == pred[u]):
                break
            u = pred[u]

    def path_set(self, i, u):
        assert (i < self.len)
        self.nodes[i] = u
    
    def path_get(self, i):
        assert(i < self.len)
        return self.nodes[i]
        
    def path_len(self):
        return self.len
        
        
        
