#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#define __USE_BSD
#include <string.h>

#include "global.h"
#include "bstree.h"


// Can be redefined if Value_Type changes
int compare(Value_Type a, Value_Type b){
  return strcmp(a,b);
}


struct bstree* initialize_set (int size)  
{
  // An empty tree is represented by NULL
  return NULL;
}

void tidy(struct bstree* tree)
{
  if(tree){
    tidy(tree->left);
    tidy(tree->right);
    // assumes tree owns value memory
    free(tree->value);
    free(tree);
  }
}

int size(struct bstree* tree){
  if(tree){
    return 1 + size(tree->left) + size(tree->right);
  }
  return 0;
} 

struct bstree* insert (Value_Type value, struct bstree* tree)
{
  if(tree){
    // TODO if tree is not NULL then insert into the correct sub-tree
  }
  else{
    // TODO otherwise create a new node containing the value
  }
  return tree;
}

bool find (Value_Type value, struct bstree* tree)
{
  if(tree){
    //TODO complete the find function
  }
  // if tree is NULL then it contains no values
  return false;
}

// You can update this if you want
void print_set_recursive(struct bstree* tree, int depth)
{
  if(tree){
    for(unsigned i=0;i<depth;i++){ printf(" "); }
    printf("%s\n",tree->value);
    print_set_recursive(tree->left,depth+1);
    print_set_recursive(tree->right,depth+1);
  }
} 
// You can update this if you want
void print_set (struct bstree* tree)
{
 printf("Tree:\n");
 print_set_recursive(tree,0);
}

void print_stats (struct bstree* tree)
{
 // TODO update code to record and print statistics
}
