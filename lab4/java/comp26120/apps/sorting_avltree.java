package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.avltree;

public class sorting_avltree extends sorting {
    String prog_name = "sorting_avltree";

    public PriorityQueue initialize_pq(int size) {
	return new avltree();
    }

    public static void main(String args[]) {
	sorting T = new sorting_avltree();
	T.sorting(args);
    }
}
