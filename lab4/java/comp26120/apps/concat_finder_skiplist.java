package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.skiplist;

public class concat_finder_skiplist extends concat_finder {
    String prog_name = "concat_finder_skiplist";

    public PriorityQueue initialize_pq(int size) {
	return new skiplist();
    }

    public static void main(String args[]) {
	concat_finder T = new concat_finder_skiplist();
	T.concat_find(args);
    }
}
