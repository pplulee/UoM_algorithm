#ifndef _GENERAL_H
#define _GENERAL_H


/**
 * Allocate memory, and exit in a defined way if this fails.
 */
void *calloc_fail(size_t elsize, size_t num);

/// Type-safe wrapper for calloc
#define CALLOC(ty,num) ((ty*)calloc_fail(sizeof(ty),num))

/**
 * Print error message and exit with value 1.
 * Accepts printf-format codes.
 */
void error(const char *format, ...) __attribute__((noreturn)) __attribute__((format(printf, 1, 2)));

/**
 * Assertion with error message, accepts printf-format codes
 */
#define assertmsg(expr,fmt, ...) {if (!(expr)) __asserterror(__FILE__,__LINE__,__PRETTY_FUNCTION__,fmt, ##__VA_ARGS__);}



/**
 * Log message
 */
void msg(int verb, const char *format, ...) __attribute__((format(printf, 2, 3)));

#define msg0(fmt, ...) msg(0,fmt, ##__VA_ARGS__)
#define msg1(fmt, ...) msg(1,fmt, ##__VA_ARGS__)

void set_msg_verb(int v);


/// Internally used only
void __asserterror(const char *file, int line, const char * func, const char *format, ...)
  __attribute__((noreturn)) __attribute__((format(printf, 4, 5)));


/// Scan a size_t
size_t scan_size(FILE *file);


#endif

