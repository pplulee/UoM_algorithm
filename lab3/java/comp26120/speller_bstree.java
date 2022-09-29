package comp26120;

public class speller_bstree extends speller {
    String prog_name = "speller_bstree";

    public set_factory.SetType data_structure() {
	return set_factory.SetType.BSTREE;
    }

    public static void main(String args[]) {
	speller S = new speller_bstree();

	speller.spelling(S, args);
    }
}
