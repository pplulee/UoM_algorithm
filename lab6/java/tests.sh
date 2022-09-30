#!/bin/sh

 java -ea comp26120.sp pq
 java -ea comp26120.sp bfs
 java -ea comp26120.sp bellman-ford
 java -ea comp26120.sp bellman-ford-neg
 java -ea comp26120.sp dijkstra
 java -ea comp26120.sp dijkstra astar

for algo in bfs bellman-ford dijkstra astar; do
   java -ea comp26120.ap route $algo MAN MAN
   java -ea comp26120.ap route $algo MAN SYD
   java -ea comp26120.ap route $algo MAN MUC
   java -ea comp26120.ap route $algo MAN ROA

   java -ea comp26120.ap route $algo TTA MAN
   java -ea comp26120.ap route $algo MAN TTA
done

 java -ea comp26120.ap count MAN
 java -ea comp26120.ap count SYD
 java -ea comp26120.ap count TTA
