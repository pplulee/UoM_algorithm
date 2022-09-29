// Giles Reger, 2019

#include <stdbool.h>

typedef char* Value_Type;

// Use, e.g., -DLLIST to select the linked list implementation
// See makefile

#ifdef LLIST 

struct llist;
typedef struct llist* PriorityQueue; 

#endif

#ifdef AVLTREE 

struct avltree;
typedef struct avltree* PriorityQueue;

#endif

#ifdef SKIPLIST 

struct skiplist;
typedef struct skiplist* PriorityQueue;

#endif

#ifdef BINARYHEAP 

struct binaryheap;
typedef struct binaryHeap* PriorityQueue;

#endif

// initialize, most data structures will ignore size 
PriorityQueue initialize_pq (int size);     

// tidy up the data structure e.g. deallocate memory
void tidy (PriorityQueue);

//Check if element is contained in queue with a given priority
bool contains(PriorityQueue, Value_Type, int);

// Insert element into queue, with given priority
// Assumes priority queue is mutable
void insert(PriorityQueue, Value_Type, int);

// Check if queue is empty
bool is_empty(PriorityQueue);

// Retrieve and remove an element with minimal priority
Value_Type pop_min(PriorityQueue);

// Print queue 
void print(PriorityQueue);
