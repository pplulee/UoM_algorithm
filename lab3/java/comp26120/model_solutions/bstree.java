package comp26120;

public class bstree implements set<String> {
    int verbose;

    String value;
    bstree left;
    bstree right;

    speller_config config;

    // TODO add fields for statistics

    public bstree(speller_config config) {
	verbose = config.verbose;
	this.config = config;
    }

	
    public int size(){
	// This presumes that if value is not null then (possibly empty) left and right trees exist.
	if(tree()){
	    return 1 + left.size() + right.size();
	}
	return 0;
    } 

    public void insert (String value) 
    {
	if(tree()){
	    int comp = value.compareTo(this.value);
	    if (comp < 0) {
		this.left.insert(value);
	    } else if (comp > 0) {
		this.right.insert(value);
	    }
	    // if comp == 0 then do nothing as it's a duplicate
	}
	else{
	    left = new bstree(this.config);
	    right = new bstree(this.config);
	    this.value = value;
	}
    }

    public boolean find (String value)
    {
	if(tree()){
	    int comp = value.compareTo(this.value);
	    if (comp == 0) { return true;}
	    else if (comp < 0) {return left.find(value);}
	    else return right.find(value);
	}
	// if tree is NULL then it contains no values
	return false;
    }

    private boolean tree() {
	return (value != null);
    }

    // You can update this if you want
    public void print_set_recursive(int depth)
    {
	if(tree()){
	    for(int i=0;i<depth;i++){ System.out.print(" "); }
	    System.out.format("%s\n",value);
	    left.print_set_recursive(depth+1);
	    right.print_set_recursive(depth+1);
	}
    } 

    // You can update this if you want
    public void print_set ()
    {
	System.out.print("Tree:\n");
	print_set_recursive(0);
    }

    public void print_stats ()
    {
	// TODO update code to record and print statistics
    }
}
