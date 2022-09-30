package comp26120;

import java.util.ArrayList;

public class bnb_kp extends KnapSack {
    double DOUB_MAX=10e30; // a large number, must be greater  than the max value of any solution
    static int SIZE=100000; // an estimate of how large the priority queue could become
    int NITEMS=2000; // an upper limit of the number of items

    int QueueSize=0; // the number of items currently stored in the priority queue

    public class struc_sol {
	ArrayList<Boolean> solution_vec = new ArrayList<Boolean>(NITEMS+1); // "binary" solution vector
	// e.g. solution_vec[1]=true means first item is packed in knapsack
	//      solution_vec[1]=false means first item is NOT in knapsack
	// NB: solution_vec[0] is meaningless (null)

	int val; // its value
	int fixed; // the number of items that are fixed to either 0 or 1, not '*' (null)
	double bound; // the upper bound value of the solution

	public struc_sol() {
	    for (int i = 0; i<=NITEMS; i++) {
		solution_vec.add(null);
	    }
	}

	// copy a solution -- needed for generating child solutions from parent solutions.
	public struc_sol copy() {
	    struc_sol copy = new struc_sol();
	    for (int i = 0; i<=NITEMS; i++) {
		copy.solution_vec.set(i, this.solution_vec.get(i));
	    }
	    copy.val = this.val;
	    copy.fixed = this.fixed;
	    copy.bound = this.bound;
	    return copy;
	}


    }

    struc_sol[] pqueue; // The knapsack solutions.  To be stored in a priority queue

    // The following four functions implement a priority queue.
    // They are based on the functions given in Robert Sedgwick's book, Algorithms in C.
    public void upheap(int qsize) {
	// unheap reorders the elements in the heap (queue) after an insertion
	struc_sol temp_element;
	temp_element = pqueue[qsize];
	pqueue[0].bound = DOUB_MAX;

	while (pqueue[qsize/2].bound<=temp_element.bound) {
	    pqueue[qsize]=pqueue[qsize/2];
	    qsize=qsize/2;
	}

	pqueue[qsize]=temp_element;
    }

    public void insert(struc_sol element) {
	assert(QueueSize<SIZE-1);
	pqueue[++QueueSize]=element;
	upheap(QueueSize);
    }

    public void downheap(int qindex) {
	// down heap reorders the elements in the heap (queue) after a removal

	int j;
	struc_sol temp_element;
	temp_element = pqueue[qindex];
	while (qindex <= QueueSize/2) {
	    j = qindex+qindex;
	    if (j<QueueSize && pqueue[j].bound<pqueue[j+1].bound) {
		j++;
	    }
	    if (temp_element.bound>=pqueue[j].bound) {
		break;
	    }
	    pqueue[qindex]=pqueue[j];
	    qindex=j;
	}
	pqueue[qindex]=temp_element;
    }

    public struc_sol removeMax() {
	struc_sol head = pqueue[1];
	pqueue[1] = pqueue[QueueSize--];
	downheap(1);
	return head;
    }
    // End priority queue methods.

    // Extra function needed because of my previous decision to use an array of booleans for solutions
    // not an array of ints.  Mostly to allow consistency in printing with the C solution.
    private static int bool_to_int(Boolean b) {
	if (b) {
	    return 1;
	}
	return 0;
    }

    public void print_sol(struc_sol sol) {
	// prints a solution in the form 000100xxxx etc
	// with x's denoting the part of the solution not yet fixed (determined)

	int i;
	System.out.format("%d %.2f ", sol.val, sol.bound);
	for (i = 1; i<=sol.fixed; i++) {
	    System.out.format("%d", bool_to_int(sol.solution_vec.get(i)));
	}
	while(i<=Nitems) {
	    System.out.format("x");
	    i++;
	}
	System.out.format("\n");
    }

    public void frac_bound(struc_sol sol, int fix) {
	  // Updates the values sol->val and sol->bound                                 

	// Computes the fractional knapsack upper bound                               
	// given a "binary" vector of items (sol.solution_vec),                        
	// where the first                                                            
	// "fix" of them are fixed. All that must be done                             
	// is compute the value of the fixed part; then                               
	// add to that the value obtained by adding in                                
	// items beyond the fixed part until the capacity                             
	// is exceeded. For the exceeded capacity, the fraction                       
	// of the last item added which would just fill the knapsack                  
	// is taken. This fraction of profit/value is added to the                    
	// total. This is the required upper bound.                                   

	// Everything above assumes items are sorted in decreasing                    
	// profit/weight ratio                                                        

	int i; // index of current item
	double totalp=0; // profit total                                              
	int totalw=0; // weight total                                                 
	sol.val=-1;

	// compute the current value and weight of the fixed part
	for (i = 1; i<= fix; i++) {
	    if (sol.solution_vec.get(i) == true) {
		totalw += item_weights.get(temp_indexes.get(i));
		totalp += item_values.get(temp_indexes.get(i));
	    }
	}

	if (totalw > Capacity) { // if fixed part infeasible, return
	    return;
	}

	sol.val=(int) totalp;
	// System.out.format("%.2f %d\n", totalp, totalw);

	// add in the rest of the items until capacity is exceeded
	i = fix+1;
	if (i <= Nitems) {
	    do {
		// ADD CODE HERE to update totalw and totalp
		i++;
	    } while ((i<=Nitems) && (totalw<Capacity));
	}

	/* if over-run the capacity, adjust profit total by substracting
	   that overrun fraction of the last item */
	if (totalw > Capacity) {
	    --i;
	    totalp -= ((double) (totalw-Capacity)/(double) (item_weights.get(temp_indexes.get(i))))*item_values.get(temp_indexes.get(i));
	}
	sol.bound=totalp;

    }

    public bnb_kp(String filename) {
        super(filename);
    }


    public static void main(String[] args) {
	ArrayList<Boolean> final_sol = new ArrayList<Boolean>(); // "binary" solution vector indicating items to pack
	int total_value, total_weight; // total value and total weight of items packed

	bnb_kp knapsack = new bnb_kp(args[0]);
	assert(knapsack.NITEMS>=knapsack.Nitems);

	knapsack.sort_by_ratio();

	knapsack.pqueue = new struc_sol[SIZE+1];

	knapsack.branch_and_bound(final_sol);
	System.out.println("Branch and Bound Solution of Knapsack is:\n");
	knapsack.check_evaluate_and_print_sol(final_sol);
    }

    public void branch_and_bound(ArrayList<Boolean> final_sol) {
	pqueue[0] = new struc_sol(); // set a blank first element
	for (int i = 0; i<=Nitems; i++) { // Initialise final solution
	    final_sol.add(null);
	}

	// branch and bound

	// start with the empty solution vector
	// compute its value and its bound
	// put current_best = to its value
	// store it in the priority queue
  
	// LOOP until queue is empty or upper bound is not greater than current_best:
	//   remove the first item in the queue
	//   construct two children, 1 with a true added, 1 with a false added
	//   FOREACH CHILD:
	//     if infeasible, discard child
	//     else
	//       compute the value and bound
	//       if value > current_best, set current_best to it, and copy child to final_sol
	//       add child to the queue
	// RETURN
  

	/* YOUR CODE GOES HERE */

    }

     public void copy_array(ArrayList<Boolean> from, ArrayList<Boolean> to) {
	// This copies Nitems elements of one boolean array intto another
	int i;
	for (i=0;i<=Nitems;i++) {
	    if (from.get(i) == null) {
		to.set(i, null);
	    } else if (from.get(i)) {
		to.set(i, true);
	    } else {
		to.set(i, false);
	    }
	}
    }
}
