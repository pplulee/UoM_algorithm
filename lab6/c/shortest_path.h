#ifndef _SHORTEST_PATH_H
#define _SHORTEST_PATH_H

#include "graph.h"


// typedef enum _algorithm_t {
//   ALGO_DIJKSTRA,
//   ALGO_ASTAR,
//   ALGO_BELLMAN_FORD,
//   ALGO_BFS
// } algorithm_t;

/*
 * The main components of a single-source shortest path result are a predecessor map and a distance map (encoded as arrays).
 *
 * The distance map assigns each node to its distance from the source node.
 *    If the node is unreachable, the distance is inf.
 *    If the node is reachable via a negative weight cycle, the distance is -inf.
 *
 * The predecessor map assigns nodes to predecessor nodes on a shortest path or negative cycle.
 *    If the node is unreachable, the predecessor must be INVALID_NODE.
 *    If the node has finite distance, its predecessor must be the previous node on a shortest path. EXCEPTION: The predecessor of the start node is the start node itself.
 *    If the node has -inf distance, following the predecessors must yield a negative-weight cycle. NOTE: In this case, there is no exception for the start node!
 *
 */

typedef struct _sssp_result_t {
  size_t N;                         /// Number of nodes, to make result more self contained
  node_t src;                       /// Start node
  node_t dst;                       /// If != INVALID_NODE, this is a partial result, only accurate for dst
  bool has_negative_cycle;          /// True if negative cycle was detected. Pred and dist are NULL then.
  node_t *pred;                     /// Predecessor map
  weight_t *dist;                   /// Distance map
  unsigned long long relax_count;   /// Number of relaxed edges
} sssp_result_t;

sssp_result_t *sssp_result_new(size_t N, node_t src, node_t dst, bool ncyc, node_t *pred, weight_t *dist, unsigned long long relax_count);
void sssp_result_delete(sssp_result_t *);

/**
 * Structure describing the result of a shortest path search between two nodes
 */
typedef struct _sp_result_t {
  node_t src;                       /// Start node
  node_t dst;                       /// Target node
  path_t *path;                     /// Result path, NULL if unreachable
  weight_t dist;                    /// Distance, INF if unreachable
  unsigned long long relax_count;   /// Number of relaxed edges
} sp_result_t;

// Constructors and destructors

sp_result_t* sp_result_new(node_t src, node_t dst, path_t* p, weight_t, long long unsigned int c);
void sp_result_delete(sp_result_t *);

// apsp_result_t *compute_apsp(algorithm_t algo, graph_t const *g, node_t s);
// sp_result_t *compute_sp(algorithm_t algo, graph_t const *g, node_t s, node_t d, weight_t const *h);

// Auxiliary functions

/// Convert apsp to sp result, deleting a.
sp_result_t *sssp_to_sp_result(sssp_result_t *a, node_t dst);


void print_sp_result(sp_result_t const *r);
void print_sssp_result(FILE *f, sssp_result_t const *r);




#endif
