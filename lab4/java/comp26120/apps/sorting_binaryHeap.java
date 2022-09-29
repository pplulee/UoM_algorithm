package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.binaryHeap;

public class sorting_binaryHeap extends sorting {
    String prog_name = "sorting_binaryHeap";

    public PriorityQueue initialize_pq(int size) {
	return new binaryHeap(size);
    }

    public static void main(String args[]) {
	sorting T = new sorting_binaryHeap();
	T.sorting(args);
    }
}
