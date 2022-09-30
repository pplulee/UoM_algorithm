#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>
#include <math.h>

#include "general.h"
#include "sp_algorithms.h"
#include "hashmap.h"
#include "airports.h"


/*
void pr_dfs_aux(graph_t const *g, node_t u, bool *visited, size_t d, size_t d_limit) {
  if (visited[u] || d>=d_limit) return;

  visited[u]=true;
  printf("%s\n",ap_get_code(u));

  for (edge_tgt_t const *tgt = graph_succs_begin(g,u); tgt!=graph_succs_end(g,u);++tgt) {
    pr_dfs_aux(g,tgt->v,visited,d+1,d_limit);
  }
}

void print_reachable(graph_t const *g, node_t src, size_t d) {
  bool visited[graph_get_num_nodes(g)];
  for (size_t i=0;i<graph_get_num_nodes(g);++i) visited[i]=false;

  pr_dfs_aux(g,src,visited,0,d);
}*/

size_t count;

void count_aux(node_t u, bool *visited) {
  if (visited[u]) return;
  visited[u] = true;
  ++count;

  graph_t const *g = ap_get_graph();

  for (edge_tgt_t const *tgt=graph_succs_begin(g,u); tgt!=graph_succs_end(g,u); ++tgt) {
    count_aux(tgt->v, visited);
  }
}

size_t count_reachable(char const *code) {

  apid_t id = ap_get_id(code);
  bool visited[ap_get_num_ids()];
  for (size_t i=0; i<ap_get_num_ids(); ++i) visited[i]=false;
  count=0;

  count_aux(id,(bool *)&visited);

  printf("%zu airports reachable from %s\n",count,code);

  return count;
}


weight_t path_dist(path_t const *p) {
  weight_t dist=weight_of_int(0);

  for (size_t i=0; i+1<path_len(p); ++i) {
    dist = weight_add(dist,ap_get_dist(path_get(p,i),path_get(p,i+1)));
  }

  return dist;
}

void print_ap_path(path_t const *p) {

  for (size_t i=1; i<path_len(p); ++i) {
    node_t u = path_get(p,i-1);
    node_t v = path_get(p,i);
    printf("%s to %s (%ldkm)\n",
      ap_get_code(u),
      ap_get_code(v),
      weight_to_int(ap_get_dist(u,v))
    );
  }
}

void print_route(sp_result_t *res) {
  if (res->path) {
    print_ap_path(res->path);
    printf("Total = %ldkm\n",weight_to_int(path_dist(res->path)));
  } else {
    printf("No route from %s to %s\n",ap_get_code(res->src),ap_get_code(res->dst));
  }
  msg0("relaxed %llu edges\n", res->relax_count);

  sp_result_delete(res);
}


void compute_route(char const *algo, char const *scode, char const *dcode) {
  node_t s=ap_get_id(scode);
  node_t d=ap_get_id(dcode);
  graph_t const *g = ap_get_graph();

  weight_t *h = CALLOC(weight_t,graph_get_num_nodes(g));
  for (size_t u=0; u<graph_get_num_nodes(g);++u) h[u] = ap_is_valid_id(u)?ap_get_dist(u,d):weight_inf();

  if (strcmp(algo,"bellman-ford")==0) print_route(sssp_to_sp_result(bellman_ford(g,s),d));
  else if (strcmp(algo,"dijkstra")==0) print_route(sssp_to_sp_result(dijkstra(g,s,d),d));
  else if (strcmp(algo,"astar")==0) print_route(astar_search(g,s,d,h));
  else if (strcmp(algo,"bfs")==0) print_route(sssp_to_sp_result(bfs(g,s,d),d));
  else error("Invalid algorithm name: %s", algo);

  free(h);
}


int main(int argc, char **argv)
{

  ap_std_init();

  if (argc==5 && strcmp(argv[1],"route")==0) compute_route(argv[2],argv[3],argv[4]);
  else if (argc==3 && strcmp(argv[1],"count")==0) count_reachable(argv[2]);
  else error("Invalid command line");


  ap_delete();

  return 0;
}

