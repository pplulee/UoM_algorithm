package comp26120;

public class tests_binaryheap extends tests {
    String prog_name = "tests_binaryheap";

    public PriorityQueue initialize_pq(int size) {
	return new binaryHeap(size);
    }

    public static void main(String args[]) {
	tests T = new tests_binaryheap();
	T.run_tests(args);
    }
}
