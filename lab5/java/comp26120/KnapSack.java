package comp26120;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Collections;
import java.util.Comparator;

/*
 *
 * set of functions that are used by two of more of the knapsack solution
 * methods: enum, branch-and-bound, dynamic programming and greedy
 *
 */

public class KnapSack {
    int Nitems;
    ArrayList<Integer> item_weights;
    ArrayList<Integer> item_values;
    ArrayList<Integer> temp_indexes;
    int Capacity;
    boolean QUIET = false;

    int total_weight; // This is used for checking solutions
    int total_value; // This is  used for checking solutions

    public KnapSack() {
    }

    public KnapSack(String filename) {
	// Note: knapsack items in the input files are numbered from 1 to N. 
	// We shall use array Lists to store the indexes, weights and values
	// of the items. So w.get(1) and v.get(1) store the weight and value of the first item.

	int i;
	File f = new File(filename);
	try {
	    Scanner scanIn = new Scanner(f);
	    Nitems = scanIn.nextInt(); // read the number of items

	    item_weights = new ArrayList<Integer>(Nitems+1);
	    item_values = new ArrayList<Integer>(Nitems+1);
	    temp_indexes = new ArrayList<Integer>(Nitems+1);

	    // 0th element of the arrays is null since input files start at 1 (not convinced by this particulard design decision)
	    temp_indexes.add(null);
	    item_weights.add(null);
	    item_values.add(null);

	    for (i = 1; i <= Nitems; i++) {
		temp_indexes.add(scanIn.nextInt());
		item_values.add(scanIn.nextInt());
		item_weights.add(scanIn.nextInt());
	    }

	    Capacity = scanIn.nextInt(); // read the knapsack capacity
	} catch (Exception e) {
	    System.err.println("Problem reading file from file and/or allocating arrays");
	    System.exit(1);
	}

    }
    
    public void print_instance() {
	int i;
	System.out.println("item\tW\tV");
	for (i = 1; i <= Nitems; i++) {
	    System.out.format("%d\t%d\t%d\n", temp_indexes.get(i), item_weights.get(i), item_values.get(i));
	}
	System.out.format("%d\n", Capacity);
    }

    public void sort_by_ratio() {
	int i;
	// sort the item indexes
	Collections.sort(temp_indexes, new mycomp());

	// print out the sorted order as a check
	for (i = 1; i<=Nitems;i++) {
	    System.out.format("%d\t%d\t", item_weights.get(temp_indexes.get(i)), item_values.get(temp_indexes.get(i)));
	    System.out.format("%f\n", (double) item_values.get(temp_indexes.get(i))/(double) item_weights.get(temp_indexes.get(i)));
	}
    }

    class mycomp implements Comparator<Integer> {
	@Override
	public int compare(Integer a, Integer b) {
	    if (b == null) { // Needed because of this weird business where the start of the array is null
		return 1;
	    }
	    if ((double)item_values.get(a)/(double)item_weights.get(a) > (double)item_values.get(b)/(double)item_weights.get(b)) {
		return -1;
	    } else {
		if ((double)item_values.get(a)/(double)item_weights.get(a) < (double)item_values.get(b)/(double)item_weights.get(b)) {
		return 1;
		} else {
		    return 0;
		}
	    }
	}
    }

    public int check_evaluate_and_print_sol(ArrayList<Boolean> sol) {

	// This function prints out the items packed in a solution, in ascending order.
	// Since items may have been sorted in a different order (using temp_indexes), it first reverses this mapping


	// The vector sol is a binary vector of length Nitems, describing the items to be put in the knapsack.
	// The field temp_indexes array maps item i to temp_indexes.get(i).
	// So sol.get(i)=1 really means item temp_indexes.get(i) should be taken.
	// In order to print out the item numbers referred to by sol in ascending order, we
	// copy them accross to an auxiliary array "pack" and then print the
	// items in pack in ascending order. 
 

	int i; // index variable
	total_value = 0; // total value packed
	total_weight = 0; // total weight packed
	ArrayList<Integer> pack = new ArrayList<Integer>(Nitems); // auxiliary array to do reverse-mapping
	for (i = 0; i<=Nitems; i++) {
	    pack.add(null); // Fill array with null objects
	}

	// First pass: unmap the mapping using pack
	for (i = 1; i <= Nitems; i++) {
	    if (sol.get(i) != null && sol.get(i) == true) {
		pack.set(temp_indexes.get(i), 1);
	    } else {
		pack.set(temp_indexes.get(i), 0);
	    }
	}

	if (!QUIET) {
	    System.out.format("Pack items: ");
	}

	for (i = 1; i <= Nitems; i++) {
	    if (pack.get(i) == 1) {
		if (!QUIET) {
		    System.out.format("%d ", i);
		}
		total_value += item_values.get(i);
		total_weight += item_weights.get(i);
	    }
	}

	// Finally, print out the value, weight and Capacity, and feasibility
	if (!QUIET) {
	    if (total_weight > Capacity) {
		System.out.format("\nvalue=%d weight=%d > Capacity=%d: Infeasible\n",total_value,total_weight,Capacity);
	    } else {
		System.out.format("\nvalue=%d weight=%d <= Capacity=%d: Feasible\n",total_value,total_weight,Capacity);
	    }
	}

	if (total_weight > Capacity) {
	    return -1; // return -1 for infeasible solutions
	} else {
	    return 0; // return - for feasible solutions
	}

    }
}
