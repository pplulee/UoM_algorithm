package comp26120;

import java.util.ArrayList;

public class sp_algorithms {

    public static final void error (String msg) {
	System.err.println(msg);
	System.exit(1);
    }

    /**
     * Use BFS to compute SSSP.
     * Edge weights are to be ignored, and the shortest paths in terms
     * of edge count shall be computed.
     *
     * If dst is not INVALID_NODE, the algorithm should stop as soon as it has computed a shortest path to dst.
     *
     */
    public static sssp_result_t bfs(graph_t g, node_t src, node_t dst) {
	long stat_edges_explored=0;

	int N = g.graph_get_num_nodes();

	ArrayList<node_t> pred = new ArrayList<node_t>();
	ArrayList<weight_t> dist = new ArrayList<weight_t>();
	for (int i=0; i < N; ++i) {
	    pred.add(node_t.INVALID_NODE);
	    dist.add(new weight_t.weight_inf());
	}

	error("Not implemented");

	return new sssp_result_t(N, src, dst, false, pred, dist, stat_edges_explored);
    }

    /**
     * Use Bellman-Ford to compute shortest paths in a weighted graph.
     * For nodes reachable from infinite weight cycles, your algorithm
     * should report a distance of -inf, and the predecessor INVALID_NODE.
     *
     */
    public static sssp_result_t bellman_ford(graph_t g, node_t src) {
	error("Not implemented");

	return null;
    }

    /**
     * Use Dijkstra's algorithm to compute shortest paths in a weighted graph with
     * non-negative weights.
     *
     * If dst is not INVALID_NODE, the algorithm should stop as soon as it has computed a shortest path to dst.
     *
     * @pre Graph has no negative weights
     */
    public static sssp_result_t dijkstra(graph_t g, node_t src, node_t dst) {
	error("Not implemented");

	return null;
    }

    /**
     * Use the A* algorithm to compute a shortest path between src and dst.
     * You can assume that there are no negatrive weights, and that the heuristics h is monotone.
     *
     * @pre Graph has no negative weights
     * @pre h is monotone, i.e., for all u, h(u) + w(u,v) <= h(v)
     *
     */
    public static sp_result_t astar_search(graph_t g, node_t src, node_t dst, weight_t[] h) {
	error("Not implemented");

	return null;
    }

}
