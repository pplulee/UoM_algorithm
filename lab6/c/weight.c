#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>
#include <limits.h>
#include <math.h>

#include "general.h"
#include "weight.h"

///////////////////////// Weights
#define _WINF LONG_MAX
#define _WNINF LONG_MIN


weight_t weight_of_int(signed long w) {
  if (w==_WINF || w==_WNINF) error("Weight overflow");
  return (weight_t){w};
}

weight_t weight_inf() {
  return (weight_t){_WINF };
}

weight_t weight_neg_inf() {
  return (weight_t){_WNINF };
}

weight_t weight_zero() {
  return weight_of_int(0);
}

weight_t weight_of_dbl(double w) {
  return weight_of_int(round(w));
}

bool weight_is_inf(weight_t a) {
  return a.__w == _WINF;
}

bool weight_is_neg_inf(weight_t a) {
  return a.__w == _WNINF;
}

bool weight_is_finite(weight_t a) {
  return !weight_is_inf(a) && !weight_is_neg_inf(a);
}

raw_weight_t weight_to_int(weight_t a) {
  assertmsg(weight_is_finite(a),"Weight must be finite");
  return a.__w;
}





weight_t weight_add(weight_t a, weight_t b) {
  if (weight_is_inf(a)) {
    assertmsg(!weight_is_neg_inf(b), "inf + -inf undefined");
    return weight_inf();
  } else if (weight_is_neg_inf(a)) {
    assertmsg(!weight_is_inf(b), "-inf + inf undefined");
    return weight_neg_inf();
  } else if (weight_is_inf(b)) {
    return weight_inf();
  } else if (weight_is_neg_inf(b)) {
    return weight_neg_inf();
  } else {
    signed long res = a.__w + b.__w; // Not using __builtin_add_overflow as ancient compiler on lab machines does not support it.
//     if (__builtin_add_overflow(a.__w,b.__w,&res)) error("Weight overflow");
    return weight_of_int(res);
  }
}

weight_t weight_sub(weight_t a, weight_t b) {
  if (weight_is_inf(a)) {
    assertmsg(!weight_is_inf(b), "inf - inf undefined");
    return weight_inf();
  } else if (weight_is_neg_inf(a)) {
    assertmsg(!weight_is_neg_inf(b), "-inf - -inf undefined");
    return weight_neg_inf();
  } else if (weight_is_inf(b)) {
    return weight_neg_inf();
  } else if (weight_is_neg_inf(b)) {
    return weight_inf();
  } else {
    signed long res = a.__w - b.__w; // Not using __builtin_sub_overflow as ancient compiler on lab machines does not support it.
//     if (__builtin_sub_overflow(a.__w,b.__w,&res)) error("Weight overflow");
    return weight_of_int(res);
  }
}


bool weight_less(weight_t a, weight_t b) {
  return a.__w < b.__w;
}

bool weight_eq(weight_t a, weight_t b) {
  return a.__w == b.__w;
}


void print_weight(FILE *f, weight_t a) {
  if (weight_is_inf(a)) fprintf(f,"inf");
  else if (weight_is_neg_inf(a)) fprintf(f,"-inf");
  else fprintf(f,"%ld",weight_to_int(a));
}

void print_weight_stdout(weight_t a) {
  if (weight_is_inf(a)) printf("inf");
  else if (weight_is_neg_inf(a)) printf("-inf");
  else printf("%ld",weight_to_int(a));
}

