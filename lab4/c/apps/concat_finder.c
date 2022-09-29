
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../global.h"
#include "../pq.h"

#define MAX_STR_LEN 100

void tidy_up(PriorityQueue pq)
{
  while(!is_empty(pq)){
    char* s = pop_min(pq);
    free(s);
  }
  tidy(pq);
}

char* prog_name = 0;

int main (int argc, char *argv[]) {
  prog_name=argv[0];

  PriorityQueue pq = initialize_pq(1000);

  char* search = malloc(sizeof(char*)*MAX_STR_LEN);
  check(search);
  scanf("%s",search);
  printf("Searching for %s\n",search);

  int n;
  scanf("%d",&n);

  for (int i = 0; i < n; i++) {
    char* tmp = malloc(sizeof(char*)*MAX_STR_LEN);
    check(tmp);
    scanf("%s", tmp);
    if(strcmp(tmp,search) == 0){
      printf("Found\n");
      tidy_up(pq);
      free(search);
      free(tmp);
      return 0;
    }
    if(strlen(tmp) < strlen(search)){
      // pq owns memory
      insert(pq,tmp,strlen(tmp));
    }
  }

  PriorityQueue done = initialize_pq(1000);
  
  while(!is_empty(pq)){
    char* next = pop_min(pq);
    printf("Pop %s\n",next);
    PriorityQueue rebuild = initialize_pq(1000);
    while(!is_empty(done)){
      char* s = pop_min(done);
      insert(rebuild,s,strlen(s));
      //printf("Try with %s\n",s);
      if(strlen(s)+strlen(next) <= strlen(search)){
        char* left = malloc(sizeof(char*)*MAX_STR_LEN);
        char* right = malloc(sizeof(char*)*MAX_STR_LEN);
	check(left);
	check(right);
        strcpy(left,next);
        strcat(left,s);
        strcpy(right,s);
        strcat(right,next);
        if(strcmp(left,search)==0 || strcmp(right,search)==0){
          printf("Found\n");
	  tidy_up(pq);
	  tidy_up(done);
	  tidy_up(rebuild);
	  free(left);
	  free(right);
	  free(search);
	  free(next);
          return 0;
        } 
	// pq owns memory
        insert(pq,left,strlen(left));
        insert(pq,right,strlen(right));
      }
    }
    // Can remove conditional if PriorityQueue does not contain duplicates
    //printf("Done with %s\n",next);
    if(!contains(rebuild,next,strlen(next))){
      //printf("Using %s\n",next);
      insert(rebuild,next,strlen(next));
    }
    else{
      free(next);
    }
    tidy(done);
    done = rebuild;
  }
  tidy_up(pq);
  tidy_up(done);
  free(search);
  printf("Not Found\n");
  return 0;
}
