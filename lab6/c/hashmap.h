#ifndef _HASHMAP_H
#define _HASHMAP_H
// Giles Reger, 2019

#include <stdbool.h> 

typedef enum HashingModes { HASH_1_LINEAR_PROBING=0,
                    HASH_1_QUADRATIC_PROBING=1, 
                    HASH_1_DOUBLE_HASHING=2, 
                    HASH_1_SEPARATE_CHAINING=3,
                    HASH_2_LINEAR_PROBING=4, 
                    HASH_2_QUADRATIC_PROBING=5, 
                    HASH_2_DOUBLE_HASHING=6, 
                    HASH_2_SEPARATE_CHAINING=7}
  hashing_mode_t;

typedef char const* hashmap_key_t;
typedef size_t hashmap_value_t;
// Should be redefined if changing Value_Type
int compare_keys(hashmap_key_t,hashmap_key_t);


typedef struct _hashmap_t hashmap_t;

hashmap_t* hashmap_new (size_t size, hashing_mode_t mode);
void hashmap_delete (hashmap_t*);

size_t hashmap_get_size(const hashmap_t* set);

hashmap_t* hashmap_insert(hashmap_key_t key, hashmap_value_t value, hashmap_t* set);

bool hashmap_lookup(hashmap_key_t key, hashmap_value_t *value, hashmap_t const* set);
bool hashmap_contains(hashmap_key_t key, const hashmap_t* set);

// Helper functions
void hashmap_print_set (hashmap_t const*);
void hashmap_print_stats (hashmap_t const*);

#endif
