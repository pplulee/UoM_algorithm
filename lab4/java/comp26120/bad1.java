package comp26120;

public class bad1 implements PriorityQueue {
    String value;

    public boolean contains(String value, int priority) {
	return false;
    }

    public void insert(String value, int priority) {
    }

    public boolean is_empty() {
	return false;
    }

    public String pop_min() {
	return null;
    }

    public void print() {}
	
}
