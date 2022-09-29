package comp26120;

public class tests_llist1 extends tests {
    String prog_name = "tests_llist1";

    public PriorityQueue initialize_pq(int size) {
	return new llist1();
    }

    public static void main(String args[]) {
	tests T = new tests_llist1();
	T.run_tests(args);
    }
}
