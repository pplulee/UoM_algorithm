package comp26120;

public class tests_bad3 extends tests {
    String prog_name = "tests_bad3";

    public PriorityQueue initialize_pq(int size) {
	return new bad3();
    }

    public static void main(String args[]) {
	tests T = new tests_bad3();
	T.run_tests(args);
    }
}
