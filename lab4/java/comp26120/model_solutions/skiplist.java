package comp26120;

import java.util.Random;

// Note that the skiplist is implemented as a linked list of 'nodes'
// where a node represents a tower in the abstract view
public class skiplist implements PriorityQueue {
    // This will have a large impact on performance, try playing with it
    public static int MAX_LEVEL = 20;

    int levels;
    int size;
    node header;

    public class node {
	int priority;
	String value;
	// Array of `forward' pointers
	node[] next;
	int height;

	public node(String value, int priority, int levels) {
	    this.priority = priority;
	    this.value = value;
	    this.next = new node[levels];
	    this.height = levels;
	}
    }


    public skiplist() {
	this.levels = 1;
	this.size = 0;
	// We will actually use the same sentinel node for start and end
	this.header = new node(null,Integer.MAX_VALUE,MAX_LEVEL);
	for (int i =  0; i < MAX_LEVEL; i++) {
	    header.next[i] = header;
	}
    }

    public boolean is_empty() {
	return this.size <= 0;
    }

    // Returns the last node with priority less than 'priority'
    // The above line used to say 'or equal' but it was pointed out that returning
    // the last node in the case of duplicates makes the contains function fail
    //
    // Records in 'updates' the nodes along the path that would need updating if a node to
    // their right on their level were to be inserted e.g. the nodes at which the decision
    // to go 'down' is made

    public node search(int priority, node[] updates) {
	node candidate_node = this.header;
	int level = MAX_LEVEL;
	while (level > 0) {
	    level --;

	    while (candidate_node.next[level].priority < priority) {
		candidate_node = candidate_node.next[level];
	    }

	    // Record the node where we go down at a particular level
	    if (updates != null) {
		updates[level] = candidate_node;
	    }
	}
	return candidate_node;
    }

    public void insert(String value, int priority) {
	node[] updates = new node[MAX_LEVEL];
	node insert_at = search(priority,updates);

	int levels = 1;
	Random random = new Random();
	while (levels < MAX_LEVEL && random.nextBoolean()) {
	    levels++;
	}

	node new_node = new node(value, priority, levels);

	for (int i = 0; i < levels; i++) {
	    new_node.next[i] = updates[i].next[i];
	    updates[i].next[i] = new_node;
	}

	size++;
    }

    public boolean contains (String value, int priority) {
	node tmp_node = search(priority, null);
	node new_node = tmp_node.next[0];

	while (new_node.priority == priority && new_node.value != null && !new_node.value.equals(value)) {
		new_node = new_node.next[0];
	}
	return (new_node.priority == priority && new_node.value != null && new_node.value.equals(value));
    }

    public String pop_min() {
	node min = header.next[0];
	String res = min.value;

	for (int i = 0; i < min.height; i++) {
	    header.next[i] = min.next[i];
	}

	size--;
	return res;
    }

    // There are probably nicer ways to print a skiplist
    public void print() {
	node new_node = header;
	do {
	    System.out.format("(%s,%d,%d)\n",new_node.value, new_node.priority, new_node.height);
	    new_node = new_node.next[0];
	}
	while (new_node != header);
    }



}
