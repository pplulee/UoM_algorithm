// Giles Reger, 2019

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>

#include "pq.h"


struct llist {
  Value_Type value;
};

struct llist* initialize_pq (int size){
  struct llist* list = malloc(sizeof(struct llist));
  return list;
}     

void tidy (struct llist* list){
}

bool contains(struct llist* pq, Value_Type value, int priority){
  return false;
}

void insert(struct llist* list, Value_Type value, int priority){
  list->value=value;
}

bool is_empty(struct llist* pq){ 
  return false;
}

Value_Type pop_min(struct llist* pq){
  return pq->value;
}

void print(struct llist* list){
}

