package comp26120;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.util.ArrayList;

/// Paths
/**
 * A path is a sequence of nodes with a specified length.
 */

public class path_t {
    int len;
    node_t[] nodes;

    public path_t(int len) {
	this.len = len;
	this.nodes = new node_t[len];
	for (int i = 0; i < len; ++i) {
	    this.nodes[i] = node_t.INVALID_NODE;
	}
    }

    /**
     * Extract path from predecessor array. Convention: Start node points to itself.
     */
    public path_t(ArrayList<node_t> pred, node_t v) {
	// Determine length
	this(0);
	int local_len = 0;

	node_t u = v;

	while (true) {
	    len++;
	    local_len++;
	    if (u.i == pred.get(u.i).i) {
		break;
	    }
	    u = pred.get(u.i);
	}

	u=v;

	this.nodes = new node_t[len];
	for (int i = 0; i < len; ++i) {
	    this.nodes[i] = node_t.INVALID_NODE;
	}

	while (true) {
	    local_len--;
	    path_set(local_len, u);
	    if (u.i == pred.get(u.i).i) {
		break;
	    }
	    u = pred.get(u.i);
	}
    }

    public void path_set(int i, node_t u) {
	assert(i<len);
	nodes[i] = u;
    }

    public int path_len() {
	return len;
    }

    public node_t path_get(int i) {
	assert(i<len);
	return nodes[i];
    }

    public void print_path(OutputStreamWriter writer) {
	try {
	    if (nodes == null) {
		writer.write("NULL\n");
	    } else if (path_len() == 0) {
		writer.write("EMP\n");
	    } else {
		String s = String.format("%d",path_get(0).i);
		writer.write(s);
		for (int i = 1; i< path_len(); ++i) {
		    s = String.format(" : %d",path_get(i).i);
		    writer.write(s);
		}
	    }
	    // writer.close();
        } catch (IOException e) {
            System.err.println("Error Message: " + e.getMessage());
            System.exit(-1);
        }
    }
}
