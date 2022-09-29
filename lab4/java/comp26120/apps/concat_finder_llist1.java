package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.llist1;

public class concat_finder_llist1 extends concat_finder {
    String prog_name = "concat_finder_llist1";

    public PriorityQueue initialize_pq(int size) {
	return new llist1();
    }

    public static void main(String args[]) {
	concat_finder T = new concat_finder_llist1();
	T.concat_find(args);
    }
}
