
#include "darray.h"

void sort(struct darray* arr, int select);


// Iterative Sorting Algorithms

// You must implement this one
void insertion_sort(struct darray* arr);

// We recommend implementing this one as it is an interesting
// exploration of the trade-off between time and space complexity
void bucket_sort(struct darray* arr);

// Think about whether this is applicable in this scenario
void counting_sort(struct darray* arr);

// This has the same theoretical complexity as insertion sort
// Does it have the same practical complexity?
void bubble_sort(struct darray* arr);

void selection_sort(struct darray* arr);


// Recursive Sorting Algorithms

// You must implement this one
void quick_sort(struct darray* arr);

// We recommend implementing this one as it is a common
// question in coding interviews and is an interesting case
// for computing complexities
void merge_sort(struct darray* arr);

// See https://en.wikipedia.org/wiki/Timsort
void tim_sort(struct darray* arr);
