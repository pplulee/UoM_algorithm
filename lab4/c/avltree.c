// Giles Reger, 2019

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "global.h"
#include "pq.h"

// Set CHECK_HB here or as a compile-time option to check whether
// the Height-Balance property holds. This slows things down a lot.
#ifndef CHECK_HB
#define CHECK_HB 0
#endif

// Structure for tree
struct avltree
{
  int priority;
  Value_Type value;
  struct avltree* left;
  struct avltree* right;
  int depth;
};

// Helper funtion for max
int max(int a, int b)
{
  if(a > b) return a;
  return b;
}

// Functions for checking HeightBalance property
int actualHeight(struct avltree* tree){
  if(tree){ return 1+max(actualHeight(tree->left),actualHeight(tree->right));}
  else return 0;
}
bool hasHeightBalanceProperty(struct avltree* tree)
{
  if(tree && tree->value==NULL){
    return hasHeightBalanceProperty(tree->left);
  }
  if(tree){
    int left = actualHeight(tree->left);
    int right = actualHeight(tree->right);
    int difference = left-right;
    if(difference<0){ difference=-difference;}
    return (difference <= 1) && hasHeightBalanceProperty(tree->left) && hasHeightBalanceProperty(tree->right);
  }
  return true;
}
void checkHeightBalanceProperty(struct avltree* tree)
{
#if CHECK_HB == 1
  if(!hasHeightBalanceProperty(tree)){
    fprintf(stderr,"HeightBalanceProperty violated\n");
    exit(-1);
  }
#endif
}


struct avltree* initialize_pq (int size) 
{
  // An empty tree is represented by node with NULL
  // value. Cannot insert NULL into tree. Assumes
  // pointer Value_Type. We only use the left subtree of
  // the sentinel
  struct avltree* tree = malloc(sizeof(struct avltree));
  check(tree);
  tree->value=NULL;
  tree->left =NULL;
  tree->right=NULL;
  tree->depth=1;
  return tree;
}

// Used for checking whether a tree is the sentinel, top tree
bool sentinel(struct avltree* tree)
{
  return tree && tree->value==NULL;
}

void tidy(struct avltree* tree)
{
  if(tree){
    tidy(tree->left);
    tidy(tree->right);
    // assumes tree does not own value memory e.g. application needs to tidy this
    free(tree);
  }
}

bool is_empty(struct avltree* tree){
  if(sentinel(tree)){
    return tree->left==NULL;
  }
  return tree==NULL;
}

// Helper functions for insertion
int height(struct avltree* tree){
  if(tree){ return tree->depth;}
  return 0;
}
struct avltree* rightRotate(struct avltree* node)
{
  struct avltree* l = node->left;
  node->left = l->right;
  l->right = node;

  node->depth = max(height(node->left), height(node->right)) + 1;
  l->depth = max(height(l->left), node->depth) + 1;

  return l;
}

struct avltree* leftRotate(struct avltree* node)
{
  // TODO implement a left rotation
  return 0;
}

int getBalance(struct avltree* node)
{
  if (node == NULL) return 0;
  int balance = height(node->right) - height(node->left);
  return balance;
}

struct avltree* rebalance(struct avltree* tree){

    int parentBalance = getBalance(tree);

    if (parentBalance == -2){ // left child updated 
      if(getBalance(tree->left) <= 0){
        //printf("Case Right\n");
        return rightRotate(tree);
      }
      else{
        //printf("Case RightLeft\n");
        tree->left =  leftRotate(tree->left);
        return rightRotate(tree);
      }
    }
    if (parentBalance == 2){ // right child updated 
      // TODO implement the case where the right child has been updated
      //      using your new leftRotate function
    }

    //printf("No change\n");
    return tree;
}

struct avltree* insert_inner (struct avltree* tree, Value_Type value, int priority)
{
  if(tree){
    if(tree->priority > priority){ tree->left = insert_inner(tree->left,value,priority); }
    else { tree->right = insert_inner(tree->right,value,priority); }
    // This implementation allows duplicates 

    tree->depth = max(height(tree->left), height(tree->right)) + 1;

    tree = rebalance(tree);
  }
  else{
    //otherwise create a new node containing the value
    tree = initialize_pq(0); 
    tree->value= value;
    tree->priority=priority;
  }
  return tree;
}

void insert (struct avltree* tree, Value_Type value, int priority)
{
  if(value==NULL){
    fprintf(stderr,"Cannot insert NULL into tree, ignoring...\n");
    return;
  }
  if(sentinel(tree)){
    // sentinel case
    tree->left = insert_inner(tree->left,value,priority);
    checkHeightBalanceProperty(tree);
    return;
  }
  fprintf(stderr,"Tree is corrupted\n");
  exit(-1);
  return;
}

bool contains (struct avltree* tree, Value_Type value, int priority)
{
  if(sentinel(tree)){ tree=tree->left;}
  if(tree){
    if(tree->priority==priority){
      // if we have the right priority and right value return true
      if(compare(value,tree->value)==0){ return true; }
      // if we have the right priority but wrong value then one of the children might have the same
      // priority and, if so, we should search there. We cannot make assumptions about which child.
      return (tree->left && tree->left->priority==priority && contains(tree->left,value,priority)) || 
             (tree->right && tree-> right->priority==priority && contains(tree-> right,value,priority));
    }
    // tree sorted by priority
    if(priority < tree->priority){ return contains(tree->left,value,priority);}
    else{ return contains(tree->right,value,priority); }
  }
  // if tree is NULL then it contains no values
  return false;
}

/*
 * Observe that the minimum node cannot have a left sub-child
 * Therefore, deleting it is comparatively straightforward e.g.
 * we do not need to choose which subtree to lift
 */
Value_Type pop_min_inner(struct avltree* tree, struct avltree* parent){
  if(tree){
    Value_Type res = NULL;
    // Not min yet
    if(tree->left){
      res = pop_min_inner(tree->left,tree);
      tree->depth = max(height(tree->left), height(tree->right)) + 1;
      parent->left=rebalance(tree);
    }
    // Min node (base case for recursion)
    else{
      res = tree->value;
      if(tree->right){
        parent->left=tree->right;
      }
      else{
        parent->left=NULL;
      }
      free(tree);
    }  

    return res;
  }
  fprintf(stderr,"Tried to pop from empty AVL tree\n");
  exit(-1);
  return NULL;
}

Value_Type pop_min(struct avltree* tree)
{
  if(sentinel(tree)){
    Value_Type res =  pop_min_inner(tree->left,tree);
    checkHeightBalanceProperty(tree);
    return res;
  }
  fprintf(stderr,"The tree is corrupted\n");
  exit(-1);
  return NULL;
}


// You can update this if you want
void print_recursive(struct avltree* tree, int depth)
{
  for(unsigned i=0;i<depth;i++){ printf(" "); }
  if(tree){
    printf("(%s,%d,%d)\n",tree->value,tree->priority,tree->depth);
    print_recursive(tree->left,depth+1);
    print_recursive(tree->right,depth+1);
  }
  else printf("(NULL,-,0)\n");
} 
// You can update this if you want
void print(struct avltree* tree)
{
 printf("Tree:\n");
 if(sentinel(tree)){
   print_recursive(tree->left,0);
 }
 else print_recursive(tree,0);
}


