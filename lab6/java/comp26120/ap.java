package comp26120;

public class ap {
    airports airport_info = new airports();
    general settings;

    public ap(general settings) {
	this.settings = settings;
    }

    private static char[] code_string_to_code(String code_string) {
	char [] code = new char[3];
	for (int i = 0; i < 3; i++) {
	    code[i] = code_string.charAt(i);
	}
	// code[3] = 0;
	return code;
    }

    public int count_aux(node_t u, boolean[] visited) {
	int count = 0;
	if (visited[u.i]) {
	    return count;
	}
	visited[u.i] = true;
	++count;

	graph_t g = airport_info.ap_get_graph();

	for (edge_tgt_t tgt: g.get_graph_succs(u.i)) {
	    count += count_aux(tgt.v, visited);
	}

	return count;
    }
    
    public void count_reachable(String code_string) {
	char[] code = code_string_to_code(code_string);
	airports.apid_t id = airport_info.ap_get_id(code);
	boolean[] visited = new boolean[airport_info.ap_get_num_ids()];
	for (int i = 0; i < airport_info.ap_get_num_ids(); ++i) {
	    visited[i] = false;
	}

	int count = count_aux(id, visited);
	
	System.out.format("%d airports reachable from %s\n",count,new String(code));
    }

    public weight_t path_dist(path_t p) {
	weight_t dist = new weight_t(0);

	for (int i=0;i+1<p.path_len();++i) {
	    dist = weight_t.weight_add(dist, airport_info.ap_get_dist(new airports.apid_t(p.path_get(i)), new airports.apid_t(p.path_get(i+1))));
	}

	return dist;
    }

    public void print_ap_path(path_t p) {
	for (int i = 1; i<p.path_len();++i) {
	    airports.apid_t u = new airports.apid_t(p.path_get(i-1));
	    airports.apid_t v = new airports.apid_t(p.path_get(i));
	    System.out.format("%s to %s (%dkm)\n", new String(airport_info.ap_get_code(u)), new String(airport_info.ap_get_code(v)), airport_info.ap_get_dist(u, v).__w);
	}
    }

    public void print_route(sp_result_t res) {
	if (res.path != null) {
	    print_ap_path(res.path);
	    System.out.format("Total = %dkm\n", path_dist(res.path).__w);
	} else {
	    System.out.format("No route from %s to %s\n", new String(airport_info.ap_get_code(new airports.apid_t(res.src.i))), new String(airport_info.ap_get_code(new airports.apid_t(res.dst.i))));
	}

	System.out.format("LOG: relaxed %d edges\n\n", res.relax_count);
    }

    public void compute_route(String algo, String scode_string, String dcode_string) {
	char[] scode = code_string_to_code(scode_string);
	char[] dcode = code_string_to_code(dcode_string);
	
	airports.apid_t s = airport_info.ap_get_id(scode);
	airports.apid_t d = airport_info.ap_get_id(dcode);
	graph_t g = airport_info.ap_get_graph();

	weight_t[] h = new weight_t[g.graph_get_num_nodes()];

	for (int u = 0; u< g.graph_get_num_nodes(); ++ u) {
	    airports.apid_t apid_u = new airports.apid_t(u);
	    h[u] = airport_info.ap_is_valid_id(apid_u)?airport_info.ap_get_dist(apid_u,d):new weight_t.weight_inf();
	}

	if (algo.equals("bellman-ford")) {
	    print_route(sp_algorithms.bellman_ford(g, s).sssp_to_sp_result(d));
	} else if (algo.equals("dijkstra")) {
	    print_route(sp_algorithms.dijkstra(g, s, d).sssp_to_sp_result(d));
	} else if (algo.equals("astar")) {
	    print_route(sp_algorithms.astar_search(g,s,d,h));
	} else if (algo.equals("bfs")) {
	    print_route(sp_algorithms.bfs(g,s,d).sssp_to_sp_result(d));
	} else {
	    sp_algorithms.error ("Invalid algorithm name: " + algo);
	}

    }

    public static void main(String[] args) {
	general general_settings = new general();
	general_settings.set_msg_verb(-1);

	ap ap = new ap(general_settings);
	ap.airport_info.ap_std_init();

	if (args.length == 4 && args[0].equals("route")) {
	    ap.compute_route(args[1],args[2],args[3]);
	} else if (args.length == 2 && args[0].equals("count")) {
	    ap.count_reachable(args[1]);
	} else {
	    sp_algorithms.error("Invalid command line");
	}
    }
}
