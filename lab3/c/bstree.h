// Giles Reger, 2019

#include <stdbool.h>

typedef char* Value_Type;
// Should be redefined if changing Value_Type
int compare(Value_Type,Value_Type);

struct bstree 
{
  Value_Type value;
  struct bstree* left;
  struct bstree* right;
  // TODO add fields for statistics
};

struct bstree* initialize_set (int size);     
void tidy (struct bstree*); 

int size(struct bstree*);

struct bstree* insert (Value_Type value, struct bstree* set);

bool find (Value_Type value, struct bstree* set);

// Helper functions
void print_set (struct bstree*);
void print_stats (struct bstree*);

