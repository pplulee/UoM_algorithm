// Giles Reger, 2019

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <limits.h>
#include <stdbool.h>

#include "pq.h"


struct llist {
  Value_Type value1;
  Value_Type value2;
  int priority1;
  int priority2;
};

struct llist* initialize_pq (int size){
  struct llist* list = malloc(sizeof(struct llist));
  list->value1=NULL;
  list->value2=NULL;
  return list;
}     

void tidy (struct llist* list){
}

bool contains(struct llist* pq, Value_Type value, int priority){
  return false;
}

void insert(struct llist* list, Value_Type value, int priority){
  if(list->value1==NULL){ list->value1=value; list->priority1=priority;}
  else{ 
    list->value2=value; list->priority2=priority;
    if(list->priority2 < list->priority1){
      Value_Type tv = list->value1;
      int tp = list->priority1;
      list->value1=list->value2;
      list->priority1=list->priority2;
      list->value2=tv;
      list->priority2=tp;
    }
  }
}

bool is_empty(struct llist* pq){ 
  return false;
}

Value_Type pop_min(struct llist* pq){
  Value_Type res = pq->value1;
  pq->value1=pq->value2;
  pq->priority1=pq->priority2;
  pq->value2=NULL;
  return res;
}

void print(struct llist* list){
}

