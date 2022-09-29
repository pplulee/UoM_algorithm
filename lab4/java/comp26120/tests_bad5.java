package comp26120;

public class tests_bad5 extends tests {
    String prog_name = "tests_bad5";

    public PriorityQueue initialize_pq(int size) {
	return new bad5();
    }

    public static void main(String args[]) {
	tests T = new tests_bad5();
	T.run_tests(args);
    }
}
