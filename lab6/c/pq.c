#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>

#include "general.h"
#include "graph.h"
#include "pq.h"


typedef struct {size_t i;} hidx_t;

size_t idx_of(hidx_t i) {return i.i - 1;}

const hidx_t INVALID_HIDX = {0};
bool hidx_is_invalid(hidx_t i) {return i.i == 0;}

const hidx_t hidx_first = {1};



// 1-based operations
hidx_t parent(hidx_t i) {return (hidx_t){i.i / 2}; }
hidx_t left(hidx_t i) {return (hidx_t){i.i * 2}; }
hidx_t right(hidx_t i) {return (hidx_t){i.i * 2 + 1}; }
bool has_parent(hidx_t i) {return parent(i).i>0; }
bool has_left(size_t n, hidx_t i) {return left(i).i<=n; }
bool has_right(size_t n, hidx_t i) {return right(i).i<=n; }


struct _DPQ_t {
    size_t num_elem;     // Number of elements
    size_t heap_size;    // Current size of heap
    weight_t *D;  // Priorities
    node_t *H;    // The heap
    hidx_t *I;    // Index of element in heap.
};


void DPQ_init(DPQ_t *pq, size_t num_elem) {
    pq->num_elem = num_elem;
    pq->heap_size=0;
    pq->D = CALLOC(weight_t,num_elem);
    pq->H = CALLOC(node_t,num_elem);
    pq->I = CALLOC(hidx_t,num_elem);

    for (size_t i=0;i<num_elem;++i) {
      pq->I[i]=INVALID_HIDX;
      pq->D[i]=weight_inf();
    }

}

void DPQ_uninit(DPQ_t *pq) {
    free(pq->D);
    free(pq->H);
    free(pq->I);
}

DPQ_t *DPQ_new(size_t num_elem) {
    DPQ_t *pq = CALLOC(DPQ_t,1);
    DPQ_init(pq,num_elem);
    return pq;
}

void DPQ_delete(DPQ_t *pq) {
    DPQ_uninit(pq);
    free(pq);
}

weight_t *DPQ_dist_free(DPQ_t *pq) {
  weight_t *res=pq->D;
  free(pq->H);
  free(pq->I);
  free(pq);
  return res;
}


weight_t DPQ_prio(DPQ_t const *pq, node_t u) {
    assert(u<pq->num_elem);
    return pq->D[u];
}

weight_t _DPQ_hprio(DPQ_t const *pq, hidx_t i) {
    return DPQ_prio(pq,pq->H[idx_of(i)]);
}

void _DPQ_adjustI(DPQ_t *pq, hidx_t i) {
    pq->I[pq->H[idx_of(i)]] = i;
}

void _DPQ_swap(DPQ_t *pq, hidx_t i, hidx_t j) {
    node_t t = pq->H[idx_of(i)];
    pq->H[idx_of(i)] = pq->H[idx_of(j)];
    pq->H[idx_of(j)] = t;
    _DPQ_adjustI(pq,i);
    _DPQ_adjustI(pq,j);
}


void _DPQ_sift_up(DPQ_t *pq, hidx_t i) {
    while (has_parent(i) && weight_less(_DPQ_hprio(pq,i), _DPQ_hprio(pq,parent(i)))) {
        _DPQ_swap(pq,i,parent(i));
        i = parent(i);
    }
}

void _DPQ_sift_down(DPQ_t *pq, hidx_t i) {
    while (has_right(pq->heap_size,i)) {
        weight_t w = _DPQ_hprio(pq,i);
        weight_t lw = _DPQ_hprio(pq,left(i));
        weight_t rw = _DPQ_hprio(pq,right(i));

        if (!weight_less(lw, w) && !weight_less(rw, w)) return;

        if (weight_less(lw,rw)) {
            _DPQ_swap(pq,i,left(i));
            i=left(i);
        } else {
            _DPQ_swap(pq,i,right(i));
            i=right(i);
        }
    }

    if (has_left(pq->heap_size,i)) {
        weight_t w = _DPQ_hprio(pq,i);
        weight_t lw = _DPQ_hprio(pq,left(i));
        if (weight_less(lw,w)) _DPQ_swap(pq,i,left(i));
    }

}

bool DPQ_contains(DPQ_t const *pq, node_t u) {
    assert(u<pq->num_elem);
    return !hidx_is_invalid(pq->I[u]);
}

hidx_t _DPQ_last_idx(DPQ_t const *pq) {
    return (hidx_t){pq->heap_size};
}

void DPQ_insert(DPQ_t *pq, node_t u, weight_t w) {
    assert(u<pq->num_elem);
    assert(!DPQ_contains(pq,u));
    pq->D[u]=w;
    ++pq->heap_size;
    hidx_t i = _DPQ_last_idx(pq);
    pq->H[idx_of(i)]=u;
    _DPQ_adjustI(pq,i);
    _DPQ_sift_up(pq,i);
}

bool DPQ_is_empty(DPQ_t const *pq) {return pq->heap_size==0;}

node_t DPQ_pop_min(DPQ_t *pq) {
    assert(!DPQ_is_empty(pq));
    hidx_t li = _DPQ_last_idx(pq);
    _DPQ_swap(pq,hidx_first,li);
    node_t res = pq->H[idx_of(li)];
    --pq->heap_size;
    pq->I[res] = INVALID_HIDX;
    _DPQ_sift_down(pq,hidx_first);
    return res;
}

void DPQ_decrease_key(DPQ_t *pq, node_t u, weight_t w) {
    assert(u<pq->num_elem);
    assert(DPQ_contains(pq,u));
    assert(weight_less(w, pq->D[u]));
    pq->D[u]=w;

    hidx_t i = pq->I[u];
    _DPQ_sift_up(pq,i);

}
