package comp26120;

public class simple_test_graph {
    general settings;

    public simple_test_graph(general settings) {
	this.settings = settings;
    }

    public void compute_path(String algo, String src, String dst) {
	node_t s = new node_t(Integer.parseInt(src));
	node_t d = new node_t(Integer.parseInt(dst));

	graph_t g = new graph_t(10);
	g.graph_add_edge(new node_t(0), new weight_t(1), new node_t(1));
	g.graph_add_edge(new node_t(1), new weight_t(2), new node_t(2));
	g.graph_add_edge(new node_t(2), new weight_t(3), new node_t(3));
	g.graph_add_edge(new node_t(3), new weight_t(1), new node_t(4));
        g.graph_add_edge(new node_t(5), new weight_t(1), new node_t(6));
	g.graph_add_edge(new node_t(6), new weight_t(1), new node_t(8));
	g.graph_add_edge(new node_t(8), new weight_t(2), new node_t(9));
	g.graph_add_edge(new node_t(5), new weight_t(9), new node_t(9));
	if (algo.equals("bellman-ford-neg")) {
	    g.graph_add_edge(new node_t(3), new weight_t(-1), new node_t(0));
	    g.graph_add_edge(new node_t(6), new weight_t(-5), new node_t(7));
	} else {
	    g.graph_add_edge(new node_t(3), new weight_t(4), new node_t(0));
	    g.graph_add_edge(new node_t(5), new weight_t(5), new node_t(7));
	}

	weight_t[] h = new weight_t[g.graph_get_num_nodes()];
	for (int u = 0; u< g.graph_get_num_nodes(); ++ u) {
	    h[u] = new weight_t(java.lang.Math.abs(d.i - u));
	}

	if (algo.equals("bellman-ford")) {
	    sp_algorithms.bellman_ford(g, s).sssp_to_sp_result(d).print_sp_result(System.out);
	} else if (algo.equals("bellman-ford-neg")) {
	    sp_algorithms.bellman_ford(g, s).sssp_to_sp_result(d).print_sp_result(System.out);
	} else if (algo.equals("dijkstra")) {
	    sp_algorithms.dijkstra(g, s, d).sssp_to_sp_result(d).print_sp_result(System.out);
	} else if (algo.equals("astar")) {
	    sp_algorithms.astar_search(g,s,d,h).print_sp_result(System.out);
	} else if (algo.equals("bfs")) {
	    sp_algorithms.bfs(g,s,d).sssp_to_sp_result(d).print_sp_result(System.out);
	} else {
	    sp_algorithms.error ("Invalid algorithm name: " + algo);
	}

    }

    public static void main(String[] args) {
	general general_settings = new general();
	general_settings.set_msg_verb(-1);

	simple_test_graph ap = new simple_test_graph(general_settings);

	if (args.length == 3 ) {
	    ap.compute_path(args[0],args[1],args[2]);
	} else if (args.length == 4) {
	    if (args[3].equals("-v")) {
                general_settings.set_msg_verb(0);
            } else if (args[3].equals("-vv")) {
                general_settings.set_msg_verb(1);
            } else if (args[3].equals("-vvv")) {
                general_settings.set_msg_verb(2);
	    }

	    ap.compute_path(args[0],args[1],args[2]);
	} else {
	    sp_algorithms.error("Invalid command line");
	}
    }
}
