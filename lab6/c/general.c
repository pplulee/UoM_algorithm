#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>
#include "general.h"

void error(const char *format, ...)
{
    va_list args;
    va_start(args, format);

    printf("ERROR: ");
    vprintf(format, args);
    printf("\n");

    va_end(args);
    exit(1);
}


void __asserterror(const char *file, int line, const char *func, const char *format, ...)
{
    va_list args;
    va_start(args, format);

    printf("%s:%d: %s: Assertion failed: ", file, line,func);
    vprintf(format, args);
    printf("\n");

    va_end(args);
    exit(1);
}



int log_verb = 0;

void set_msg_verb(int v) {
  log_verb = v;
}

void msg(int verb, const char *format, ...)
{
  va_list args;
  va_start(args, format);

  if (log_verb >= verb) {
    for (int i=0;i<verb;++i) printf("    ");
    printf("LOG: ");
    vprintf(format, args);
    printf("\n");
  }
  va_end(args);

}






void *calloc_fail(size_t elsize, size_t num) {
  void *res = calloc(elsize,num);
  if (res==NULL) error("Out of memory");
  return res;
}



size_t scan_size(FILE *file) {
    size_t res;
    if (fscanf(file, "%zu", &res) == 1) return res; else error("Error reading input");
}

