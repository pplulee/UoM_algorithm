package comp26120.apps;

import comp26120.PriorityQueue;
import comp26120.binaryHeap;

public class concat_finder_binaryHeap extends concat_finder {
    String prog_name = "concat_finder_binaryHeap";

    public PriorityQueue initialize_pq(int size) {
	return new binaryHeap(size);
    }

    public static void main(String args[]) {
	concat_finder T = new concat_finder_binaryHeap();
	T.concat_find(args);
    }
}
