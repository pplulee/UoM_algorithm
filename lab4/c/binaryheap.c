// Giles Reger, based on code provided by Peter Lammich, 2019
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "global.h"
#include "pq.h"

struct binaryHeap {
    int num_elem;     // Number of elements
    int heap_size;    // Current size of heap
    int* weights;      // The heap
    Value_Type* elements;  // The heap
};


// 0-based operations
// This could be updated to be 1-based if you wanted, what else would need to change?
#define FIRST 0
int parent(int i) {return (i-1)/2;} 
int left(int i) {return (2*i) + 1; } 
int right(int i) {return (2*i) + 2; } 


struct binaryHeap* initialize_pq(int size){
    struct binaryHeap* pq = malloc(sizeof(struct binaryHeap));
    check(pq);
    pq->num_elem = size; 
    pq->heap_size=0;
    pq->weights = malloc(sizeof(int)*size);
    check(pq->weights);
    pq->elements = malloc(sizeof(Value_Type)*size);
    check(pq->elements);
    return pq;
}

void tidy(struct binaryHeap* pq){ 
    free(pq->elements);
    free(pq->weights);
    free(pq);
    // application owns contents of heap
}

// Helper function for swapping nodes in the tree
void swap(struct binaryHeap *pq, int i, int j) {
    Value_Type t = pq->elements[i];
    pq->elements[i] = pq->elements[j];
    pq->elements[j] = t;

    int w = pq->weights[i];
    pq->weights[i] = pq->weights[j];
    pq->weights[j] = w;
}


void sift_up(struct binaryHeap *pq, int i) {
   // TODO implement sift_up (also known as bubble-up and other things)
}

void sift_down(struct binaryHeap *pq, int i) {

    while(true){
      int l = left(i);
      int r = right(i);
      if(l >= pq->heap_size && r >= pq->heap_size){
        // no children, we're finished
        return;
      } 
      int smallest = l;
      if(r < pq->heap_size && pq->weights[r] < pq->weights[l]){ smallest=r;}

      if(pq->weights[smallest] < pq->weights[i]){ 
        swap(pq,i,smallest);
      } 
      else{
        // children not smaller, we're finished
        return;
      }

      i = smallest;
    }
}

bool contains(struct binaryHeap *pq, Value_Type u,int priority) {
  // Linear Search required as unordered
  for(int i=FIRST;i<pq->heap_size;i++){
    if(compare(pq->elements[i],u)==0 && pq->weights[i]==priority){
      return true;
    }
  }
  return false;
}

void expand(struct binaryHeap *pq)
{
    pq->num_elem = pq->num_elem*2;

    int* new_weights = malloc(sizeof(int)*pq->num_elem);
    check(new_weights);
    Value_Type* new_elements = malloc(sizeof(Value_Type)*pq->num_elem);
    check(new_elements);

    memcpy(new_weights,pq->weights,pq->heap_size*sizeof(int));
    memcpy(new_elements,pq->elements,pq->heap_size*sizeof(Value_Type));

    free(pq->weights);
    free(pq->elements);

    pq->weights=new_weights;
    pq->elements=new_elements;
}

int last_idx(struct binaryHeap  *pq) {
    // TODO the last is only 0 at the very start
    //      fix this to set last to the last index of pq
    int last = 0;
    // if we ever query outside the heap just expand it
    if(last >= pq->num_elem){
      expand(pq);
    }
    return last;
}

void insert(struct binaryHeap *pq, Value_Type u, int w) {
    int li = last_idx(pq);
    pq->weights[li]=w;
    pq->elements[li]=u;

    //TODO there is something missing here, put it back

    pq->heap_size++;
}

bool is_empty(struct binaryHeap *pq) {
  return pq->heap_size==0;
}

Value_Type pop_min(struct binaryHeap *pq) {
    if(is_empty(pq)){
      fprintf(stderr,"Error: pop_min from empty binaryHeap\n");
      exit(-1);
    }
    --pq->heap_size;
    int li = last_idx(pq);
    swap(pq,FIRST,li);
    Value_Type res = pq->elements[li];
    sift_down(pq,FIRST);
    return res;
}

void print(struct binaryHeap *pq){
  printf("BinaryHeap has %d elements with %d size\n",pq->num_elem,pq->heap_size);
  for(int i=FIRST; i < pq->heap_size; i++){
    printf("(%s,%d)\n",pq->elements[i], pq->weights[i]);
  }
}

