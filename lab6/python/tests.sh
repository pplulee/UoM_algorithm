#!/bin/sh

 python3 sp.py pq
 python3 sp.py bfs
 python3 sp.py bellman-ford
 python3 sp.py bellman-ford-neg
 python3 sp.py dijkstra
 python3 sp.py dijkstra astar

for algo in bfs bellman-ford dijkstra astar; do
   python3 ap.py route $algo MAN MAN
   python3 ap.py route $algo MAN SYD
   python3 ap.py route $algo MAN MUC
   python3 ap.py route $algo MAN ROA

   python3 ap.py route $algo TTA MAN
   python3 ap.py route $algo MAN TTA
done

python3 ap.py count MAN
python3 ap.py count SYD
python3 ap.py count TTA
