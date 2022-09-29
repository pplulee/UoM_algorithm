package comp26120;

public class hashset implements set<String> {
    int verbose;
    HashingModes mode;

    speller_config config;

    cell[] cells;
    int size;
    int num_entries; // number of cells in_use

    // TODO add any other fields that you need

    // This is  a cell structure assuming Open Addressing
    // You wil need alternative data-structures for separate chaining
    public class cell { // hash-table entry
	String element; // only data is the key itself
	state state;
    }

    public static enum state {
	empty,
	in_use,
	deleted;
    }

    public hashset(speller_config config) {
	verbose = config.verbose;
	mode = HashingModes.getHashingMode(config.mode);

	// TODO: create initial hash table
	
    }

    // Helper functions for finding prime numbers 
    public boolean isPrime (int n)
    {
	for (int i = 2; i*i <= n; i++)
	    if (n % i == 0)
		return false;
	return true;
    }

    public int nextPrime(int n)
    {
	int i = n;
	while (!isPrime(i)) {
	    i++;
	}
	return i;
    }

    public void insert (String value) 
    {
	// TODO code for inserting into hash table
    }

    public boolean find (String value)
    {
	// TODO code for looking up in hash table
	return false;
    }

    public void print_set ()
    {
	// TODO code for printing hash table
    }

    public void print_stats ()
    {
	// TODO code for printing statistic
    }

    // Hashing Modes

    public enum HashingModes {
	HASH_1_LINEAR_PROBING, // =0 in mode flag
        HASH_1_QUADRATIC_PROBING, // =1, 
        HASH_1_DOUBLE_HASHING, //=2, 
        HASH_1_SEPARATE_CHAINING, // =3,
        HASH_2_LINEAR_PROBING, // =4, 
        HASH_2_QUADRATIC_PROBING, // =5, 
        HASH_2_DOUBLE_HASHING, // =6, 
        HASH_2_SEPARATE_CHAINING; // =7

	public static HashingModes getHashingMode(int i) {
	    switch (i) {
	    case 1:
		return HASH_1_QUADRATIC_PROBING;
	    case 2:
		return HASH_1_DOUBLE_HASHING;
	    case 3:
		return HASH_1_SEPARATE_CHAINING;
	    case 4:
		return HASH_2_LINEAR_PROBING;
	    case 5:
		return HASH_2_QUADRATIC_PROBING;
	    case 6:
		return HASH_2_DOUBLE_HASHING;
	    case 7:
		return HASH_2_SEPARATE_CHAINING;
	    default:
		return HASH_1_LINEAR_PROBING;
	    }
	}
    }

    // Your code

   


}
