#ifndef _AIRPORTS_H
#define _AIRPORTS_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdarg.h>
#include <stdbool.h>

#include "graph.h"


typedef node_t apid_t;

/** Read airport list from file.
 * The file has the following format:
 *
 * num_ids       // Maximum Id + 1
 * num_airports  // Number of actual airport entries in file
 * Id IATA Lat Long // Entry for an airport.
 * ...
 *
 */
void ap_read(FILE *f);

/**
 * Read routes from file.
 */
void ap_read_routes(FILE *f);

/**
 * Reads airport list and routes from files "airports.txt" and "routes.txt", which must be in the current directory.
 */
void ap_std_init();

/**
 * Returns a graph where the nodes are airport IDs, and the edges represent connections. They are labeled with the distance in km.
 *
 * @note The graph is constructed by @ref ap_read_routes, this function only returns it, and is thus O(1).
 *
 */
graph_t const *ap_get_graph();


/**
 * Free memory used for airport database and graph.
 */
void ap_delete();

/**
 * Remove the entry for an airport.
 * @pre id < num_ids, but not necessarily valid!
 */
void ap_invalidate_id(apid_t id);

/**
 * Get maximum id + 1
 */
size_t ap_get_num_ids();

/**
 * Return true if id is actually assigned to an airport.
 * That is, id < num_ids, and there is an airport entry for this id.
 */
bool ap_is_valid_id(apid_t id);

/// @pre id must be valid
char *ap_get_code(apid_t id);

/// @pre id must be valid
double ap_get_lat(apid_t id);

/// @pre id must be valid
double ap_get_lng(apid_t id);


/**
 * Exit on invalid id, or return unchanged id.
 * @pre id must be valid
 */
apid_t ap_check_id(apid_t id);

bool ap_is_valid_code(char const *code);

/**
 * Exits with defined error message on invalid code.
 */
apid_t ap_get_id(char const *code);

/**
 * Get the distance, in km, between two airports.
 * This uses the haversine-formula, regarding the earth as sphere with radius 6371km.
 * @pre ids must be valid
 */
double ap_get_dist_dbl(apid_t id1, apid_t id2);

/**
 * Get the distance between two airports as weight.
 */
weight_t ap_get_dist(apid_t id1, apid_t id2);



#endif

