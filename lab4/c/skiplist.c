// Giles Reger, 2019

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>

#include "global.h"
#include "pq.h"

// This will have a large impact on performance, try playing with it
#define MAX_LEVEL 20 


struct node {
  int priority;
  Value_Type value;
  // Array of 'forward' pointers
  struct node** next;
  // Just for printing
  int height;
};

// Note that the skiplist is implemented as a linked list of 'nodes'
// where a node represents a tower in the abstract view
struct skiplist {
  int levels;
  int size;
  struct node *header;
};

// Helper function for making nodes, does not initialise next array
struct node* make_node(Value_Type value, int priority, int levels){
  struct node* node = malloc(sizeof(struct node));
  check(node);
  node->priority = priority;
  node->value = value;
  node->next = malloc(sizeof(struct node*) * levels);
  check(node->next);
  node->height=levels;
  return node;
}

struct skiplist* initialize_pq (int size){
  struct skiplist* slist = malloc(sizeof(struct skiplist));
  check(slist);
  slist->levels = 1;
  slist->size = 0; 
  // We will actually use the same sentinel node for start and end 
  slist->header= make_node(NULL,INT_MAX,MAX_LEVEL);
  for(int i=0; i<MAX_LEVEL; i++){
    slist->header->next[i] = slist->header;
  }
  return slist;
}     

void tidy (struct skiplist* list){
  struct node* next = list->header->next[0];
  while(next!=list->header){
    struct node* n = next;
    next = n->next[0];
    free(n->next);
    free(n);
  }
  free(list->header->next);
  free(list->header);
  free(list);
}

bool is_empty(struct skiplist* slist){
  return slist->size <= 0;
}

// Returns the last node with priority less than 'priority'
// UPDATE: the above line used to say 'or equal' but it was pointed out that returning
// the last node in the case of duplicates makes the contains function fail
//
// Records in 'updates' the nodes along the path that would need updating if a node to
// their right on their level were to be inserted e.g. the nodes at which the decision
// to go 'down' is made
struct node* search(struct skiplist* slist, int priority, struct node** updates)
{
  struct node* node = slist->header;
  int level = MAX_LEVEL;
  while(level >0){
    level--;

    // TODO we now need to scan along this level until the 'next'
    // priority is not less than the priority we are searching for. 
    // (Hint: the next node at this leve is currently in node->next[level])
    
    // Record the node where we go down at a particular level
    if(updates){updates[level]=node;}
  }
  return node;
}

void insert(struct skiplist* slist, Value_Type value, int priority){

  struct node* updates[MAX_LEVEL];
  struct node* insert_at = search(slist,priority,updates);

  // TODO create a new_node with a random number of levels
  // where the chance of having n levels is 1/2^n e.g. flip
  // a coin for each level. (Hint: use rand()) 

  struct node* new_node = 0; 

  for(int i=0;i<levels;i++){
    new_node->next[i] = updates[i]->next[i];
    updates[i]->next[i] = new_node;
  }

  slist->size++;
}

bool contains(struct skiplist* slist, Value_Type value, int priority)
{
  struct node* node = search(slist,priority,NULL)->next[0];
  while(node->priority==priority && node->value && compare(node->value,value)!=0){
    node = node->next[0];
  }
  return (node->priority==priority && node->value && compare(node->value,value)==0);
}


Value_Type pop_min(struct skiplist* slist){

 struct node* min = slist->header->next[0];
 Value_Type res = min->value;

 // TODO what do we need to do to repair the Skip List
 // to remove the min node? (Hint: what is pointing to min
 // and where should that point?)

 free(min->next);
 free(min);
 
 slist->size--;

 return res;
}

// There are probably nicer ways to print a skiplist
void print(struct skiplist* list){

  struct node* node = list->header;
  do{
    printf("(%s,%d,%d)\n",node->value,node->priority,node->height);
    node = node->next[0];
  }
  while(node != list->header);
}

