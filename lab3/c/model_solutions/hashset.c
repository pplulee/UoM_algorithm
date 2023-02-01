#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define _BSD_SOURCE 
#include <string.h>
#include <math.h>

#include "global.h"
#include "hashset.h"

// Can be redefined if Value_Type changes
int compare(Value_Type a, Value_Type b){
  return strcmp(a,b);
}

// Helper functions for finding prime numbers 
bool isPrime (int n)
{
  for (int i = 2; i*i <= n; i++)
    if (n % i == 0)
      return false;
  return true;
}

int nextPrime(int n)
{
  for (; !isPrime(n); n++);
  return n;
}
// h = x0*a^(k-1) + x1*a^(k-2) + ... + x(k-2)*a + x(k-1)
// h = |ak + b| mod N
int hashFunc(Value_Type k, int N)
{
  int temp = 1; int a = 41;
  int len = strlen(k);
  long long h = 0;
  //printf("%s, len: %d, k[%d]: %lld\n", k, len, len - 1, h);
  for (int i = len - 1; i >= 0; i--){
    h += k[i] * temp;
    //printf("h += k[%d](%d) * %d, h = %lld\n", i, k[i], a, h);
    temp *= a;
  }

  //printf("%lld\n", h);
  h = labs(h) % N;
  return h;
}

int hashFunc2(Value_Type k, int N)
{
    int len = strlen(k);
    long long h = 0;
    for (int i = len -1; i >=0; i--) {
        h += k[i];
    }
    h = labs(h) % N;
    return h;
}

bool isLinearProbing(int mode){
  return mode == HASH_1_LINEAR_PROBING || mode == HASH_2_LINEAR_PROBING;
}
bool isQuadraticProbing(int mode){
  return mode == HASH_1_QUADRATIC_PROBING || mode == HASH_2_QUADRATIC_PROBING;
}
bool isDoubleHashing(int mode){
  return mode == HASH_1_DOUBLE_HASHING || mode == HASH_2_DOUBLE_HASHING;
}
bool isSeparateChaining(int mode){
  return mode == HASH_1_SEPARATE_CHAINING || mode == HASH_2_SEPARATE_CHAINING;
}


struct hashset* initialize_set (int size)  
{
  struct hashset* set = (struct hashset*) malloc(sizeof(struct hashset));
  check(set);
  if (! isSeparateChaining(mode)) {
      set->cells = (cell *)malloc(size * sizeof(cell));
      check(set->cells);
  } else {
      set->cell_chains = (cell_chain *)malloc(size * sizeof(cell_chain));
      check(set->cell_chains);
  }
  set->size = size;
  set->num_entries = 0;
  set->collision = 0;

  if (! isSeparateChaining(mode)) {
      for(int i = 0; i < size; i++){
          set->cells[i].state = empty;
      }
  }
  return set;

}

void tidy(struct hashset* set)
{
  if (! isSeparateChaining(mode)) {
    for(int i=0;i<set->size;i++){
      if(set->cells[i].state == in_use){
	free(set->cells[i].element);
      }
    }
    free(set->cells);
  } else {
    for(int i = 0;i<set->size;i++) {
      struct CC chaini = set->cell_chains[i];
      tidy_cell_chain(&chaini);
    }
    free(set->cell_chains);
  }
  free(set);
}

int size(struct hashset* set){ return set->num_entries; }

// insertion

void insertCell(Value_Type k, struct hashset* set, int pos)
{
 set->cells[pos].element = strdup(k);
 set->cells[pos].state = in_use;
 set->num_entries ++;
  return;
}

struct hashset* rehash(struct hashset* set)
{
  int N =set->size;
  int newSize = nextPrime(2*N);
  struct hashset* new_set = initialize_set(newSize);
  //  printf("test");
  if (verbose > 2)
    { // call with option -vvv to get this
        printf("Rehashing\n");
        printf("Current Set\n");
         print_set (set);
   }
  for(int i = 0; i < N; i++){
    if (! isSeparateChaining(mode)) {
      if(set->cells[i].state == in_use)
	insert(set->cells[i].element, new_set);
    } else {
      if (set->cell_chains[i].value != NULL) {
	insert(set->cell_chains[i].value, new_set);
	  struct CC* cell_chain = &set->cell_chains[i];
	  while(cell_chain->link != NULL) {
	    insert(cell_chain->value, new_set);
	    cell_chain = cell_chain->link;
	  }
      }
    }
  }
  tidy(set);
  if (verbose > 2)
    { // call with option -vvv to get this
          printf("New Set\n");
        print_set (new_set);
  }

  return new_set;
}

struct hashset* insert (Value_Type value, struct hashset* set)
{
  if(find(value, set)) return set; // detect duplicate

  int N = set->size;
  if(set->num_entries >= N/2) // check full table
    set = rehash(set);

  N = set->size;
  int pos = hashFunc(value, N);

  // insert into empty cell
  if (!isSeparateChaining(mode)) {
    if(set->cells[pos].state != in_use)
      insertCell(value, set, pos);

    else{
      if(isLinearProbing(mode)) // linear probing: A[(i+j)mod N]
	{
	  for(int j = 1; j < N; j++){
	    int look = (pos + j) % N;
	    set->collision ++;
	    if(set->cells[look].state != in_use){
	      insertCell(value, set, look);
	      break;
	    }
	  }
	}
      else if(isQuadraticProbing(mode)) // quadratic probing: A[(i+j^2)mod N]
	{
	  for(int j = 1; j < N; j++){
	    int look = (pos + j*j) % N;
	    set->collision ++;
	    if(set->cells[look].state != in_use){
	      insertCell(value, set, look);
	      break;
	    }
	  }
	}
      else if(isDoubleHashing(mode)) // double hash: A[(i+j*h'(k))mod N] 
	{
	  int temp = hashFunc2(value, N);

	  for(int j = 1; j < N; j++){
	    int look = (pos + j*temp) % N;
	    set->collision ++;
	    if(set->cells[look].state != in_use){
	      insertCell(value, set, look);
	      break;
	    }
	  }
	}
    }
  } else {
    struct CC* cc = &set->cell_chains[pos];
    struct CC* ccmod = insert_chain(value, cc);
    set->cell_chains[pos] = *ccmod;
    set->collision += set->cell_chains[pos].collision;
    set->num_entries++;
  }
  return set;
}

bool find (Value_Type value, struct hashset* set)
{
  int N =set->size;
  int pos = hashFunc(value, N);

  if (!isSeparateChaining(mode)) {
    if(set->cells[pos].state == in_use
       && (strcmp(set->cells[pos].element, value) == 0))
      return true;

    else if(isLinearProbing(mode)) // linear probing
      {
	for(int j = 1; j < N; j++){
	  int look = (pos + j) % N;
	  if(set->cells[look].state == empty)
	    return false;
	  if(set->cells[look].state == in_use
	     && (strcmp(set->cells[look].element, value) == 0)){
	    return true;
	  }
	}
      }
    else if(isQuadraticProbing(mode)) // quadratic probing
      {
	for(int j = 1; j < N; j++){
	  int look = (pos + j*j) % N;
	  if(set->cells[look].state == empty)
	    return false;
	  if(set->cells[look].state == in_use &&
	     (strcmp(set->cells[look].element, value) == 0)){
	    return true;
	  }
	}
      }
    else if(isDoubleHashing(mode)) // double hash
      {
	int temp = hashFunc2(value, N);

	for(int j = 1; j < N; j++){
	  int look = (pos + j*temp) % N;
	  if(set->cells[look].state == empty)
	    return false;
	  if(set->cells[look].state == in_use &&
	     (strcmp(set->cells[look].element, value) == 0)){
	    return true;
	  }
	}
      }
  } else {
    struct CC *cc = &set->cell_chains[pos];
    return find_chain(value, cc);
  }
  return false;
}

void print_set (struct hashset* set)
{
  int i = 0;
  for(; i < set->size; i++){
    if (!isSeparateChaining(mode)) {
      if(set->cells[i].state == in_use)
	printf("Cell %5d: %s\n", i, set->cells[i].element);
      if(set->cells[i].state == empty)
	printf("Cell %5d: empty\n", i);
      if(set->cells[i].state == deleted)
	printf("Cell %5d: deleted\n", i);
    } else {
      char* chains = "";
      struct CC chaini = set->cell_chains[i];
      printf("Cell %5d: %s\n", i, print_chain(chains, &chaini));
    }
  }
}

void print_stats (struct hashset* set)
{
  printf("Collision times: %d\n", set->collision);
  printf("Entry number: %d\n", set->num_entries);
  printf("Average collisions per access: %lf\n", (double)set->collision / (double)set->num_entries);
}

struct CC* insert_chain(Value_Type value, struct CC *cell_chain)
{
  if (cell_chain->value == NULL) {
    cell_chain->value = value;
    cell_chain->collision = 0;
    return cell_chain;
  } else if (cell_chain->value == value) {
    cell_chain->collision = 0;
    return cell_chain;
  } else if (cell_chain->link == NULL) {
    cell_chain = initialise_cell_chain(value);
    return cell_chain;
  } else {
    cell_chain->link = insert_chain(value, cell_chain->link);
    cell_chain->collision = cell_chain->link->collision + 1;
    return cell_chain;
  }
  return cell_chain;
}

struct CC* initialise_cell_chain(Value_Type value) {
  struct CC* cell_chain = (struct CC*) malloc(sizeof(struct CC));
  check(cell_chain);
  cell_chain->value = value;
  cell_chain->collision = 0;
  cell_chain->link = NULL;
  return cell_chain;
  
}

bool find_chain (Value_Type value, struct CC *cell_chain) {
  if (cell_chain->value == NULL) {
    return 0;
  }
  if (cell_chain->value == value) {
    return 1;
  }
  if (cell_chain->link == NULL) {
    return 0;
  } else {
    return find_chain(value, cell_chain->link);
  }
  return 0;
}

void tidy_cell_chain(struct CC *cc) {
  if (cc->link == NULL) {
    free(cc->value);
      } else {
    tidy_cell_chain(cc->link);
    free(cc->value);
  }
  free(cc);
}

char* print_chain(char* out, struct CC *cc) {
  strcat(out, cc->value);
  if (cc->link != NULL) {
    strcat(out, strcat(", ", print_chain(out, cc->link)));
  }
  return out;
}
