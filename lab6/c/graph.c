#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>
#include <limits.h>
#include <math.h>

#include "general.h"
#include "graph.h"



//////////////////////// Graph Data Structure

node_t scan_node(FILE *file) {
    node_t res;
    if (fscanf(file, "%zu", &res) == 1) return res; else error("Error reading input");
}

raw_weight_t scan_raw_weight(FILE *file) {
    raw_weight_t res;
    if (fscanf(file,"%ld", &res) == 1) return res; else error("Error reading input");
}

weight_t scan_weight(FILE *file) {
    signed long res;
    if (fscanf(file,"%ld", &res) == 1) return weight_of_int(res); else error("Error reading input");
}

//const node_t INVALID_NODE = SIZE_MAX;

// const edge_tgt_t INVALID_TGT = {weight_inf(),INVALID_NODE};

bool _tgt_is_invalid(edge_tgt_t const *tgt) {
    return tgt->v == INVALID_NODE;
}


typedef struct _succs_t {
    size_t n;
    size_t capacity;   // Capacity
    edge_tgt_t *a;
} succs_t;


void succs_init(succs_t *s) {
    s->n=0;
    s->capacity=0;
    s->a = NULL;
}

void succs_uninit(succs_t *s) {
    if (s->a) free(s->a);
}

void succs_add(succs_t *s, edge_tgt_t tgt) {
    if (s->n >= s->capacity) {
        s->capacity = (s->capacity+1)*2;
        edge_tgt_t *aa = CALLOC(edge_tgt_t,s->capacity);
        if (s->a) {
            memcpy(aa,s->a,sizeof(edge_tgt_t)*s->n);
            free(s->a);
        }
        s->a = aa;
    }
    assert(s->n < s->capacity);
    s->a[s->n] = tgt;
    ++s->n;
}


struct _graph_t {
    size_t num_nodes;
    succs_t *adjs;
};

// Graph
void graph_init(graph_t *g, size_t num_nodes) {
    assert(num_nodes < SIZE_MAX);
    g->num_nodes=num_nodes;
    if (num_nodes) g->adjs = CALLOC(succs_t,num_nodes); else g->adjs=NULL;
    for (size_t i=0; i<num_nodes;++i) succs_init(g->adjs + i);
}

void graph_uninit(graph_t *g) {
    for (size_t i=0; i<g->num_nodes;++i) succs_uninit(g->adjs + i);
    if (g->adjs) free(g->adjs);
}

graph_t *graph_new(size_t num_nodes) {
    graph_t *res = CALLOC(graph_t,1);
    graph_init(res,num_nodes);
    return res;
}

void graph_delete(graph_t *g) {
    graph_uninit(g);
    free(g);
}

void graph_check_node(graph_t const *g, node_t u) {
    if (!(u < g->num_nodes)) {error("Node out of range: %zu",u);}
}

size_t graph_get_num_nodes(graph_t const *g) {return g->num_nodes;}


void graph_add_edge(graph_t *g, node_t u, weight_t w, node_t v) {
//     printf("Add edge %lu %lu %ld\n",u,v,w);
    assertmsg(u!=v,"self loop edge %zu -> %zu", u, v);
    assert(weight_is_finite(w));

    graph_check_node(g,u); graph_check_node(g,v);
    succs_add(g->adjs + u, (edge_tgt_t){w,v});
}

size_t graph_num_succs(graph_t const *g, node_t u) {
    return g->adjs[u].n;
}

edge_tgt_t const *graph_succs_begin(graph_t const *g, node_t u) {
    return g->adjs[u].a;
}

edge_tgt_t const *graph_succs_end(graph_t const *g, node_t u) {
    return g->adjs[u].a + g->adjs[u].n;
}

graph_t *graph_read(FILE *f) {
    size_t num_nodes = scan_size(f);
    size_t num_edges = scan_size(f);
    graph_t *g = graph_new(num_nodes);

//     printf("Reading %zu nodes and %zu edges\n",num_nodes,num_edges);

    for (size_t i=0; i<num_edges; ++i) {
        node_t u = scan_node(f);
        node_t v = scan_node(f);
        weight_t w = scan_weight(f);
        graph_add_edge(g,u,w,v);
    }

    return g;
}

void graph_write(FILE *f, graph_t const *g) {
  size_t N = graph_get_num_nodes(g);
  size_t num_edges = 0;

  for (node_t u=0; u<N; ++u) {
    num_edges+=graph_num_succs(g,u);
  }

  fprintf(f, "%zu\n%zu\n",N,num_edges);

  for (node_t u=0; u<N; ++u) {
    for (edge_tgt_t const *tgt = graph_succs_begin(g,u); tgt!=graph_succs_end(g,u);++tgt) {
      fprintf(f, "%zu %zu %ld\n",u,tgt->v,weight_to_int(tgt->w));
    }
  }

}



struct _path_t {
  size_t len;
  node_t nodes[];
};

path_t *path_new(size_t len) {
  path_t *p = malloc(sizeof(path_t) + len * sizeof(node_t));
  if (!p) error("Out of memory");
  p->len=len;
  for (size_t i=0;i<len;++i) p->nodes[i]=INVALID_NODE;
  return p;
}

void path_delete(path_t *p) {
  free(p);
}

void path_set(path_t *p, size_t i, node_t u) {
  assert(i<p->len);
  p->nodes[i]=u;
}
node_t path_get(path_t const *p, size_t i) {
  assert(i<p->len);
  return p->nodes[i];
}

size_t path_len(path_t const *p) {return p->len;}

path_t *path_from_pred(node_t const *pred, node_t v) {
  // Determine length
  size_t len=0;

  node_t u=v;

  while (true) {
    ++len;
    if (u==pred[u]) break;
    u=pred[u];
  }
  path_t *p = path_new(len);

  u=v;
  while (true) {
    --len;
    path_set(p,len,u);
    if (u==pred[u]) break;
    u=pred[u];
  }

  return p;
}







