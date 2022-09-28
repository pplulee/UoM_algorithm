// Giles Reger, 2019

#include <stdbool.h>

// Necessary as can be included more than once
#ifndef FWD_DARRAY 
#define FWD_DARRAY

enum SearchModes   { LINEAR_SEARCH=0, 
                     BINARY_SEARCH_ONE=1, 
                     BINARY_SEARCH_TWO=2, 
                     BINARY_SEARCH_THREE=3, 
                     BINARY_SEARCH_FOUR=4, 
                     BINARY_SEARCH_FIVE=5 };

typedef char* Value_Type;
// Should be redefined if changing Value_Type
int compare(Value_Type,Value_Type);

struct darray
{
  Value_Type* cells;
  int capacity;
  int size;
  bool sorted;
  // statistics
  int resizes;
};

struct darray* initialize_set (int size);     
void tidy (struct darray*); 

int size(struct darray*);

struct darray* insert (Value_Type value, struct darray* set);

bool find (Value_Type value, struct darray* set);

// Helper functions
void print_set (struct darray*);
void print_stats (struct darray*);

#endif
