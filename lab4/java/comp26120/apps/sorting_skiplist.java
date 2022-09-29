package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.skiplist;

public class sorting_skiplist extends sorting {
    String prog_name = "sorting_skiplist";

    public PriorityQueue initialize_pq(int size) {
	return new skiplist();
    }

    public static void main(String args[]) {
	sorting T = new sorting_skiplist();
	T.sorting(args);
    }
}
