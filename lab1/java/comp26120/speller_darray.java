package comp26120;

public class speller_darray extends speller {
    String prog_name = "speller_darray";

    public set_factory.SetType data_structure() {
	return set_factory.SetType.DARRAY;
    }

    public static void main(String args[]) {
	speller S = new speller_darray();

	speller.spelling(S, args);
    }
}
