package comp26120;

public class avltree implements PriorityQueue {
    // Set CHECK_HB here to check whether
    // the Height-Balance property holds. This slows things down a lot.
    static boolean CHECK_HB = false;

    int priority;
    String value;
    avltree left;
    avltree right;
    int depth;

    // Helper function for max
    public static int max(int a, int b) {
	if (a > b) return a;
	return b;
    }

    // Functions for checking HeightBalance property
    public int actualHeight() {
	if (left != null && right != null) {
	    return 1 + max(this.left.actualHeight(), this.right.actualHeight());
	} else {
	    return 0;
	}
    }

    public boolean hasHeightBalanceProperty() {
	if (this.left != null && this.value == null) {
	    return this.left.hasHeightBalanceProperty();
	}

	if (this.left != null && this.right != null) {
	    int left_height = this.left.actualHeight();
	    int right_height = this.right.actualHeight();
	    int difference = left_height - right_height;
	    if (difference < 0) {
		difference = -difference;
	    }

	    return (difference <= 1) && this.left.hasHeightBalanceProperty() && this.right.hasHeightBalanceProperty();
	}

	return true;
    }

    public void checkHeightBalanceProperty() {
	if (CHECK_HB) {
	    if (!hasHeightBalanceProperty())  {
		System.err.println("HeightBalanceProperty violated");
		System.exit(-1);
	    }
	}
    }

    public avltree() {
	this.depth=1;
    }

    public avltree(int priority, String value, avltree left, avltree right, int depth) {
	this.priority = priority;
	this.value = value;
	this.left = left;
	this.right = right;
	this.depth = depth;
    }

    //Used for checkign whether a tree is the sentinel, top tree
    public boolean sentinel() {
	return this.value == null;
    }

    public boolean is_empty() {
	if (sentinel()) {
	    return this.left == null;
	}

	return this.left==null && this.right == null;
    }

    //Helper functions for insertion
    public static int height(avltree tree) {
	if (tree != null) {
	    return tree.depth;
	}

	return 0;
    }

    public avltree copy() {
	if (left != null & right != null) {
	    return new avltree(priority, value, left.copy(), right.copy(), depth);
	} else if (left != null) {
	    return new avltree(priority, value, left.copy(), right, depth);
	} else if (right != null) {
	    return new avltree(priority, value, left, right.copy(), depth);
	} else {
	    return new avltree(priority, value, left, right, depth);
	}
	
    }

    public avltree shallow_copy() {
	return new avltree(priority, value, left, right, depth);
    }

    public void rightRotate() {
	avltree l = this.left;
	if (l.right != null) {
	    this.left = l.right;
	} else {
	    this.left = null;
	}
	l.right = this.shallow_copy();

	this.depth = max(height(this.left), height(this.right)) + 1;
	l.depth = max(height(l.left), this.depth) + 1;

	this.value = l.value;
	this.priority = l.priority;
	this.left = l.left;
	this.right = l.right;
	this.depth = l.depth;
    }

    public void leftRotate() {
	avltree r = this.right;
	if (r.left != null) {
	    this.right = r.left;
	} else {
	    this.right = null;
	}
	r.left = this.shallow_copy();

	this.depth = max(height(this.left), height(this.right)) + 1;
	r.depth = max(height(r.left), this.depth) + 1;

	this.value = r.value;
	this.priority = r.priority;
	this.left = r.left;
	this.right = r.right;
	this.depth = r.depth;
    }

    public int getBalance() {
	if (this.left == null && this.right == null) {
	    return 0;
	}
	int balance = height(this.right) - height(this.left);
	return balance;
    }

    public void rebalance() {
	int parentBalance = getBalance();

	if (parentBalance == -2) { // left child updated
	    if (this.left.getBalance() <= 0) {
		// System.out.println("Case Right");
		rightRotate();
	    } else {
		// System.out.println("Case RightLeft");
		this.left.leftRotate();
		rightRotate();
	    }
	} else if (parentBalance == 2) { // right child update
	    if (this.right.getBalance() >= 0) {
		// System.out.println("Case Left");
		leftRotate();
	    } else {
		// System.out.println("Case LeftRight");
		this.right.rightRotate();
		leftRotate();
	    }
	}

	// System.out.println("No change");
    }

    public avltree insert_inner(avltree tree, String value, int priority) {
	if (tree != null) {
	    if (tree.priority > priority) {
		tree.left = insert_inner(tree.left, value, priority);
	    } else {
		tree.right = insert_inner(tree.right, value, priority);
	    }
	    // This implementation allows duplicates

	    tree.depth = max(height(tree.left), height(tree.right)) + 1;

	    tree.rebalance();
	} else {
	    tree = new avltree();
	    tree.value = value;
	    tree.priority = priority;
	}
	return tree;
    }

    public void insert(String value, int priority) {
	if (value == null) {
	    System.err.println("Cannot insert NULL into tree, ignoring...");
	    return;
	}

	if (sentinel()) {
	    // sentinel case
	    this.left = insert_inner(this.left, value, priority);
	    checkHeightBalanceProperty();
	    return;
	}

	System.err.println("Tree is corrupted");
	System.exit(-1);
	return;
    }

    public boolean contains(String value, int priority) {
	if (sentinel() && this.left != null) {
	    return this.left.contains(value, priority);
	} else {
	    if (this.priority == priority) {
		// if we have the right priority and the right value return true;
		if (value.equals(this.value)) {
		    return true;
		}
		// if we have the right priority but the wrong value then one of the children might have the same priority and, if so, we should search there.  We cannot make assumpations about which child.
		return (this.left != null && this.left.priority == priority && this.left.contains(value, priority)) || (this.right != null && this.right.priority==priority && this.right.contains(value, priority));
	    }
	    // tree sorted by priority
	    if (priority < this.priority && this.left != null) {
		return this.left.contains(value, priority);
	    } else if (this.right != null) {
		return this.right.contains(value,priority);
	    }
	}
	// if relevant subtrees are null then they contain no values;
	return false;
    }

    /*
     * Observe that the minimum node cannot have a left sub-child
     * Therefore, deleting it is comparatively straightforward e.g.
     * we do not need to choose which subtree to lift
     */
    public static String pop_min_inner(avltree tree, avltree parent){
	if (tree != null) {
	    String res = null;
	    // Not min yet
	    if (tree.left != null) {
		res = pop_min_inner(tree.left,tree);
		tree.depth = max(height(tree.left), height(tree.right)) + 1;
		tree.rebalance();
		parent.left = tree;
	    }
	    // Min node (base case for recursion)
	    else {
		res = tree.value;
		if (tree.right != null) {
		    parent.left = tree.right;
		} else {
		    parent.left = null;
		}
	    }
	    return res;
	}
	System.err.println("Tree to pop from empty AVL tree");
	System.exit(-1);
	return null;
    }

    public String pop_min() {
	if (sentinel()) {
	    String res = pop_min_inner(this.left, this);
	    checkHeightBalanceProperty();
	    return res;
	}
	System.err.println("The tree is corrupted");
	System.exit(-1);
	return null;
    }

    // You can update this if you want
    public void print_recursive(int depth) {
	for (int i = 0;i< depth; i++) {
	    System.out.print(" ");
	}
	System.out.format("(%s,%d,%d)\n",this.value,this.priority,this.depth);
	if (this.left != null) {
	    this.left.print_recursive(depth + 1);
	} else {
	    System.out.println(" (NULL, - , 0)");
	}
	if (this.right != null) {
	    this.right.print_recursive(depth + 1);
	}
	else {
	    System.out.println(" (NULL, - , 0)");
	}
    }

    public void print() {
	System.out.println("Tree:");
	if (sentinel()) {
	    if (this.left != null) {
		this.left.print_recursive(0);
	    } else {
		System.out.println("Sentinel left is null");
	    }
	} else {
	    print_recursive(0);
	}
    }


    
}
