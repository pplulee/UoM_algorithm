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

// Returns the last node with priority less than or equal to 'priority'
// (In the presence of duplicates we could return the first node in the case of equals) 
// Records in 'updates' the nodes along the path that would need updating if a node to
// their right on their level were to be inserted e.g. the nodes at which the decision
// to go 'down' is made
struct node* search(struct skiplist* slist, int priority, struct node** updates)
{
  struct node* node = slist->header;
  int level = MAX_LEVEL;
  while(level >0){
    level--;
    while(node->next[level]->priority <= priority){ 
      node = node->next[level];
    }
    if(updates){updates[level]=node;}
  }
  return node;
}

void insert(struct skiplist* slist, Value_Type value, int priority){

  struct node* updates[MAX_LEVEL];
  struct node* insert_at = search(slist,priority,updates);

  int levels = 1;
  while(levels < MAX_LEVEL && (rand() % 2 == 0)){ levels++;}

  struct node* new_node = make_node(value,priority,levels);

  for(int i=0;i<levels;i++){
    new_node->next[i] = updates[i]->next[i];
    updates[i]->next[i] = new_node;
  }

  slist->size++;
}

bool contains(struct skiplist* slist, Value_Type value, int priority)
{
  struct node* node = search(slist,priority,NULL);
  while(node->priority==priority && node->value && compare(node->value,value)!=0){
    node = node->next[0];
  }
  return (node->priority==priority && node->value && compare(node->value,value)==0);
}


Value_Type pop_min(struct skiplist* slist){

 struct node* min = slist->header->next[0];
 Value_Type res = min->value;

 for(int i=0;i<min->height;i++){
   slist->header->next[i] = min->next[i];
 }
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

