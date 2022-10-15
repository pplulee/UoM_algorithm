#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define _BSD_SOURCE 
#include <string.h>

#include "global.h"
#include "darray.h"
#include "sorting.h"


// Can be redefined if Value_Type changes
int compare(Value_Type a, Value_Type b){
  return strcmp(a,b);
}


struct darray* initialize_set (int size)  
{

  struct darray* arr = malloc(sizeof(struct darray)); 
  check(arr);
  arr->cells = (Value_Type*) (malloc(sizeof(Value_Type)*size));
  check(arr->cells);
  arr->capacity = size;
  arr->size = 0;
  arr->sorted = false;
  arr->resizes = 0;
  return arr;
}

void tidy(struct darray* arr)
{
  if(arr){
    // free memory created by strdup
    for(unsigned i=0; i<arr->size;i++){ free(arr->cells[i]); }
    // free array and struct
    free(arr->cells);
    free(arr);
  }
}

int size(struct darray* arr){ return arr->size; }

struct darray* insert (Value_Type value, struct darray* arr)
{
  // If we have reached capacity, double size and copy
  if(arr->size >= arr->capacity){
    struct darray* new_arr = initialize_set(arr->capacity*2);
    for(unsigned int i=0;i<arr->size;i++){
      new_arr->cells[i] = arr->cells[i];
    }
    new_arr->size = arr->size;
    new_arr->resizes = arr->resizes+1;
    free(arr->cells);
    free(arr);
    arr = new_arr;
  }

  arr->cells[arr->size] = strdup(value);
  arr->size++; 

  // changing the array means it may no longer be sorted
  arr->sorted = false;

  return arr;
}

bool find (Value_Type value, struct darray* arr)
{
  if(mode == LINEAR_SEARCH){
  for(unsigned i=0;i<arr->size;i++){
    if(compare(value,arr->cells[i])==0){
      return true;
    }
  }
  return false;
  }
  else{ // Binary Search 
  if(!arr->sorted){
    if(verbose > 2){
      printf("Dynamic Array not sorted, sorting...\n");
    }
    sort(arr,mode);
    if(verbose > 2){
      printf("Dynamic Array sorted\n");
    }
    arr->sorted = true;
  }

  int first = 0;
  int last = arr->size-1;
  int middle = (first+last)/2;

  while(first <= last){
    int search = compare(arr->cells[middle],value);
    if(search < 0){
      first = middle+1;
    }
    else if(search == 0){
      return true;
    }
    else{
      last = middle - 1;
    }
    middle = (first + last)/2;
  }

  return false;
  }
}

// You can make any changes you want to this function
void print_set (struct darray* arr)
{
  printf("DArray:\n");
  for(unsigned i=0;i<arr->size;i++){
    printf("\t%s\n",arr->cells[i]);
  }
}

// You can make any changes you want to this function
void print_stats (struct darray* arr)
{
  printf("Dynamic array of capacity %d contains %d elements\n",arr->capacity,arr->size);
  printf("Dynamic array was resized %d times\n",arr->resizes);
}

