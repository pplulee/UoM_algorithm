package comp26120;

import java.util.ArrayList;

public interface PriorityQueue {
    /**
     * Get priority of node.
     *
     * Complexity: O(1)
     *
     * @pre u < N
     */
    public weight_t DPQ_prio(node_t u);

    /**
     * Check if node is contained in queue
     *
     * Complexity: O(1)
     *
     * @pre u < N
     */
    public boolean DPQ_contains(node_t u);

    /**
     * Insert node into queue, with given priority.
     * The priority of this node is set accordingly.
     *
     * Complexity: O(log N)
     *
     * @pre Node must not be in queue
     * @pre u < N
     * @param u node
     * @param w priority
     */
    public void DPQ_insert(node_t u, weight_t w);

    /**
     * Check if queue is empty
     *
     * Complexity: O(1)
     */
    public boolean DPQ_is_empty();

    /**
     * Retrieve and remove an element of the queue with minimal priority
     *
     * Complexity: O(log N)
     *
     * @pre The queue is not empty
     */
    public node_t DPQ_pop_min();

    /**
     * Lower priority of element in queue
     *
     * Complexity: O(log N)
     *
     * @pre the node is in the queue
     * @pre the new priority is less than the current nodes priority
     */
    public void DPQ_decrease_key(node_t u, weight_t w);

    /**
     * Priority map
     */
    public ArrayList<weight_t> DPQ_dist_free();

}
