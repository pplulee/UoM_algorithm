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

void compute_path(char const *algo, char const *src, char const *dst) {
    node_t s;
    sscanf(src, "%zu", &s);
    node_t d;
    sscanf(dst, "%zu", &d);
    graph_t *g = graph_new(10);
    graph_add_edge(g, 0, weight_of_int(1), 1);
    graph_add_edge(g,1, weight_of_int(2), 2);
    graph_add_edge(g,2, weight_of_int(3), 3);
    graph_add_edge(g,3, weight_of_int(1), 4);
    graph_add_edge(g,5, weight_of_int(1), 6);
    graph_add_edge(g,6, weight_of_int(1), 8);
    graph_add_edge(g,8, weight_of_int(2), 9);
    graph_add_edge(g,5, weight_of_int(9), 9);
    if (strcmp(algo, "bellman-ford-neg")==0) {
        graph_add_edge(g,3, weight_of_int(-1), 0);
        graph_add_edge(g,5, weight_of_int(-5), 7);
    } else {
        graph_add_edge(g,3, weight_of_int(4), 0);
        graph_add_edge(g,5, weight_of_int(5), 7);
    }


  weight_t *h = CALLOC(weight_t,graph_get_num_nodes(g));
    for (size_t u=0; u<graph_get_num_nodes(g);++u) h[u] = weight_of_int(d - u);

  if (strcmp(algo,"bellman-ford")==0) print_sp_result(sssp_to_sp_result(bellman_ford(g,s),d));
    else if (strcmp(algo,"bellman-ford-neg")==0) print_sp_result(sssp_to_sp_result(bellman_ford(g,s),d));
  else if (strcmp(algo,"dijkstra")==0) print_sp_result(sssp_to_sp_result(dijkstra(g,s,d),d));
  else if (strcmp(algo,"astar")==0) print_sp_result(astar_search(g,s,d,h));
  else if (strcmp(algo,"bfs")==0) print_sp_result(sssp_to_sp_result(bfs(g,s,d),d));
  else error("Invalid algorithm name: %s", algo);

  free(h);
}


int main(int argc, char **argv)
{

  ap_std_init();

  if (argc==4) compute_path(argv[1],argv[2],argv[3]);
  else if (argc==5) {
    if (strcmp(argv[4],"-v")==0) set_msg_verb(0);
    else if (strcmp(argv[4],"-vv")==0) set_msg_verb(1);
    else if (strcmp(argv[4],"-vvv")==0) set_msg_verb(2);

    compute_path(argv[1],argv[2],argv[3]);
  }
  else error("Invalid command line");

  return 0;
}

