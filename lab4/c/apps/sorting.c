
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../global.h"
#include "../pq.h"

// set to 1 or compile with -DDEBUG=1 to print debug lines
// ensure this is 0 when submitting
#define DEBUG 0


// Let's do some weirdly complicated ranking of words
// based on their first five characters. You don't need
// to understand this but we're mapping all characters to
// 0-26 and then subdividing the integers into five levels of
// width 27, so every string with a different first five 
// characters gets a different code 

int offset(int n){
 int res = 27;
 while(n>0){ 
   int new = res*27;
    // Should not happen as n should be <6 
   if(new < res){ printf("OVERFLOW in offset\n"); exit(-1); }
   res=new;
   n--;
 }
 return res;
}

int get_bucket(char c){
  if(c < 65) return 0;
  if(c>122) return 0;
  if(c>90) c-=32;
  int b = (c-64);
  return b;
}

int get_code(char* str){
  int len = strlen(str);

  // What would happen if we just returned len as the code?
  // What impact would this have on the operations we perform
  // on our data structures?

  int res = 0;
  int MAX = 5;
  int end = (len>MAX) ? MAX : len;
  for(int i=end-1;i>=0;i--){
    int c = (int)str[i];
    int new = res+(offset((MAX-1)-i)*get_bucket(c)); 
    // Should not happen as 27^6 < 2^32  
    if(new < res){ printf("OVERFLOW in get_code\n"); exit(-1); }
    res = new;
  }
  return res;
}

char* prog_name = 0;

int main (int argc, char *argv[]) {
  prog_name=argv[0];

  int n; 
  scanf("%d", &n);
  PriorityQueue pq = initialize_pq(n);

  printf("INSERTING...\n");
  for (int i = 0; i < n; i++) {
    char* tmp = malloc(sizeof(char*)*80);
    check(tmp);
    scanf("%s", tmp);
    int p = get_code(tmp);
#if DEBUG==1
    printf("Insert %s with priority %d\n",tmp,p);
#endif
    // memory deallocated on pop
    insert(pq,tmp,get_code(tmp));
#if DEBUG==1
    printf("==============\n");
    print(pq);
    printf("==============\n");
#endif
  }
  printf("POPPING...\n");
  while(!is_empty(pq)){
    char* tmp = pop_min(pq);
    printf("%s\n",tmp);
    free(tmp);
#if DEBUG==1
    printf("==============\n");
    print(pq);
    printf("==============\n");
#endif
  }
  tidy(pq);
}
