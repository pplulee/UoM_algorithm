package comp26120;

public class general {
    public int log_verb = 0;

    public void set_msg_verb(int v) {
	log_verb = v;
    }

    public int get_verb() {
	return log_verb;
    }

    public void msg(int verb, String s) {
	if (log_verb >= verb) {
	    for (int i = 0; i<verb; ++i) {
		System.out.format("    ");
	    }
	    System.out.format("LOG: ");
	    System.out.println(s);
	}
    }
}
