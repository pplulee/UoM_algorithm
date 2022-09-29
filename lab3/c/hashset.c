#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define __USE_BSD
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

// Your code

struct hashset* initialize_set (int size)  
{
// TODO create initial hash table
}

void tidy(struct hashset* set)
{
// TODO tidy up
}

int size(struct hashset* set){
// TODO return number of values stored in table
} 

struct hashset* insert (Value_Type value, struct hashset* set)
{
// TODO code for inserting into hash table
}

bool find (Value_Type value, struct hashset* set)
{
// TODO code for looking up in hash table
}

void print_set (struct hashset* set)
{
// TODO code for printing hash table
}

void print_stats (struct hashset* set)
{
// TODO code for printing statistics
}
