package comp26120;

public class tests_bad1 extends tests {
    String prog_name = "tests_bad1";

    public PriorityQueue initialize_pq(int size) {
	return new bad1();
    }

    public static void main(String args[]) {
	tests T = new tests_bad1();
	T.run_tests(args);
    }
}
