package comp26120.apps;

import comp26120.PriorityQueue;
import java.util.Scanner;

public abstract class concat_finder {
    public int MAX_STR_LEN=100;

    public static void tidy_up(PriorityQueue pq) {
	while (!pq.is_empty()) {
	    String s = pq.pop_min();
	}
    }

    String prog_name = "";

    public abstract PriorityQueue initialize_pq(int size);

    public void concat_find(String[] args) {

	PriorityQueue pq = initialize_pq(1000);

	Scanner scanIn = new Scanner(System.in);
	String search = scanIn.nextLine();
	System.out.format("Searching for %s\n",search);

	int n;
	String nString = scanIn.nextLine();
	n = Integer.parseInt(nString);

	for (int i=0; i<n; i++) {
	    String tmp = scanIn.nextLine();
	    if (tmp.equals(search)) {
		System.out.println("Found");
		tidy_up(pq);
		return;
	    }

	    if (tmp.length() < search.length()) {
		// pq owns memory
		pq.insert(tmp, tmp.length());
	    }
	}
	scanIn.close();

	PriorityQueue done = initialize_pq(1000);

	while (!pq.is_empty()) {
	    String next = pq.pop_min();
	    System.out.format("Pop %s\n", next);
	    PriorityQueue rebuild = initialize_pq(1000);
	    while (!done.is_empty()) {
		String s = done.pop_min();
		rebuild.insert(s, s.length());
		// System.out.format("Try with %s\n",s);
		if (s.length() + next.length() <= search.length()) {
		    String left = next.concat(s);
		    String right = s.concat(next);

		    if (left.equals(search) || right.equals(search)) {
			System.out.println("Found");
			tidy_up(pq);
			tidy_up(done);
			tidy_up(rebuild);
			return;
		    }
		    // pq owns memory
		    pq.insert(left, left.length());
		    pq.insert(right, right.length());
		}
	    }
	    // Can remove conditional if PriorityQueue does not contain duplicates
	    // System.out.format("Done with %s\n", next);
	    if (!rebuild.contains(next, next.length())) {
		// System.out.format("Using %s\n", next);
		rebuild.insert(next, next.length());
	    }
	    done = rebuild;
	}
	tidy_up(pq);
	tidy_up(done);
	System.out.println("Not Found");
	return;
    }
}
