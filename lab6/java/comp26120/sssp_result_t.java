package comp26120;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

/*
 * The main components of a single-source shortest path result are a predecessor map and a distance map (encoded as arrays).
 *
 * The distance map assigns each node to its distance from the source node.
 *    If the node is unreachable, the distance is inf.
 *    If the node is reachable via a negative weight cycle, the distance is -inf.
 *
 * The predecessor map assigns nodes to predecessor nodes on a shortest path or negative cycle.
 *    If the node is unreachable, the predecessor must be INVALID_NODE.
 *    If the node has finite distance, its predecessor must be the previous node on a shortest path. EXCEPTION: The predecessor of the start node is the start node itself.
 *    If the node has -inf distance, following the predecessors must yield a negative-weight cycle. NOTE: In this case, there is no exception for the start node!
 *
 */
public class sssp_result_t {
    int N; /// Number of nodes, to make result more self contained
    node_t src; /// Start node
    node_t dst; /// If != INVALID_NODE, this is a partial result, only accurate for dst
    ArrayList<node_t> pred = new ArrayList<node_t>(); /// Predecessor map
    boolean has_negative_cycle; /// True if negative cycle was detected. Pred and dist are NULL then.
    ArrayList<weight_t> dist = new ArrayList<weight_t>(); /// Distance map
    long relax_count; /// Number of relaxed edges
    
    public sssp_result_t(int N, node_t src, node_t dst, boolean ncyc, ArrayList<node_t> p, ArrayList<weight_t> d, long c) {
	this.N = N;
	this.src = src;
	this.dst = dst;
	this.pred.addAll(p);
	this.has_negative_cycle = ncyc;
	this.dist.addAll(d);
	this.relax_count = c;
    }

    /// Convert sssp to sp result.
    public sp_result_t sssp_to_sp_result(node_t dst) {
	path_t p = null;

	assert(this.dst == node_t.INVALID_NODE || this.dst == dst);

	if (pred.get(dst.i) != node_t.INVALID_NODE) {
	    p = new path_t(this.pred,dst);
	}

	sp_result_t r = new sp_result_t(this.src, dst, p, dist.get(dst.i), relax_count);
	return r;
    }

        public void print_sssp_result(OutputStream os) {
	try {
            OutputStreamWriter writer = new OutputStreamWriter(os);
	    int  NN = N<10?N:10;

	    writer.write("Distmap:");
	    for (int i = 0; i<NN; ++i) {
		writer.write(" ");
		dist.get(i).print_weight();
	    }

	    if (N < NN) {
		writer.write("...\n");
	    } else {
		writer.write("\n");
	    }

        } catch (IOException e) {
            System.err.println("Error Message: " + e.getMessage());
            System.exit(-1);
        }

    }

}
