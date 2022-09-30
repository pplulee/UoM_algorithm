#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>

#include "graph.h"
#include "pq.h"
#include "sp_algorithms.h"

sssp_result_t *bfs(graph_t const *g, node_t src, node_t dst) {
  unsigned long long stat_edges_explored=0;

  size_t N = graph_get_num_nodes(g);
  node_t *pred = CALLOC(node_t,N);
  weight_t *dist = CALLOC(weight_t,N);
    
  for (size_t i=0;i<N;++i) {
    pred[i]=INVALID_NODE;
    dist[i]=weight_inf();
  }

  error("Not implemented");

  return sssp_result_new(N,src,dst,false,pred,dist,stat_edges_explored);
}

sssp_result_t *bellman_ford(graph_t const *g, node_t src) {
  error("Not implemented");
}

sssp_result_t *dijkstra(graph_t const *g, node_t src, node_t dst) {
  error("Not implemented");
}

sp_result_t *astar_search(graph_t const *g, node_t src, node_t dst, weight_t const* h) {
  error("Not implemented");
}




