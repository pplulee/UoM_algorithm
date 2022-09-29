package comp26120;

public class bad2 implements PriorityQueue {
    String value;

    public boolean contains(String value, int priority) {
	return false;
    }

    public void insert(String value, int priority) {
	this.value = value;
    }

    public boolean is_empty() {
	return false;
    }

    public String pop_min() {
	return value;
    }

    public void print() {}
	
}
