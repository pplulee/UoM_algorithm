#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "global.h"

// We should define compare for Value_Type here
int compare(char* a, char* b){
  return strcmp(a,b);
}

void check (void *memory)
{ // check result from strdup, malloc etc.
  if (memory == NULL)
  {
    fprintf (stderr, "%s: out of memory\n", prog_name);
    exit (3);
  }
}

