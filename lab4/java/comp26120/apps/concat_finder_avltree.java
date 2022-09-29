package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.avltree;

public class concat_finder_avltree extends concat_finder {
    String prog_name = "concat_finder_avltree";

    public PriorityQueue initialize_pq(int size) {
	return new avltree();
    }

    public static void main(String args[]) {
	concat_finder T = new concat_finder_avltree();
	T.concat_find(args);
    }
}
