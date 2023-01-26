package comp26120;

import java.util.ArrayList;

public class enum_kp extends KnapSack {
    public enum_kp(String filename) {
	super(filename);
    }

    
    public static void main(String[] args) {
	enum_kp knapsack = new enum_kp(args[0]);

	knapsack.print_instance();
	knapsack.enumerate();
    }

    public void enumerate() {
	// Do an exhaustive search (aka enumeration) of all possible ways to pack
	// the knapsack.
	// This is achieved by creating every binary solution vector of length Nitems.
	// For each solution vector, its value and weight is calculated.

	int i; // item index
	ArrayList<Boolean> solution = new ArrayList<Boolean>(Nitems + 1); // Solution vector representing items packed
	solution.add(null); // C implementation has null first object
	    
	ArrayList<Boolean> best_solution = new ArrayList<Boolean>(Nitems + 1); // Solution vector for best solution found
	best_solution.add(null);
	
	int best_value; // total value packed in the best solution
	double j = 0;
	int infeasible; // 0 means feasible; -1 means infeasible (violates the capacity constraint)

	// set the knapsack initially empty
	for (i = 1; i <= Nitems; i++) {
	    solution.add(false);
	    best_solution.add(false);
	}

	QUIET=true;
	best_value = 0;

	while (!(next_binary(solution, Nitems))) {
	    j = j+1.0;
	    if (!QUIET)
		System.out.format("done %g of the full enumeration\n", j/Math.pow(2.0,Nitems));
	    infeasible=check_evaluate_and_print_sol(solution);  // calculates the value and weight and feasibility
	    if ((infeasible == 0) && total_value > best_value) {
		best_value = total_value;

		for (i = 1; i <= Nitems; i++) {
		    best_solution.set(i, solution.get(i));
		}
	    }
	    if (!QUIET) {
		System.out.format("best so far has value=%d\n", best_value);
	    }
	}
	QUIET = false;
	System.out.format("Finished.\nPack the following items for optimal\n");
	check_evaluate_and_print_sol(best_solution);
    }

    public boolean next_binary(ArrayList<Boolean> str, int Nitems) {
	// Called with an ArrayList of 0/1 entires with length Nitems
	// (0th item is null for some reason inherited from C implementation - I expect
	// because in C the array is here treated as a pointer to a string).
	// If we treat this array list as a binary number, then this
	// Function adds "1" - e.g., {0,0,0,1} would turn to {0,0,1,0}
	// It returns true when there are no possible binary numbers left 
	int i = Nitems;
	while(i>=1) {
	    if (str.get(i) == true) {
		str.set(i, false);
		i--;
	    } else {
		str.set(i, true);
		break;
	    }
	}
	if (i == 0) {
	    return true;
	} else {
	    return false;
	}
    }
}
