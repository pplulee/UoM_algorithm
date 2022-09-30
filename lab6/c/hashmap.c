#define __USE_XOPEN_EXTENDED
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <assert.h>
#include <string.h>

#include <math.h>

#include "hashmap.h"
#include "general.h"

typedef char *hashmap_mkey_t;

// This is a cell struct assuming Open Addressing
// You will need alternative data-structurs for separate chaining
typedef struct
{ // hash-table entry
  hashmap_mkey_t key;
  hashmap_value_t value;
  enum {empty, in_use, deleted} state;
} cell;

struct _hashmap_t
{
  cell *cells;
  size_t size; // cell cells [table_size];
  size_t num_entries; // number of cells in_use
  hashing_mode_t mode;
  //TODO add anything else that you need
  unsigned long long collision;
};

typedef size_t hashcode_t; // unsigned integer type <= size_t !

// Can be redefined if Value_Type changes
int compare_keys(hashmap_key_t a, hashmap_key_t b){
  return strcmp(a,b);
}

// Helper functions for finding prime numbers 
bool isPrime (size_t n)
{
  for (size_t i = 2; i*i <= n; i++)
    if (n % i == 0)
      return false;
  return true;
}

size_t nextPrime(size_t n)
{
  for (; !isPrime(n); n++);
  return n;
}
// h = x0*a^(k-1) + x1*a^(k-2) + ... + x(k-2)*a + x(k-1)
// h = |ak + b| mod N
hashcode_t hashFunc(hashmap_key_t k, size_t N)
{
  int temp = 1; int a = 41;
  size_t len = strlen(k);
  long long h = 0;

  //printf("%s, len: %zu, k[%zu]: %lld\n", k, len, len - 1, h);
  size_t i=len;
  while (i>0) {
    --i;
    h += k[i] * temp;
    //printf("h += k[%zu](%d) * %d, h = %lld\n", i, k[i], a, h);
    temp *= a;
  }

  //printf("%lld\n", h);
  h = (hashcode_t)(labs(h) % N);
  return h;
}


bool isLinearProbing(hashing_mode_t mode){
  return mode == HASH_1_LINEAR_PROBING || mode == HASH_2_LINEAR_PROBING;
}
bool isQuadraticProbing(hashing_mode_t mode){
  return mode == HASH_1_QUADRATIC_PROBING || mode == HASH_2_QUADRATIC_PROBING;
}
bool isDoubleHashing(hashing_mode_t mode){
  return mode == HASH_1_DOUBLE_HASHING || mode == HASH_2_DOUBLE_HASHING;
}


#define DOUBLE_HASH_Q 7919

hashmap_t* hashmap_new(size_t size, hashing_mode_t mode)
{
  if (size<5) size=5;
  size=nextPrime(size);

  if (isDoubleHashing(mode) && size <= DOUBLE_HASH_Q ) {
    assert(isPrime(DOUBLE_HASH_Q));
    size = nextPrime(DOUBLE_HASH_Q + 1);
  }

  hashmap_t* set = CALLOC(hashmap_t,1);
  set->cells = CALLOC(cell,size);
  set->size = size;
  set->num_entries = 0;
  set->collision = 0;
  set->mode = mode;

  for(size_t i = 0; i < size; i++){
    set->cells[i].state = empty;
  }
  return set;

}

void hashmap_delete(hashmap_t* set)
{
  for(size_t i=0;i<set->size;i++){
    if(set->cells[i].state == in_use){
      free(set->cells[i].key);
    }
  }
  free(set->cells);
  free(set);
}

size_t hashmap_get_size(hashmap_t const* set){ return set->num_entries; }

// insertion

void insertCell(hashmap_key_t k, hashmap_value_t v, hashmap_t* set, size_t pos)
{
 set->cells[pos].key = strdup(k);
 set->cells[pos].value=v;
 set->cells[pos].state = in_use;
 set->num_entries ++;
  return;
}

hashmap_t* rehash(hashmap_t* set)
{
  size_t N =set->size;
  size_t newSize = nextPrime(2*N);
  hashmap_t* new_set = hashmap_new(newSize, set->mode);
  for(size_t i = 0; i < N; i++){
    if(set->cells[i].state == in_use)
      hashmap_insert(set->cells[i].key, set->cells[i].value, new_set);
  }
  hashmap_delete(set);
  return new_set;
}


hashmap_t* hashmap_insert (hashmap_key_t key, hashmap_value_t value, hashmap_t* set)
{
  if(hashmap_contains(key, set)) error("Duplicate key %s", key); // detect duplicate

  size_t N = set->size;
  if(   set->num_entries >= N
    || (isQuadraticProbing(set->mode) && set->num_entries >= N / 2 ))
  {
    set = rehash(set);
  }
  N = set->size;

  //printf("INSERT %s -> %zu\n", key,value);

  hashcode_t pos = hashFunc(key, N);

  // insert into empty cell
  if(set->cells[pos].state != in_use)
    insertCell(key, value, set, pos);

  else{
    if(isLinearProbing(set->mode)) // linear probing: A[(i+j)mod N]
    {

      for(size_t j = 1; j < N; j++){
        size_t look = (pos + j) % N;
       set->collision ++;
        if(set->cells[look].state != in_use){
          insertCell(key, value, set, look);
          break;
        }
      }
    }
    else if(isQuadraticProbing(set->mode)) // quadratic probing: A[(i+j^2)mod N]
    {

      for(size_t j = 1; j < N; j++){
        size_t look = (pos + j*j) % N;

       set->collision ++;
        if(set->cells[look].state != in_use){
          insertCell(key, value, set, look);
          break;
        }
      }
    }
    else if(isDoubleHashing(set->mode)) // double hash: A[(i+j*h'(k))mod N] h'(k)=q-(k mod q)
    {
      size_t q = DOUBLE_HASH_Q; // q<N a prime number
      assert(q<N);

      size_t temp = q - pos % q;

      for(size_t j = 1; j < N; j++){
        size_t look = (pos + j*temp) % N;

       set->collision ++;
        if(set->cells[look].state != in_use){
          insertCell(key, value, set, look);
          break;
        }
      }
    } else assert(false);
  }
  return set;
}

bool hashmap_lookup(hashmap_key_t key, hashmap_value_t *value, hashmap_t const* set) {
  size_t N =set->size;
  hashcode_t pos = hashFunc(key, N);

  if(set->cells[pos].state == in_use
        && (strcmp(set->cells[pos].key, key) == 0))
  {
    if (value) *value=set->cells[pos].value;
    return true;
  }
  else if(isLinearProbing(set->mode)) // linear probing
  {
    for(size_t j = 1; j < N; j++){
      size_t look = (pos + j) % N;
      if(set->cells[look].state == empty)
        return false;
      if(set->cells[look].state == in_use
        && (strcmp(set->cells[look].key, key) == 0))
      {
        if (value) *value=set->cells[look].value;
        return true;
      }
    }
  }
  else if(isQuadraticProbing(set->mode)) // quadratic probing
  {
    for(size_t j = 1; j < N; j++){
      size_t look = (pos + j*j) % N;

      if(set->cells[look].state == empty)
        return false;
      if(set->cells[look].state == in_use &&
        (strcmp(set->cells[look].key, key) == 0))
      {
        if (value) *value=set->cells[look].value;
        return true;
      }
    }
  }
  else if(isDoubleHashing(set->mode)) // double hash
  {
    size_t q = DOUBLE_HASH_Q;
    size_t temp = q - pos % q;
    assert(q<N);

    for(size_t j = 1; j < N; j++){
      size_t look = (pos + j*temp) % N;

      if(set->cells[look].state == empty)
        return false;
      if(set->cells[look].state == in_use &&
        (strcmp(set->cells[look].key, key) == 0))
      {
        if (value) *value=set->cells[look].value;
        return true;
      }
    }
  }
  return false;
}


bool hashmap_contains (hashmap_key_t key, hashmap_t const* set)
{
  return hashmap_lookup(key,NULL,set);
}

void hashmap_print_set (hashmap_t const* set)
{
  for(size_t i = 0; i < set->size; i++){
    if(set->cells[i].state == in_use)
      printf("Cell %zu: %s=>%zu\n", i, set->cells[i].key, set->cells[i].value);
    if(set->cells[i].state == empty)
      printf("Cell %zu: empty\n", i);
    if(set->cells[i].state == deleted)
      printf("Cell %zu: deleted\n", i);
  }
}

void hashmap_print_stats (hashmap_t const* set)
{
  printf("Collision times: %llu\n", set->collision);
  printf("Entry number: %zu\n", set->num_entries);
  printf("Average collisions per access: %lf\n", (double)set->collision / (double)set->num_entries);
}
