package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.llist2;

public class concat_finder_llist2 extends concat_finder {
    String prog_name = "concat_finder_llist2";

    public PriorityQueue initialize_pq(int size) {
	return new llist2();
    }

    public static void main(String args[]) {
	concat_finder T = new concat_finder_llist2();
	T.concat_find(args);
    }
}
