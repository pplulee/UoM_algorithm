package comp26120;

public class tests_bad2 extends tests {
    String prog_name = "tests_bad2";

    public PriorityQueue initialize_pq(int size) {
	return new bad2();
    }

    public static void main(String args[]) {
	tests T = new tests_bad2();
	T.run_tests(args);
    }
}
