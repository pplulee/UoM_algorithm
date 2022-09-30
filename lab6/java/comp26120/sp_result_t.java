package comp26120;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

/**
 * Structure describing the result of a shortest path search between two nodes
 */
public class sp_result_t {
    node_t src;                      /// Start node
    node_t dst;                       /// Target node
    path_t path;                    /// Result path, NULL if unreachable
    weight_t dist;                   /// Distance, INF if unreachable
    long relax_count;   /// Number of relaxed edges

    public sp_result_t(node_t src, node_t dst, path_t p, weight_t d, long c) {
	this.src = src;
	this.dst = dst;
	this.path = p;
	this.dist = d;
	this.relax_count = c;
    }

    public void print_sp_result(OutputStream os) {
	try {
            OutputStreamWriter writer = new OutputStreamWriter(os);
	    writer.write("Distance: ");
	    dist.print_weight(writer);
	    writer.write("\n");

	    writer.write("Path: ");
	    if (path == null) {
		writer.write("NULL");
	    } else {
		path.print_path(writer);
	    }
	    writer.write("\n");

	    String s = String.format("# Relaxed nodes: %d\n", relax_count);
	    writer.write(s);
	    writer.flush();

        } catch (IOException e) {
            System.err.println("Error Message: " + e.getMessage());
            System.exit(-1);
        }

    }
}
