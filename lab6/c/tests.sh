#!/bin/sh

 ./sp pq
 ./sp bfs
 ./sp bellman-ford
 ./sp bellman-ford-neg
 ./sp dijkstra
 ./sp dijkstra astar

for algo in bfs bellman-ford dijkstra astar; do
   ./ap route $algo MAN MAN
   ./ap route $algo MAN SYD
   ./ap route $algo MAN MUC
   ./ap route $algo MAN ROA

   ./ap route $algo TTA MAN
   ./ap route $algo MAN TTA
done

 ./ap count MAN
 ./ap count SYD
 ./ap count TTA
