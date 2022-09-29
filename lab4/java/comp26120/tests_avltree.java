package comp26120;

public class tests_avltree extends tests {
    String prog_name = "tests_avltree";

    public PriorityQueue initialize_pq(int size) {
	return new avltree();
    }

    public static void main(String args[]) {
	tests T = new tests_avltree();
	T.run_tests(args);
    }
}
