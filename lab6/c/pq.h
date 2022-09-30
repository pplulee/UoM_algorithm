#ifndef _PQ_H
#define _PQ_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>

#include "general.h"
#include "graph.h"


typedef struct _DPQ_t DPQ_t;

/**
 * Create new, initially empty priority queue.
 * The priorities of all nodes < N are set to infinite.
 * @param N Maximum number of nodes
 */
DPQ_t *DPQ_new(size_t N);

/**
 * Delete priority queue
 */
void DPQ_delete(DPQ_t *pq);

/**
 * Get priority of node.
 *
 * Complexity: O(1)
 *
 * @pre u < N
 */
weight_t DPQ_prio(DPQ_t const *pq, node_t u);

/**
 * Check if node is contained in queue
 *
 * Complexity: O(1)
 *
 * @pre u < N
 */
bool DPQ_contains(DPQ_t const *pq, node_t u);

/**
 * Insert node into queue, with given priority.
 * The priority of this node is set accordingly.
 *
 * Complexity: O(log N)
 *
 * @pre Node must not be in queue
 * @pre u < N
 * @param u node
 * @param w priority
 */
void DPQ_insert(DPQ_t *pq, node_t u, weight_t w);

/**
 * Check if queue is empty
 *
 * Complexity: O(1)
 */
bool DPQ_is_empty(DPQ_t const *pq);

/**
 * Retrieve and remove an element of the queue with minimal priority
 *
 * Complexity: O(log N)
 *
 * @pre The queue is not empty
 */
node_t DPQ_pop_min(DPQ_t *pq);

/**
 * Lower priority of element in queue
 *
 * Complexity: O(log N)
 *
 * @pre the node is in the queue
 * @pre the new priority is less than the current nodes priority
 */
void DPQ_decrease_key(DPQ_t *pq, node_t u, weight_t w);


/**
 * Free priority queue, but keep priority map
 */
weight_t *DPQ_dist_free(DPQ_t *pq);



#endif


