// Giles Reger, 2019

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "global.h"
#include "pq.h"

struct llist {
  Value_Type value;
  int priority;
  struct llist* next;
  struct llist* prev;
};


struct llist* initialize_pq (int size){
  // Use a dummy node for the head of the list 
  struct llist* dummy = malloc(sizeof(struct llist)); 
  check(dummy);
  dummy->value = NULL;
  dummy->priority = 0;
  dummy->next=NULL;
  dummy->prev=NULL;
  return dummy;
}     

void tidy (struct llist* list){
  if(list){
    free(list->value);
    struct llist* next = list->next;
    free(list);
    tidy(next);
  }
}

bool contains(struct llist* pq, Value_Type value,int priority){
  // Linear search
  if(pq){
    // Skip dummy
    struct llist* next = pq->next;
    while(next){
      if(compare(next->value,value)==0 && next->priority==priority){
        return true; 
      }
      next = next->next;
    }
  }
  return false;
}

void insert(struct llist* list, Value_Type value, int priority){
  struct llist* node = malloc(sizeof(struct llist));
  check(node);
  node->value=value;
  node->priority=priority;

  struct llist* here = list;
  while(here->next && here->next->priority < priority){
      here=here->next;
  }
  // insert after here
  node->next=here->next;
  if(here->next){
    here->prev=node;
  }
  here->next=node;
  node->prev=here;
}

bool is_empty(struct llist* pq){ 
  // Assumes single dummy
  return (pq->next==NULL); 
}


// This is why we need the dummy - we need the original pointer to still
// be the pointer to the list even after we remove the minimum element
Value_Type pop_min(struct llist* pq){

  if(pq && pq->next){
    // The best will always be the first
    struct llist* node = pq->next;

    Value_Type value = node->value;
    
    // Remove
    pq->next=node->next;
    if(node->next){
      node->next->prev=node->prev;
    }
    free(node);

    return value;
  }
  return NULL;
}

void print(struct llist* list){
  if(list){
    printf("(%p) <%s,%d> (from %p)\n",list,list->value,list->priority,list->prev);
    print(list->next);
  }
  else{ printf("NULL\n"); }
}
