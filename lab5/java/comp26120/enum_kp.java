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
	    /* ADD CODE IN HERE TO KEEP TRACK OF FRACTION OF ENUMERATION DONE */

	    // calculates the value and weight and feasibility:
	    infeasible=check_evaluate_and_print_sol(solution);  
	    /* ADD CODE IN HERE TO KEEP TRACK OF BEST SOLUTION FOUND*/
	}
	/* ADD CODE TO PRINT OUT BEST SOLUTION */
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
