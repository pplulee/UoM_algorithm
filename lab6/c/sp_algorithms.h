#ifndef _SP_ALGORITHMS_H
#define _SP_ALGORITHMS_H

#include "shortest_path.h"

/**
 * Use BFS to compute APSP.
 * Edge weights are to be ignored, and the shortest paths in terms
 * of edge count shall be computed.
 *
 * If dst is not INVALID_NODE, the algorithm should stop as soon as it has computed a shortest path to dst.
 *
 */
sssp_result_t *bfs(graph_t const *g, node_t src, node_t dst);

/**
 * Use Bellman-Ford to compute shortest paths in a weighted graph.
 * For nodes reachable from infinite weight cycles, your algorithm
 * should report a distance of -inf, and the predecessor INVALID_NODE.
 *
 */
sssp_result_t *bellman_ford(graph_t const *g, node_t src);

/**
 * Use Dijkstra's algorithm to compute shortest paths in a weighted graph with
 * non-negative weights.
 *
 * If dst is not INVALID_NODE, the algorithm should stop as soon as it has computed a shortest path to dst.
 *
 * @pre Graph has no negative weights
 */
sssp_result_t *dijkstra(graph_t const *g, node_t src, node_t dst);

/**
 * Use the A* algorithm to compute a shortest path between src and dst.
 * You can assume that there are no negatrive weights, and that the heuristics h is monotone.
 *
 * @pre Graph has no negative weights
 * @pre h is monotone, i.e., for all u, h(u) + w(u,v) <= h(v)
 *
 */
sp_result_t *astar_search(graph_t const *g, node_t src, node_t dst, weight_t const* h);



#endif
