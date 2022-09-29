package comp26120;

public class binaryHeap implements PriorityQueue {
    int num_elem; // Number of elements
    int heap_size; // Current size of heap
    int[] weights; // The heap
    String[] elements; // The heap

    // 0-based operaations
    // This could be updated to be 1-based if you wanted, what else would need to change?
    public static int FIRST=0;

    int parent(int i) {	return (i - 1)/2;    }
    int left(int i) { return (2*i) + 1; }
    int right(int i) { return (2*i) + 2; }

    public binaryHeap(int size) {
	this.num_elem = size;
	this.heap_size = 0;
	weights = new int[size];
	elements = new String[size];
    }

    // Helper function for swapping nodes in the tree
    public void swap(int i, int j) {
	String t = elements[i];
	elements[i] = elements[j];
	elements[j] = t;

	int w = weights[i];
	weights[i] = weights[j];
	weights[j] = w;
    }

    public void sift_up(int i) {
	// TODO implement sift-up (also known as bubble-up and other things)
    }

    public void sift_down(int i) {
	while (true) {
	    int l = left(i);
	    int r = right(i);
	    if (l >= heap_size && r >= heap_size) {
		// no children, we're finished
		return;
	    }
	    int smallest = l;
	    if (r < heap_size && weights[r] < weights[l]) {
		smallest = r;
	    }

	    if (weights[smallest] < weights[i]) {
		swap(i, smallest);
	    } else {
		// children not smaller, we're finished
		return;
	    }

	    i = smallest;
	}
    }

    public boolean contains(String u, int priority) {
	// Linear Search required as unordered
	for (int i = FIRST; i < heap_size; i++) {
	    if (elements[i].equals(u) && weights[i] == priority) {
		return true;
	    }
	}
	return false;
    }

    public void expand() {
	num_elem = num_elem*2;

	int[] new_weights = new int[num_elem];
	String[] new_elements = new String[num_elem];

	System.arraycopy(weights, 0, new_weights, 0, weights.length);
	System.arraycopy(elements, 0, new_elements, 0, elements.length);

	weights = new_weights;
	elements = new_elements;
    }

    int last_idx() {
	// TODO the last is only 0 at the very start
	//      fixt this to set last to the last index of pq
	int last = 0;
	// if we ever query outside the heap just expand it
	if (last >= num_elem) {
	    expand();
	}
	return last;
    }

    public void insert(String u, int w) {
	int li = last_idx();
	weights[li] = w;
	elements[li] = u;

	// TODO there is something missing here, put it back

	heap_size++;
    }

    public boolean is_empty() {
	return heap_size == 0;
    }

    public String pop_min() {
	if (is_empty()) {
		System.err.println("Error: pop_min from empty binaryHeap");
		System.exit(-1);
	}
	heap_size = heap_size - 1;
	int li = last_idx();
	swap (FIRST, li);
	String res = elements[li];
	sift_down(FIRST);
	return res;
    }

    public void print() {
	System.out.format("BinaryHeap has %d elements with %d size\n",num_elem,heap_size);
	for (int i = FIRST; i < heap_size; i++) {
	    System.out.format("(%s,%d)\n",elements[i], weights[i]);
	}
    }
}
