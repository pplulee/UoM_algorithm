package comp26120;

public class speller_hashset extends speller {
    String prog_name = "speller_hashset";

    public set_factory.SetType data_structure() {
	return set_factory.SetType.HASH;
    }

    public static void main(String args[]) {
	speller S = new speller_hashset();

	speller.spelling(S, args);
    }
}
