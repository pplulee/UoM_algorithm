import sys
import random
import math

import general
import weight
from weight import weight_t
from graph import graph_t, edge_tgt_t, INVALID_NODE
from pq import DPQ_t
from hashmap import hashmap_t
from hashmap import HashingModes
from sp_algorithms import bfs, bellman_ford, dijkstra, astar_search

def msg0(s):
    general.msg(0, s)
def msg1(s):
    general.msg(1, s)

def randrawweight(mn,mx):
    assert(weight.WEIGHT_MIN <= mn and mx <= weight.WEIGHT_MAX)
    res = random.randrange(mn, mx+1)
    assert(mn <= res and res <= mx)
    return res

def randweight(p_inf,mn,mx):
    if (random.random()<p_inf):
        return weight.weight_inf()
    else:
        return weight.weight_t(randrawweight(mn, mx))

def randname(length):
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    
    s = "";
    for i in range(0,length):
        end=len(alpha)
        s+=alpha[random.randrange(end)]
        
    s += "0"
    return s

def rand_graph(N, p_edge, min_weight, max_weight):
    g = graph_t(N)
    
    for u in range(0, N):
        for v in range(0, N):
            if (not u == v and random.random() < p_edge):
                w = weight_t(random.randrange(min_weight, max_weight+1))
                g.graph_add_edge(u, w, v)
    return g

class point_t:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class map_graph_t:
    def __init__(self, g, coords):
        self.g = g
        self.coords = coords

def coords_dist(coords, u, v):
    dx = coords[u].x - coords[v].x
    dy = coords[u].y - coords[v].y
    
    return weight.weight_t(round(math.sqrt(dx*dx + dy*dy)))

def rand_map_graph(N, dim, p_edge):
    g = graph_t(N)
    coords = [point_t(0, 0)]*N
    
    for u in range(0, N):
        coords[u].x = random.random()*dim
        coords[u].y = random.random()*dim
        
    for u in range(0, N):
        for v in range(0, N):
            if (not u == v and random.random() < p_edge):
                dx = coords[u].x - coords[v].x
                dy = coords[u].y - coords[v].y
    
                w = weight.weight_t(round(math.sqrt(dx*dx + dy*dy)))
                g.graph_add_edge(u, w, v)
                
    return map_graph_t(g, coords)
                
def testDPQ():
    N = 1000
    pq = DPQ_t(N)
    
    # Fill queue
    total = weight.weight_t(0)
    
    for i in range(0, N):
        w = pq.DPQ_prio(i)
        assert w.weight_is_inf(), "Initially, all priorities must be infinite"
        
        if (not i%10 == 0):
            w = randweight(.01,-10000,10000)
            if (not w.weight_is_inf()):
                total = weight.weight_add(total, w)
            pq.DPQ_insert(i,w)
                
    # Check membership, and total value
    total2 = weight.weight_t(0)
    for i in range(0, N):
        assert(pq.DPQ_contains(i) == (not i%10 == 0))
        if (pq.DPQ_contains(i)):
            w = pq.DPQ_prio(i)
            if (not w.weight_is_inf()):
                total2 = weight.weight_add(total2, w)
    
    assert(weight.weight_eq(total2, total))
        
    # Decrease some keys
    total = weight.weight_t(0)
    for i in range(1, N):
        if (pq.DPQ_contains(i)):
            w = pq.DPQ_prio(i)
            ch = False
            
            if (random.random() < 0.5):
                if (w.weight_is_inf()):
                    w = randweight(0, -10000, 10000)
                else:
                    w = randweight(0,-11000,w.weight_to_int() - 1)
                ch = True
                    
            if (not w.weight_is_inf()):
                total = weight.weight_add(total, w)
            if (ch):
                pq.DPQ_decrease_key(i, w)
                    
            assert(weight.weight_eq(pq.DPQ_prio(i), w))
            
    # Check membership and total value
    total2 = weight.weight_t(0)
    for i in range(0, N):
        if (pq.DPQ_contains(i)):
            w = pq.DPQ_prio(i)
            if (not w.weight_is_inf()):
                total2 = weight.weight_add(total2, w)
                    
    assert(weight.weight_eq(total2, total))
        
    total2 = weight.weight_t(0)
        
    assert(not pq.DPQ_is_empty())
    u = pq.DPQ_pop_min()
    last = pq.DPQ_prio(u)
    if (not last.weight_is_inf()):
        total2 = weight.weight_add(total2, last)
            
    while (not pq.DPQ_is_empty()):
        u = pq.DPQ_pop_min()
        w = pq.DPQ_prio(u)
        assert(not weight.weight_less(w, last))
        last = w
        if (not last.weight_is_inf()):
            total2 = weight.weight_add(total2, last)
            
    assert(weight.weight_eq(total2, total))

def test_hashmap(mode):
    N = 1000
    keys = [None] * N
    
    m = hashmap_t(2, mode)
    
    for i in range(0, N):
        name = randname(random.randrange(1, 49))
        name += str(i)
        
        keys[i] = name
        m.hashmap_insert(keys[i], i)
        
        if (not m.hashmap_contains(keys[i])):
            print("CONTAINS-KEY: %s" % keys[i])
            m.hashmap_print_set()
            assert(false)
    
    assert(m.hashmap_get_size() == N)
    
    for i in range(0, N):
        assert(m.hashmap_contains(keys[i]))
        v = sys.maxsize
        v = m.hashmap_lookup(keys[i])
        if (v == None):
            assert(false)
            
        assert(v == i)
        
    for i in range(0, N):
        name = randname(random.randrange(1, 49))
        assert(not m.hashmap_contains(name))
        
def compute_weight_matrix(g, N):
    w = [None]*N
    
    for u in range(0, N):
        w[u] = [None]*N
        for v in range(0, N):
            w[u][v] = weight.weight_inf()

    for u in range(0, N):
        for tgt in g.get_graph_succs(u):
            w[u][tgt.v] = tgt.w
            
    return w
    
class path_info_t:
    def __init__(self, w, len, src, dst):
        self.weight = w
        self.len = len
        self.src = src
        self.dst = dst

def compute_path_info(g, p):
    res = path_info_t(weight.weight_zero(), 0, INVALID_NODE, INVALID_NODE)
    N = g.graph_get_num_nodes()
    
    if (p.path_len() == 0):
        return res
        
    # Build weight matrix
    w = compute_weight_matrix(g, N)
    
    u = p.path_get(0)
    
    res.src = u
    
    for i in range(1, p.path_len()):
        v = p.path_get(i)
        res.len = res.len + 1
        res.weight = weight.weight_add(res.weight, w[u][v])
        u = v
        
    res.dst = u
    # res.weight = weight.weight_add(res.weight, weight.weight_t(1)) - for check error message at end of check_sp_result
    return res
    

def check_sp_result(g, src, dst, real_dist, r):
    assert (weight.weight_eq(r.dist, real_dist)), "The weight of the path (dist) as calculated by the comparison algorithm (Dijkstra and/or Bellman-Ford) does not match weight of the path in the result of your algorithm: comparison calculation (%d) != result returned (%d)" % (real_dist.w,r.dist.w)
    
    assert (src == r.src and dst == r.dst), "Test Failed: The result returned by your algorithm doesn't state its source (src) and destination (dst) as the same nodes we supplied for the test."
    
    if (r.path == None and r.dist.weight_is_inf()):
        assert (not src == dst), "Test Failed: Your result gives the distance between source and destination (dist) as infinite even though they are the same node in this test."
        # No check for actual unreachability
        return
        
    # If reachable, we expect a path and a finite distance
    assert (r.path != None and not r.dist.weight_is_inf()), "Test Failed: Your result contains a proposed path (path) but also states that the distance (dist) from source to destination is infinite."
    
    pi = compute_path_info(g, r.path)
    
    # Path must go from src to dst
    assert (pi.src == src and pi.dst == dst)
    
    # Its weight must match the claimed distance
    assert (weight.weight_eq(pi.weight, r.dist)), "The weight of the path as calculated by this test does not match weight of the path in the result of your algorithm (dist): test calculation (%d) != result returned (%d)" % (pi.weight.w,r.dist.w)

def check_sssp_result(g, src, r):
    N = g.graph_get_num_nodes()
    assert(r.N == N), "Test Failed: Your result says the graph contains a different number of nodes (N) than the test case supplied."
    
    msg1("checking shortest path")
    
    assert(not r.dist == None and not r.pred == None), "Test Failed: Either your distance (dist) is null or your predecessor map (pred) is null."
    
    assert(src == r.src and r.dst == INVALID_NODE), "Test Failed: Either your result source node (src) is not the one we supplied or the destination node (dst) is not equal to INVALIDE_NODE."
    
    #
    #   Certification Algorithm
    #
    #  === Reachability ===
    #    A node is reachable, iff its distance is not +inf.
    #    To verify reachability, we assert that there is no edge from a reachable to an unreachable node, and that src is reachable.
    #
    #  === Distance not too long ===
    #    The distance of the start node must be 0, or -inf.
    #    We check that no edge can be relaxed, i.e., that for every edge (u,v), we have dist[u] + w(u,v) >= dist[v].
    #    This property guarantees that the specified distances are not too long.
    #    NOTE: This also works for nodes on negative cycles: Setting their distance to -inf is the only
    #           way that every node on the negative cycle can be stable.

    #   === Pred map correct ===
    #     pred[u] must be INVALID_NODE for unreachable nodes.
    #     for reachable nodes, (pred[u],u) must be an edge.
    #      EXCEPTION: Start node, if finite distance: Here, pred[src]=src
    #
    #  === Distances not too short (finite) ===
    #    For nodes u with finite distance, we check that dist[pred[u]] + w(pred[u],u) == dist[u].
    #      EXCEPTION: Start node with finite distance
    #
    #
    #  === Distances not too short (negative weight cycles) ===
    #    For nodes with -inf distance, we actually follow the predecessor map to find a negative weight cycle
    #
  
    w = compute_weight_matrix(g, N)
    
    if (r.has_negative_cycle):
        msg1("Negative cycle reported")
        
    assert (r.dist[src].weight_is_neg_inf() or weight.weight_eq(r.dist[src], weight.weight_zero())), "Test failed: the distance to the start node is not 0, or -inf"
    
    has_neg_inf_dist = False # Will be set if we encounter node with -inf distance.  We'll compare that to result's negative weight cycle

    for u in range(0, N):
        # Check that edges cannot be relaxed, and do not go from reachable to unreachable
        for tgt in g.get_graph_succs(u):
            v = tgt.v
            ew = tgt.w
            
            assert (r.dist[u].weight_is_inf() or not r.dist[v].weight_is_inf()), "Test failed: found an edge in your distance map from a reachable to an unreachable node"
            
            assert (not ew.weight_is_inf()) # If this fails something is fishy with the graph: Edges shouldn't have infinite weight!
            
            rd = weight.weight_add(r.dist[u], ew) # Relax distance for node v
            
            assert (not weight.weight_less(rd, r.dist[v])), "Test failed:  Found an edge %d -(%d)-> %d in your calculated distance map that is still relaxable.  The distance to %d is %d - adding the weight between  %d and %d gives %d which is less than your calculated distance to %d which is %d" % (u, ew.weight_to_int(), v, u, r.dist[u].w, u, v, rd.w, v, r.dist[v].w)
        
        #  Check for pred-map
        
        if (r.dist[u].weight_is_inf()):
            # Unreachable node
            assert(r.pred[u] == INVALID_NODE), "Test failed: Found a node with an infinite distance which has a predecessor in pred"
        elif (not r.dist[u].weight_is_neg_inf()):
            # Reachable node, not over negative-weight cycle
            pu = r.pred[u]
            
            assert(pu < N)
            if (u == src):
                assert(pu == src) # Special case: pred of source points to itself
            else:
                ew = w[pu][u]
                assert (ew.weight_is_finite()), "Test failed.  Two nodes that are not connected appear in your predecessor map: %d -> %d (weight=%d) appears in your map but these nodes are not connected." %(pu, u, w[pu][u].w)
                rd = weight.weight_add(r.dist[pu], ew) # Relax distance for node u
                
                assert(weight.weight_eq(rd, r.dist[u])), "Test failed.  Found two adjacent nodes, u and v, on your shortest path where the distance to u plus the edge weight between it and v is not equal to the distance to v." # Estimates for edges on shortest path must be precise
        else:
            # Reachable node, over negative-weight cycle
            has_neg_inf_dist=True
            
            pu = r.pred[u]
            ew = w[pu][u]
            assert(pu < N), "Test Failed.  The predecessor to a node is not a node in the graph."
            
            assert (ew.weight_is_finite()), "Test failed.  Two nodes that are not connected appear in your predecessor map: %d -> %d (weight=%d) appears in your map but these nodes are not connected." %(pu, u, w[pu][u].w)
            
            # Follow the cycle
            # Take N steps to make sure we are actually on the cycle
            for i in range(0, N):
                pu = r.pred[pu]
                assert(pu < N), "Test Failed.  The predecessor to a node is not a node in the graph."
                
            # Now do another round through the cycle, computing its weight
            pw = weight.weight_add(weight.weight_zero(), w[r.pred[pu]][pu])
            v = r.pred[pu]
            while (not v == pu):
                pw = weight.weight_add(pw, w[r.pred[v]][v])
                v = r.pred[v]
                
            assert(weight.weight_less(pw, weight.weight_zero())), "Test failed. Found a negative cycle with a positive weight." 
        
    assert(has_neg_inf_dist == r.has_negative_cycle), "Test failed.  Either you have a negative infinite distance in your solution and have not reported a negative cycle or vice versa."
            

def check_sssp_result_compat(r1, r2):
    assert (r1.N == r2.N)
    N = r1.N
    for u in range(0, N):
        assert(weight.weight_eq(r1.dist[u], r2.dist[u])), "Test failed.  Comparing two solutions which give different distances to the same node in the graph."

TEST_HASHMAP = 1
TEST_PQ = 2
TEST_BFS = 4
TEST_BELLMAN_FORD = 8
TEST_BELLMAN_FORD_NEG = 16
TEST_DIJKSTRA = 32
TEST_ASTAR = 64

do_tests = 0

def check_sssp_algos(g, src, dst, negative):
    r1 = None
    r2 = None
    
    d = weight.weight_inf()
    
    if (not negative and (do_tests & TEST_DIJKSTRA)):
        msg1("Dijkstra")
        r1 = dijkstra(g, src, INVALID_NODE)
        check_sssp_result(g, src, r1)
        d = r1.dist[dst]
    
    if (do_tests & TEST_BELLMAN_FORD):
        msg1("Bellman-Ford")
        r2 = bellman_ford(g, src)
        check_sssp_result(g, src, r2)
        d = r2.dist[dst]
    
    if (not r1 == None and not r2 == None):
        msg1("Checking both Dijstra and Bellman-Ford return the same result")
        check_sssp_result_compat(r1, r2)
        
    return d

def graph_unweighted_of(g):
    N = g.graph_get_num_nodes()
    gg = graph_t(N)
    
    for u in range(0, N):
        for tgt in g.get_graph_succs(u):
            gg.graph_add_edge(u, weight_t(1), tgt.v)
            
    return gg

def do_graph_check(N, p, mn, mx):
    msg1("graph check %d %f [%d..< %d]" % (N, p, mn, mx))
    
    g = rand_graph(N, p, mn, mx)
    
    check_sssp_algos(g, 0, 0, mn<0)
    
    if (do_tests & TEST_BFS):
        msg1("BFS")
        ug = graph_unweighted_of(g)
        r = bfs(ug, 0, INVALID_NODE)
        check_sssp_result(ug, 0, r)
    

def do_map_graph_check(N, p, src, dst):
    assert (src<N and dst<N)
    
    if (not (do_tests & TEST_ASTAR)):
        return
    if (not do_tests & (TEST_DIJKSTRA | TEST_BELLMAN_FORD)):
        general.error("For testing A*, you must also test Dijkstra and/or Bellman-Ford!")
    
    msg1("map graph check %d %f %d ->* %d" % (N, p, src, dst))
    
    mg = rand_map_graph(N, 10000, p)
    
    real_dist = check_sssp_algos(mg.g, src, dst, False)
    
    h = [None]*N
    for u in range(0, N):
        h[u] = coords_dist(mg.coords, u, dst)
        
    msg1("A*")
    
    r = astar_search(mg.g, src, dst, h)
    
    check_sp_result(mg.g, src, dst, real_dist, r)

def reseed_rand():
    random.seed(789231)

general.set_msg_verb(-1)

for i in range(1, len(sys.argv)):
    if (sys.argv[i] == "hashmap"):
        do_tests |= TEST_HASHMAP
    elif (sys.argv[i] == "pq"):
        do_tests |= TEST_PQ
    elif (sys.argv[i] == "bfs"):
        do_tests |= TEST_BFS
    elif (sys.argv[i] == "bellman-ford"):
        do_tests |= TEST_BELLMAN_FORD
    elif (sys.argv[i] == "bellman-ford-neg"):
        do_tests |= TEST_BELLMAN_FORD | TEST_BELLMAN_FORD_NEG
    elif (sys.argv[i] == "dijkstra"):
        do_tests |= TEST_DIJKSTRA
    elif (sys.argv[i] == "astar"):
        do_tests |= TEST_ASTAR
    elif (sys.argv[i] == "-v"):
        general.set_msg_verb(0)
    elif (sys.argv[i] == "-vv"):
        general.set_msg_verb(1)
    elif (sys.argv[i] == "-vvv"):
        general.set_msg_verb(2)
    else:
        general.error("Unknown command line option: %s" % sys.argv[i])
        
if (do_tests & TEST_HASHMAP):
    msg0("Testing Hashmap Implementation")
    reseed_rand()
    for i in range(0, 200):
        test_hashmap(HashingModes.HASH_1_LINEAR_PROBING)
        test_hashmap(HashingModes.HASH_1_DOUBLE_HASHING)
        test_hashmap(HashingModes.HASH_1_QUADRATIC_PROBING)
        
if (do_tests & TEST_PQ):
    msg0("Testing Priority Queue Implementation")
    reseed_rand()
    for i in range(0,1000):
        testDPQ()
    
GRAPH_TESTS = TEST_ASTAR | TEST_BELLMAN_FORD | TEST_BFS | TEST_DIJKSTRA
    
if (do_tests & GRAPH_TESTS):
    msg0("Testing shortest path algorithms on random graphs.")

    msg0("Random graphs of size 100 with Positive weights")
    reseed_rand()
    eprob = 1.0
    for i in range(0,8):
        do_graph_check(100, eprob, 0, 10000)
        eprob = eprob/2
        
    if (do_tests & TEST_BELLMAN_FORD_NEG):
        msg0("Random graphs of size 100 with both Postive and Negative weights")
        reseed_rand()
        eprob = 1.0
        for i in range(0, 8):
            do_graph_check(100, eprob, -10000, 10000)
            eprob = eprob/2
        
        msg0("Corner case: Random graphs of size 100 with All negative weights")
        reseed_rand()
        eprob = 1.0
        for i in range(0, 8):
            do_graph_check(100, eprob, -10000, 0)
            eprob = eprob/2
    
    msg0("Corner case: All zero")
    reseed_rand()
    eprob  = 1.0
    for i in range(0,8):
        do_graph_check(100, eprob, 0, 0)
        eprob = eprob/2

    msg0("Corner case: Random graph of size 100 where all weights are zero")
    reseed_rand()
    do_graph_check(1, 0, 0, 0)
    do_map_graph_check(1, 0, 0, 0)
    
    if (do_tests & TEST_ASTAR):
        msg0("Testing A*: Random map-like graphs of size 100.")
        msg0("Testing A*: These tests will be compared against the output of Dijsktra or Bellman-ford so one of these must be tested at the same time.")
        reseed_rand()
        eprob  = 1.0
        for i in range(0,8):
            do_map_graph_check(100, eprob, 0, 1)
            eprob = eprob/2

