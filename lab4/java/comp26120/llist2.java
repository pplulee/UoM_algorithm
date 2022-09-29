package comp26120;

public class llist2 implements PriorityQueue {
    String value = null;
    int priority;
    llist2 next = null;
    llist2 prev = null;
    
    public llist2() {
        // Use a dummy node for the head of the list;
        priority = 0;
    }

    public llist2(String value, int priority) {
        // A node to be inserted into a list
        this.value = value;
        this.priority = priority;
    }

    public boolean contains(String value, int priority) {
	// Linear search
	// Skip dummy
        llist2 tmp_next = next;
        while (tmp_next != null) {
            if (tmp_next.value.equals(value) && tmp_next.priority == priority) {
                return true;
            }
            tmp_next  = tmp_next.next;
        }

        return false;
    }

    public void insert(String value,  int priority) {
	llist2 node = new llist2(value, priority);

	llist2 here = this;
	while (here.next != null && here.next.priority < priority) {
	    here = here.next;
	}
	// insert after here
	node.next = here.next;
	if (here.next != null) {
	    here.next.prev = node;
	}

	here.next=node;
	node.prev=here;
	
    }

    // This is why we use the dummy - we can then just moves the nodes in the list around without
    // needing to change the value of the first node after we remove the minimum element
    public String pop_min() {
	if (this.next != null) {
	    // The best will always be the first
	    llist2 node = this.next;
	    String value = node.value;

	    // Remove
	    this.next = node.next;
	    if (node.next != null) {
		node.next.prev = node.prev;
	    }

	    return value;
	}
	return null;
    }

    public boolean is_empty() {
        // Assumes single dummy
        return (this.next == null);
    }


    public void print() {
        System.out.format("<%s,%d> followed by...\n",value,priority);
        if (this.next != null) {
            next.print();
        } else {
            System.out.println("End of List");
        }
    }


}
