package comp26120;

public class bad5 implements PriorityQueue {
    String value1 = null;
    String value2 = null;
    int priority1;
    int priority2;

    public boolean contains(String value, int priority) {
	return false;
    }

    public void insert(String value, int priority) {
	if (this.value1 == null) {
	    this.value1 = value;
	    this.priority1 = priority;
	} else{
	    this.value2 = value;
	    this.priority2 = priority;
	    if (this.priority2 < this.priority1) {
		String tv = this.value1;
		int tp = this.priority1;
		this.value1 = this.value2;
		this.priority1 = this.priority2;
		this.value2 = tv;
		this.priority2 = tp;
	    }
	}
    }

    public boolean is_empty() {
	return false;
    }

    public String pop_min() {
	String res = this.value1;
	this.value1  = this.value2;
	this.priority1 = this.priority2;
	this.value2 = null;
	return res;
    }

    public void print() {}
	
}
