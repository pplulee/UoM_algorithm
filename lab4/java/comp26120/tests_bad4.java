package comp26120;

public class tests_bad4 extends tests {
    String prog_name = "tests_bad4";

    public PriorityQueue initialize_pq(int size) {
	return new bad4();
    }

    public static void main(String args[]) {
	tests T = new tests_bad4();
	T.run_tests(args);
    }
}
