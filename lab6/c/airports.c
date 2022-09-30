#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>
#include <assert.h>
#include <math.h>

#include "hashmap.h"
#include "general.h"
#include "graph.h"

#include "airports.h"


#define R 6371
#define TO_RAD (3.1415926536 / 180)
double dist(double lat1, double lng1, double lat2, double lng2)
{
	double dx, dy, dz;
	lng1 -= lng2;
	lng1 *= TO_RAD, lat1 *= TO_RAD, lat2 *= TO_RAD;

	dz = sin(lat1) - sin(lat2);
	dx = cos(lng1) * cos(lat1) - cos(lat2);
	dy = sin(lng1) * cos(lat1);
	return asin(sqrt(dx * dx + dy * dy + dz * dz) / 2) * 2 * R;
}

typedef struct {
  char code[4]; // We use the empty string to indicate unassigned ids
  double lat;
  double lng;
} airport_t;

size_t num_apids = 0;
airport_t *airports = NULL;
hashmap_t *code_id_map = NULL;

graph_t *route_g = NULL;


size_t ap_get_num_ids() {return num_apids;}


void ap_read(FILE *f) {
  size_t n;

  assert(airports == NULL && code_id_map==NULL);

  if (fscanf(f,"%zu",&num_apids)!=1) error("Error reading airport file");
  if (fscanf(f,"%zu",&n)!=1) error("Error reading airport file");

  airports = CALLOC(airport_t, num_apids);

  code_id_map = hashmap_new(num_apids,HASH_1_LINEAR_PROBING);

  for (size_t i=0;i<n;++i) {

    apid_t id;
    char code[4];
    double lat;
    double lng;

    if (fscanf(f,"%zu %3s %lf %lf\n",&id,(char*)&code,&lat,&lng) != 4)
        error("Error reading airport file");

    if (!(id<num_apids)) error("Invalid airport ID: %zu", id);

    airports[id] = (airport_t){{code[0],code[1],code[2],0},lat,lng};


    hashmap_insert(code,id,code_id_map);
  }

//   printf("Read %zu airports\n",n);

}

void ap_read_routes(FILE *f) {
  size_t num_edges = scan_size(f);

  assert(route_g == NULL);
  route_g = graph_new(ap_get_num_ids());

  for (int i=0;i<num_edges;++i) {
    apid_t id1 = ap_check_id(scan_size(f));
    apid_t id2 = ap_check_id(scan_size(f));

    weight_t dist = ap_get_dist(id1,id2);

    graph_add_edge(route_g,id1,dist,id2);
  }
}

FILE *fopenchk(char const *name, char const *mode) {
  FILE *f = fopen(name,mode);
  if (!f) error("Error opening '%s' for %s",name,mode);
  return f;
}

void ap_std_init() {
  {
    FILE *f = fopenchk("../data/airports.txt","r");
    ap_read(f);
    fclose(f);
  }

  {
    FILE *f = fopenchk("../data/routes.txt","r");
    ap_read_routes(f);
    fclose(f);
  }
}



graph_t const *ap_get_graph() {return route_g;}

weight_t ap_get_dist(apid_t id1, apid_t id2) {
  return weight_of_int(round(ap_get_dist_dbl(id1,id2)));
}



void ap_delete() {
  if (airports) free(airports);
  if (code_id_map) hashmap_delete(code_id_map);
  if (route_g) graph_delete(route_g);
}

bool ap_is_valid_id(apid_t id) {
   // printf("id: %zu",id);
  //  printf("code: %s", airports[id].code);
  return id<num_apids && airports[id].code[0]!=0;
}

void ap_invalidate_id(apid_t id) {
  assert(id < num_apids);
  // Note: As our hashtables do not support delete, we insert a validity check after retrieving a code.
  airports[id].code[0] = 0;
}


apid_t ap_check_id(apid_t id) {
  if (!ap_is_valid_id(id)) error("Invalid airport id: %zu",id);
  return id;
}


char *ap_get_code(apid_t id) {
  assert(ap_is_valid_id(id));
  return airports[id].code;
};
double ap_get_lat(apid_t id) {
  assert(ap_is_valid_id(id));
  return airports[id].lat;
};

double ap_get_lng(apid_t id) {
  assert(ap_is_valid_id(id));
  return airports[id].lng;
};

bool ap_get_id_aux(char const *code, apid_t *res) {
  return (hashmap_lookup(code,res,code_id_map) && ap_is_valid_id(*res));
}

bool ap_is_valid_code(char const *code) {
  apid_t res;
  return ap_get_id_aux(code,&res);
}

apid_t ap_get_id(char const *code) {
  apid_t res;
  if (!ap_get_id_aux(code,&res)) error("Unknown airport ID: %s",code);

  return res;
}

double ap_get_dist_dbl(apid_t id1, apid_t id2) {
  return dist(ap_get_lat(id1), ap_get_lng(id1), ap_get_lat(id2), ap_get_lng(id2));
}


