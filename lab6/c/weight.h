#ifndef _WEIGHT_H
#define _WEIGHT_H

#include <limits.h>

/// Weight and distance type.

/*
 * We provide a weight-type, that implements integers with +infinity and -infinity, and provides
 * overflow-checked operations, which fail on underflows or overflows.
 *
 * It is wrapped into a struct, to prevent accidental access to the raw integer.
 */

typedef signed long raw_weight_t;

#define WEIGHT_MIN (LONG_MIN+1)
#define WEIGHT_MAX (LONG_MAX-1)



typedef struct _weight_t {raw_weight_t __w;} weight_t;

/// These conversion functions only work for *finite* weights
weight_t weight_of_int(raw_weight_t w);
weight_t weight_of_dbl(double w);
raw_weight_t weight_to_int(weight_t a);

/// Zero weight
weight_t weight_zero();
/// +infinity
weight_t weight_inf();
/// -infinity
weight_t weight_neg_inf();

/// Check for +infinity
bool weight_is_inf(weight_t a);
/// Check for -infinity
bool weight_is_neg_inf(weight_t a);
/// Check that weight is finite, i.e., not +inf nor -inf
bool weight_is_finite(weight_t a);

/**
 * Add weights. Adding to +inf or -inf will n ot change the weight.
 * Adding +inf and -inf is undefined!
 * @pre {a,b} != {+inf,-inf}
 */
weight_t weight_add(weight_t a, weight_t b);

/**
 * Subtract weights.
 *
 *    a     b     result
 *    ----------------
 *    inf   inf   undef
 *    inf   *     inf
 *    -inf  -inf  unfef
 *    -inf  *     -inf
 *    fin   inf   -inf
 *    fin   -inf  inf
 *
 */
weight_t weight_sub(weight_t a, weight_t b);

/// Compare <
bool weight_less(weight_t a, weight_t b);

/// Compare ==
bool weight_eq(weight_t a, weight_t b);

/// Pretty print
void print_weight(FILE *f, weight_t a);
void print_weight_stdout(weight_t a);

#endif


