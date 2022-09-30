#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>

#include "graph.h"
#include "pq.h"
#include "shortest_path.h"
#include "sp_algorithms.h"

sssp_result_t *sssp_result_new(size_t N, node_t src, node_t dst, bool ncyc,node_t *p, weight_t *d, unsigned long long c) {
  sssp_result_t *r = CALLOC(sssp_result_t,1);
  r->N=N;
  r->src=src;
  r->dst=dst;
  r->pred=p;
  r->has_negative_cycle=ncyc;
  r->dist=d;
  r->relax_count=c;
  return r;
}

void sssp_result_delete(sssp_result_t *r) {
  if (r->pred) free(r->pred);
  if (r->dist) free(r->dist);
  free(r);
}

sp_result_t *sp_result_new(node_t src, node_t dst, path_t *p, weight_t d, unsigned long long c) {
  sp_result_t *r = CALLOC(sp_result_t,1);
  r->src=src;
  r->dst=dst;
  r->path=p;
  r->dist=d;
  r->relax_count=c;
  return r;
}

void sp_result_delete(sp_result_t *r) {
  if (r->path) path_delete(r->path);
  free(r);
}


sp_result_t *sssp_to_sp_result(sssp_result_t *a, node_t dst) {
  path_t *p = NULL;

  assert(a->dst==INVALID_NODE || a->dst==dst);

  if (a->pred[dst] != INVALID_NODE) {
    p = path_from_pred(a->pred,dst);
  }

  sp_result_t *r = sp_result_new(a->src, dst, p,a->dist[dst],a->relax_count);

  sssp_result_delete(a);

  return r;
}

void print_path(path_t const *p) {
  if (p == NULL) printf("NULL");
  else if (path_len(p) == 0) printf("EMP");
  else {
    printf("%zu",path_get(p,0));
    for (size_t i=1;i<path_len(p);++i)
      printf(", %zu",path_get(p,i));

  }
}

void print_sp_result(sp_result_t const *r) {
  printf("Distance: "); print_weight_stdout(r->dist); printf("\n");
  printf("Path: "); print_path(r->path); printf("\n");
  printf("# Relaxed nodes: %llu\n", r->relax_count);
}

void print_sssp_result(FILE *f, sssp_result_t const *r) {
  size_t N = r->N;
  size_t NN = N<10?N:10;

  fprintf(f,"Distmap:");
  for (size_t i=0; i<NN; ++i) {
    fprintf(f," "); print_weight(f,r->dist[i]);
  }

  if (N<NN) {
    fprintf(f," ...\n");
  } else {
    fprintf(f,"\n");
  }

}





