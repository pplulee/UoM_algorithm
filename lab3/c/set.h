// Giles Reger, 2019

// Support Dynamic Array and Hashtable implementations
#ifdef DARRAY

#include "darray.h"
typedef struct darray* Set;    

#endif 

#ifdef BSTREE

#include "bstree.h"
typedef struct bstree* Set;

#endif

#ifdef HASH

#include "hashset.h"
typedef struct hashset* Set;

#endif

// set initial size of set
Set initialize_set (int size);     
// tidy up the set data structure e.g. deallocate memory
void tidy (Set); 

int size(Set);

// This returns a Set as it might be necessary to 
// change the underlying pointer e.g. correct usage is
// set = insert(x,set);
Set insert (Value_Type, Set);

bool find (Value_Type, Set);

// Helper functions
void print_set (Set);
void print_stats (Set);
