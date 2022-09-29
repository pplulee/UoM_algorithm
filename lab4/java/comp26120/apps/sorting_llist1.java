package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.llist1;

public class sorting_llist1 extends sorting {
    String prog_name = "sorting_llist1";

    public PriorityQueue initialize_pq(int size) {
	return new llist1();
    }

    public static void main(String args[]) {
	sorting T = new sorting_llist1();
	T.sorting(args);
    }
}
