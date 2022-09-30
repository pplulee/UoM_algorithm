#ifndef _GRAPH_H
#define _GRAPH_H

#include <stdint.h>
#include <stdbool.h>
#include <limits.h>

#include "weight.h"


/// Node type.
typedef size_t node_t;
/// Marker for invalid node.
#define INVALID_NODE SIZE_MAX

/// Type for graphs
typedef struct _graph_t graph_t;

///Constructors

/**
 * Create graph with specified number of nodes, and no edges
 * @pre num_nodes < SIZE_MAX
 */
graph_t *graph_new(size_t num_nodes);

/// Free all memory used by graph.
void graph_delete(graph_t *g);

/* Create graph from file. The file is a text file containing the positive integer numbers:
 *
 * num_nodes
 * num_edges
 * u_1 v_1 w_1
 * ...
 *
 * i.e., the number of nodes, then the number of edges, and then, for each edge, the source node, target node, and weight.
 *
 * Everything content after the last edge will be ignored.
 *
 * The function outputs an error message for files not adhering to this format!
 */
graph_t *graph_read(FILE *f);

/**
 * Write graph to file. Uses format described in @ref graph_read.
 */
void graph_write(FILE *f, graph_t const *g);


///Graph operations

/**
 * Add edge to graph
 * @pre Nodes must be in range, i.e., u,v < num_nodes
 * @pre Weight must be finite
 * @pre Self-loop edges not allowed, i.e., u != v
 */
void graph_add_edge(graph_t *g, node_t u, weight_t w, node_t v);


/**
 * Get number of nodes.
 */
size_t graph_get_num_nodes(graph_t const *g);

/**
 * Get sucessors of specified node
 *
 * Each successor is represented by a weight and a target node.
 * One can query the number of successors, an array of successors (begin), and
 * a pointer to one past the last successor (end).
 *
 * Thus, iteration over successors can either be done by indexing "begin[i]",
 * or by incrementing the pointer until it is ==end.
 *
 * For example, the following code snippet iterates over all successors of node u in graph g
 *
 *   for (edge_tgt_t const *tgt=graph_succs_begin(g,u);tgt!=graph_succs_end(g,u);++tgt) { / * use tgt->v and tgt->w to access target node and edge weight * / }
 *
 */
typedef struct {
    weight_t w; /// Edge weight
    node_t v;   /// Target node
} edge_tgt_t;

size_t graph_num_succs(graph_t const *g, node_t u);
edge_tgt_t const *graph_succs_begin(graph_t const *g, node_t u);
edge_tgt_t const *graph_succs_end(graph_t const *g, node_t u);

/// Paths
/**
 * A path is a sequence of nodes with a specified length.
 */

typedef struct _path_t path_t;

path_t *path_new(size_t len);
void path_delete(path_t *p);

void path_set(path_t *p, size_t i, node_t u);
node_t path_get(path_t const *p, size_t i);
size_t path_len(path_t const *p);

/**
 * Extract path from predecessor array. Convention: Start node points to itself.
 * @returns path array, ter
 */
path_t *path_from_pred(node_t const *pred, node_t v);

#endif

