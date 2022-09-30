package comp26120;

import java.util.Scanner;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

// Class for graphs.
public class graph_t {
    int num_nodes;
    succs_t[] adjs;

    public graph_t(int num_nodes) {
	graph_new(num_nodes);
    }

    public void graph_new(int num_nodes) {
	assert(num_nodes < Integer.MAX_VALUE);

	this.num_nodes = num_nodes;
	adjs = new succs_t[num_nodes];
	for (int i =  0; i < num_nodes; ++i) {
	    adjs[i] = new succs_t();
	}
    }

    /* Create graph from file. The file is a text file containing the positive integer numbers:
     *
     * num_nodes
     * num_edges
     * u_1 v_1 w_1
     * ...
     *
     * i.e., the number of nodes, then the number of edges, and then, for each edge, the source node, target node, and weight.
     *
     * Everything content after the last edge will be ignored.
     *
     * The function outputs an error message for files not adhering to this format!
 */
    public graph_t(InputStream is) {
	Scanner scanIn = new Scanner(is);
	int num_nodes = scanIn.nextInt();
	int num_edges = scanIn.nextInt();

	graph_new(num_nodes);

	for (int i = 0; i < num_edges; ++i) {
	    node_t u = scan_node(scanIn);
	    node_t v = scan_node(scanIn);
	    weight_t w = scan_weight(scanIn);
	    graph_add_edge(u, w, v);
	}
	scanIn.close();
    }

    public static final node_t scan_node(Scanner scanIn) {
	try {
	    int res_int = scanIn.nextInt();
	    return new node_t(res_int);
	} catch (Exception e) {
	    System.err.println("Error reading input");
	    System.exit(1);
	}
	return null;
    }

    public static final long scan_raw_weight(Scanner scanIn) {
	try {
	    long res_long = scanIn.nextLong();
	    return res_long;
	} catch (Exception e) {
	    System.err.println("Error reading input");
	    System.exit(1);
	}
	return 0;
    }

    public static final weight_t scan_weight(Scanner scanIn) {
	try {
	    long res_long = scanIn.nextLong();
	    return new weight_t(res_long);
	} catch (Exception e) {
	    System.err.println("Error reading input");
	    System.exit(1);
	}
	return null;
    }

    class succs_t {
	// n and capacity aren't really relvant for Java, but still...
	int n;
	int capacity; // Capacity
	ArrayList<edge_tgt_t> a = new ArrayList<edge_tgt_t>();

	public succs_t() {
	    n = 0;
	    capacity = 0;
	}

	public void succs_add(edge_tgt_t tgt) {
	    if (n >= capacity) {
		capacity = (capacity + 1)*2;
	    }

	    assert(n < capacity);
	    a.add(tgt);
	    n++;
	}
    }

    public void graph_check_node(node_t u) {
	if (!(u.i < num_nodes)) {
	    sp_algorithms.error("Node out of range: " + u.i);
	}
    }

    /**
     * Get number of nodes.
     */
    public int graph_get_num_nodes() {
	return num_nodes;
    }

    /**
     * Add edge to graph
     * @pre Nodes must be in range, i.e., u,v < num_nodes
     * @pre Weight must be finite
     * @pre Self-loop edges not allowed, i.e., u != v
     */
    public void graph_add_edge(node_t u, weight_t w, node_t v) {
	assert(u != v): "self loop edge " + u + " -> " + v;
	assert(w.weight_is_finite());

	graph_check_node(u);
	graph_check_node(v);
	adjs[u.i].succs_add(new edge_tgt_t(w, v));
    }

    /**
     * Get sucessors of specified node
     *
     * Each successor is represented by a weight and a target node.
     * One can query the number of successors, and array of successors
     *
     * For example, the following code snippet iterates over all successors of node u in graph g
     *
     *  for (edge_tgt_t tgt: g.get_graph_succs(u.i)) { / * use tgt.v and tgt.w to access target node and edge weight * / }
     *
     */
    public int graph_num_succs(node_t u) {
	return adjs[u.i].n;
    }

    /* Legacy from C code, not used */
    public edge_tgt_t graph_succs_begin(node_t u) {
	return adjs[u.i].a.get(0);
    }

    public ArrayList<edge_tgt_t> get_graph_succs(int i) {
	succs_t adj = adjs[i];
	return adj.a;
    }

    /* Legacy from C code, not used */
    public edge_tgt_t graph_succs_end(node_t u) {
	succs_t adj = adjs[u.i];
	return adj.a.get(adj.n);
    }

    /**
     * Write graph to file. Uses format described in @ref graph_read.
     */
    public void graph_write(OutputStream os) {
	OutputStreamWriter writer = new OutputStreamWriter(os);

	int N = graph_get_num_nodes();
	int num_edges = 0;

	for (int i = 0; i < N; ++i) {
	    num_edges += graph_num_succs(new node_t(i));
	}

	try {
	    String s = String.format("%d\n%d\n", N, num_edges);
	    writer.write(s);

	    for (int i = 0; i < N; ++i) {
		for (edge_tgt_t tgt : get_graph_succs(i)) {
		    s = String.format("%d %d % d\n", i, tgt.v.i, tgt.w.weight_to_int());
		    writer.write(s);
		}
	    }
	    writer.close();
	} catch (Exception e) {
	    sp_algorithms.error(e.getMessage());
	}
    }

    public static final path_t path_from_pred(ArrayList<node_t> pred, node_t v) {
	// Determine length
	int len = 0;

	node_t u = v;

	while (true) {
	    ++len;
	    if (u.i == pred.get(u.i).i) {
		break;
	    }
	    u = pred.get(u.i);
	}
	path_t p = new path_t(len);

	u = v;
	while (true) {
	    --len;
	    p.path_set(len, u);
	    if (u.i == pred.get(u.i).i) {
		break;
	    }
	    u = pred.get(u.i);
	}

	return p;
    }

}
