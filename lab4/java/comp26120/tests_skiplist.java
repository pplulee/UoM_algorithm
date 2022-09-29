package comp26120;

public class tests_skiplist extends tests {
    String prog_name = "tests_skiplist";

    public PriorityQueue initialize_pq(int size) {
	return new skiplist();
    }

    public static void main(String args[]) {
	tests T = new tests_skiplist();
	T.run_tests(args);
    }
}
