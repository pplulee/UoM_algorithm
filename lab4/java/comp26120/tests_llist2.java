package comp26120;

public class tests_llist2 extends tests {
    String prog_name = "tests_llist2";

    public PriorityQueue initialize_pq(int size) {
	return new llist2();
    }

    public static void main(String args[]) {
	tests T = new tests_llist2();
	T.run_tests(args);
    }
}
