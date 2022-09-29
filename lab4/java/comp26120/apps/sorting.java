package comp26120.apps;

import comp26120.PriorityQueue;
import java.util.Scanner;

public abstract class sorting {
    // set to 1 to print debug lines
    // ensure this is 0 when submitting
    public static int DEBUG = 0;

    // Let's do some weirdly complicated ranking of words
    // based on their first five characters. You don't need
    // to understand this but we're mapping all characters to
    // 0-26 and then subdividing the integers into five levels of
    // width 27, so every string with a different first five 
    // characters gets a different code

    public int offset(int n) {
	int res = 27;
	while (n > 0) {
	    int new_int = res*27;
	    // Should not happen as n should be < 6
	    if (new_int < res) {
		System.out.println("OVERFLOW in offset");
		System.exit(-1);
	    }
	    res = new_int;
	    n--;
	}
	return res;
    }

    public int get_bucket(char c) {
	if (c < 65) return 0;
	if (c > 122) return 0;
	if (c > 90) c = (char) (c - 32);
	int b = (c - 64);
	return b;
    }

    public int get_code(String str) {
	int len = str.length() - 1;

	// What would happen if we just returned len as the code?
	// What impact would this have on the operations we perform
	// on our data structures?

	int res = 0;
	int MAX = 5;
	int end = (len > MAX) ? MAX : len;
	for (int i= end - 1; i >= 0; i--) {
	    char c = str.charAt(i);
	    int new_int = res+(offset((MAX-1)-i)*get_bucket(c));
	    // Should not happen as 27^6 < 2^32
	    if (new_int < res) {
		System.out.println("OVERFLOW in get_code");
		System.exit(-1);
	    }
	    res = new_int;
	}
	return res;
    }

    String prog_name="";

    public abstract PriorityQueue initialize_pq(int size);

    public void sorting(String[] argv) {
	int n;

	Scanner scanIn = new Scanner(System.in);
	String nString  = scanIn.nextLine();
	n = Integer.parseInt(nString);

	PriorityQueue pq = initialize_pq(n);

	System.out.println("INSERTING...");
	for (int i = 0; i < n; i++) {
	    // System.out.println(i);
	    String tmp = scanIn.nextLine();
	    int p = get_code(tmp);
	    if (DEBUG == 1) {
		System.out.format("Insert %s with priority %d\n", tmp, p);
	    }
	    pq.insert(tmp, get_code(tmp));
	    if (DEBUG == 1) {
		System.out.println("==============");
		pq.print();
		System.out.println("==============");
	    }
	}
	scanIn.close();
	System.out.println("POPPING...");
	while(!pq.is_empty()) {
	    String tmp = pq.pop_min();
	    System.out.format("%s\n", tmp);
	    if (DEBUG == 1) {
		System.out.println("==============");
		pq.print();
		System.out.println("==============");		
	    }
	}
	
    }
}
