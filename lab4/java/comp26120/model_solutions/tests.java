package comp26120;

import comp26120.PriorityQueue;

public abstract class tests {

    public void check_result(int testno, String expected, String found) {
	if (found == null) {
	    System.err.format("Test %d Failed when %s expected and NULL found\n",testno,expected);
	    System.exit(-1);
	}

	if (! expected.equals(found)) {
	    System.err.format("Test %d Failed when %s expected and %s found\n",testno,expected,found);
	    System.exit(-1);
	}
    }

    public void assert_test(int testno, boolean value, String reason) {
	if (!value) {
	    System.err.format("Test %d Failed as %s\n",testno,reason);
	    System.exit(-1);
	}
    }

    public abstract PriorityQueue initialize_pq(int size);


    public void run_test0() {
	System.out.println("TEST 0");
	PriorityQueue queue = initialize_pq(10);
	System.out.println("Initialised...");
	queue.insert("hello",1);
	System.out.println("Inserted hello with priority 1...");
	queue.insert("goodbye",2);
	System.out.println("Inserted goodbye with priority 2...");
	check_result(0,"hello",queue.pop_min());
	System.out.println("Popped hello...");
	check_result(0,"goodbye",queue.pop_min());
	System.out.println("Popped goodbye...");
	assert_test(0,queue.is_empty()," queue is meant to be empty");
	System.out.println("Queue now empty");
    }

    public void run_test1() {
	System.out.println("TEST 1");
	PriorityQueue queue = initialize_pq(10);
	System.out.println("Initialised...");
	queue.insert("hello",1);
	System.out.println("Inserted hello with priority 1...");
	queue.insert("goodbye",2);
	System.out.println("Inserted goodbye with priority 2...");
	queue.print();
    }

    public void run_test2() {
	System.out.println("TEST 2");
	PriorityQueue queue = initialize_pq(10);
	System.out.println("Initialised...");
	queue.insert("hello",2);
	System.out.println("Inserted hello with priority 2...");
	queue.insert("goodbye",1);
	System.out.println("Inserted goodbye with priority 1...");
	check_result(0,"goodbye",queue.pop_min());
	System.out.println("Popped goodbye...");
	check_result(0,"hello",queue.pop_min());
	System.out.println("Popped hello...");
	assert_test(0,queue.is_empty()," queue is meant to be empty");
	System.out.println("Queue now empty");
	queue.print();
    }

    public void run_test3() {
	System.out.println("TEST 3");
	PriorityQueue queue = initialize_pq(5);
	queue.insert("first", 1);
	queue.insert("second", 2);
	queue.insert("fourth", 4);
	queue.insert("third", 3);
	queue.insert("hundred", 100);
	queue.insert("fifty", 50);
	queue.insert("ten", 10);
	check_result(3, "first", queue.pop_min());
	System.out.println("Popped first...");
 	check_result(3, "second", queue.pop_min());
	System.out.println("Popped second...");
	check_result(3, "third", queue.pop_min());
	System.out.println("Popped third...");
	check_result(3, "fourth", queue.pop_min());
	System.out.println("Popped fourth...");
	check_result(3, "ten", queue.pop_min());
	System.out.println("Popped ten...");
	check_result(3, "fifty", queue.pop_min());
	System.out.println("Popped fifty...");
 	check_result(3, "hundred", queue.pop_min());
	System.out.println("Popped hundred...");
  }


    String prog_name = "0";

    public int run_tests(String[] args) {
	if (args.length != 1) {
	    System.err.println("Supply test number");
	    return -1;
	}

	try {
	    int test_number = Integer.parseInt(args[0]);
	    switch (test_number) {
	    case 0: run_test0();
		    break;
	    case 1: run_test1(); break;
	    case 2: run_test2(); break;
	    case 3: run_test3(); break;
	    default:
		System.err.format("Test number %d not recognised\n",test_number);
		break;
	    }
	    return 0;
	} catch (NumberFormatException e) {
	    System.err.println("Supply test number as an integer");
	    return -1;
	}
    }
}
