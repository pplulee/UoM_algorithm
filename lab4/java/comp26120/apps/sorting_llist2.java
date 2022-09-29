package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.llist2;

public class sorting_llist2 extends sorting {
    String prog_name = "sorting_llist2";

    public PriorityQueue initialize_pq(int size) {
	return new llist2();
    }

    public static void main(String args[]) {
	sorting T = new sorting_llist2();
	T.sorting(args);
    }
}
