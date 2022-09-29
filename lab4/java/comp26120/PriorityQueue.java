package comp26120;

public interface PriorityQueue {
    public boolean contains(String s, int i);

    public void insert(String s, int i);

    public boolean is_empty();

    public String pop_min();

    public void print();
}
