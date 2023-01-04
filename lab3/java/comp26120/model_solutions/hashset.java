package comp26120;

public class hashset implements set<String> {
    int verbose;
    HashingModes mode;

    speller_config config;

    cell[] cells;
    cell_chain[] cell_chains;
    int size;
    int num_entries; // number of cells in_use

    // TODO add any other fields that you need
    int collision;

    // This is  a cell structure assuming Open Addressing
    // You wil need alternative data-structures for separate chaining
    public class cell { // hash-table entry
	String element; // only data is the key itself
	state state;

	public cell(state s) {
	    state = s;
	}
    }

    public class cell_chain {
	String value;
	cell_chain link;

	public cell_chain() {
	    value = null;
	    link = null;
	}

	public cell_chain(String value) {
	    this.value = value;
	}

	public int insert(String value) {
	    if (this.value == null) {
		this.value = value;
		return 0;
	    } else if (this.value == value) {
		return 0;
	    } else if (this.link == null) {
		this.link = new cell_chain(value);
		return 1;
	    } else{
		return this.link.insert(value) + 1;
	    }
	}

	public boolean find(String value) {
	    if (this.value == null) {
		return false;
	    } else if (this.value.equals(value)) {
		return true;
	    } else if (this.link == null) {
		return false;
	    } else {
		return this.link.find(value);
	    }
	}

	public String print_chain() {
	    if (this.link == null) {
		return this.value;
	    } else {
		return this.value + "," + this.link.print_chain();
	    }
	}
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
	size = config.init_size;
	if (isSeparateChaining(mode)) {
	    cell_chains = initialise_cell_chain_array();
	} else {
	    cells = initialise_cell_array();
	}
    }

    private cell[] initialise_cell_array() {
	cell[] cell_array = new cell[size];
	num_entries = 0;
	collision = 0;

	for (int i = 0; i < size; i++) {
	    cell_array[i] = new cell(state.empty);
	}
	return cell_array;

    }

   private cell_chain[] initialise_cell_chain_array() {
	cell_chain[] cell_array = new cell_chain[size];
	num_entries = 0;
	collision = 0;

	for (int i = 0; i < size; i++) {
	    cell_array[i] = new cell_chain();
	}
	return cell_array;

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

    // h = x0*a^(k-1) + x1*a^(k-2) + ... + x(k-2)*a + x(k-1)
    // h = |ak + b| mod N
    public int hashFunc(String k, int N)
    {
	int temp = 1; int a = 41;
	int len = k.length();
	long h = 0;
	// System.err.format("%s, len: %d, k[%d]: %d%n\n", k, len, len - 1, h);
	for (int i = len - 1; i >= 0; i--){
	    int char_as_int = k.charAt(i);
	    h += char_as_int * temp;
	    // System.err.format("h += k[%d](%d) * %d, h = %d%n\n", i, (int) k.charAt(i), a, h);
	    temp *= a;
	}

	int h_int = (int) (Math.abs(h) % N);
	// System.err.format("%d\n", h_int);
	return h_int;
    }

    public int hashFunc2(String k, int N)
    {
	int len = k.length();
	int h = 0;
	for (int i = len - 1; i >= 0; i--) {
	    h += k.charAt(i);
	}
	int h_int = (int) (Math.abs(h) % N);
	return h_int;
    }

    // insertion

    private void insertCell(String k, int pos)
    {
	cells[pos].element = k;
	cells[pos].state = state.in_use;
	num_entries ++;
	return;
    }

    private void rehash()
    {
	int N = size;
	int newSize = nextPrime(2*N);
	if (this.verbose > 2) {
	    System.out.println("Rehashing");
	    System.out.println("Current Set");
	    this.print_set();
	}
	size = newSize;
	if (! isSeparateChaining(mode)) {
	    cell[] old_cells = cells.clone();
	    cells = initialise_cell_array();
	    for(int i = 0; i < N; i++){
		if(old_cells[i].state == state.in_use)
		    insert(old_cells[i].element);
	    }
	} else {
	    cell_chain[] old_cells = cell_chains.clone();
	    cell_chains = initialise_cell_chain_array();
	    for(int i = 0; i < N; i++){
		if (old_cells[i].value != null) {
		    cell_chain cell = old_cells[i];
		    insert(cell.value);
		    while (cell.link != null) {
			cell = cell.link;
			insert(cell.value);
		    }
		}
	    }
	}
	if (this.verbose > 2) {
	    System.out.println("New Set");
	    this.print_set();
	}
    }

    boolean isLinearProbing(HashingModes mode){
	return mode == HashingModes.HASH_1_LINEAR_PROBING || mode == HashingModes.HASH_2_LINEAR_PROBING;
    }

    boolean isQuadraticProbing(HashingModes mode){
	return mode == HashingModes.HASH_1_QUADRATIC_PROBING || mode == HashingModes.HASH_2_QUADRATIC_PROBING;
    }

    boolean isDoubleHashing(HashingModes mode){
	return mode == HashingModes.HASH_1_DOUBLE_HASHING || mode == HashingModes.HASH_2_DOUBLE_HASHING;
    }

    boolean isSeparateChaining(HashingModes mode){
	return mode == HashingModes.HASH_1_SEPARATE_CHAINING || mode == HashingModes.HASH_2_SEPARATE_CHAINING;
    }


    public void insert (String value) 
    {
	// TODO code for inserting into hash table

	if(find(value)) return; // detect duplicate

	int N = size;

	if(num_entries >= N/2) // check full table
	    rehash();

	N = size;
	int pos = hashFunc(value, N);

	// insert into empty cell
	if (! isSeparateChaining(mode)) {
	    if(cells[pos].state != state.in_use)
		insertCell(value, pos);

	    else{
		if(isLinearProbing(mode)) // linear probing: A[(i+j)mod N]
		    {
			for(int j = 1; j < N; j++){
			    int look = (pos + j) % N;
			    collision ++;
			    if(cells[look].state != state.in_use){
				insertCell(value, look);
				break;
			    }
			}
		    }
		else if(isQuadraticProbing(mode)) // quadratic probing: A[(i+j^2)mod N]
		    {
			for(int j = 1; j < N; j++){
			    int look = (pos + j*j) % N;
			    if (look < 0)
				look = 0;
			    collision ++;
			    if(cells[look].state != state.in_use){
				insertCell(value, look);
				break;
			    }
			}
		    }
		else if(isDoubleHashing(mode)) // double hash: A[(i+j*h'(k))mod N] 
		    {
			int temp = hashFunc2(value, N);

			for(int j = 1; j < N; j++){
			    int look = (pos + j*temp) % N;
			    collision ++;
			    if(cells[look].state != state.in_use){
				insertCell(value, look);
				break;
			    }
			}
		    }
	    }
	} else {
	    this.collision += cell_chains[pos].insert(value);
	    System.out.println(this.collision);
	    num_entries++;
	}
    }

    public boolean find (String value)
    {
	// TODO code for looking up in hash table
	int N = size;
	int pos = hashFunc(value, N);

	if (! isSeparateChaining(mode)) {
	    if(cells[pos].state == state.in_use
	       && (cells[pos].element.compareTo(value) == 0))
		return true;

	    else if(isLinearProbing(mode)) // linear probing
		{
		    for(int j = 1; j < N; j++){
			int look = (pos + j) % N;
			if(cells[look].state == state.empty)
			    return false;
			if(cells[look].state == state.in_use
			   && (cells[look].element.compareTo(value) == 0)){
			    return true;
			}
		    }
		}
	    else if(isQuadraticProbing(mode)) // quadratic probing
		{
		    for(int j = 1; j < N; j++){
			int look = (pos + j*j) % N;
			if (look < 0)
			    look = 0;
			if(cells[look].state == state.empty)
			    return false;
			if(cells[look].state == state.in_use &&
			   (cells[look].element.compareTo(value) == 0)){
			    return true;
			}
		    }
		}
	    else if(isDoubleHashing(mode)) // double hash
		{
		    int temp = hashFunc2(value, N);

		    for(int j = 1; j < N; j++){
			int look = (pos + j*temp) % N;
			if(cells[look].state == state.empty)
			    return false;
			if(cells[look].state == state.in_use &&
			   (cells[look].element.compareTo(value) == 0)){
			    return true;
			}
		    }
		}
	} else {
	    return cell_chains[pos].find(value);
	}

	return false;
    }

    public void print_set ()
    {
	 int i = 0;
	 for(; i < size; i++){
	     if (! isSeparateChaining(mode)) {
		 if(cells[i].state == state.in_use)
		     System.out.format("Cell %5d: %s\n", i, cells[i].element);
		 if(cells[i].state == state.empty)
		     System.out.format("Cell %5d: empty\n", i);
		 if(cells[i].state == state.deleted)
		     System.out.format("Cell %5d: deleted\n", i);
	     } else {
		 System.out.format("Cell %5d: %s\n", i, cell_chains[i].print_chain());
	     }
	 }

    }

    public void print_stats ()
    {
	// TODO code for printing statistic
	System.out.format("Collision times: %d\n", collision);
	System.out.format("Entry number: %d\n", num_entries);
	System.out.format("Average collisions per access: %f\n", (double)collision / (double)num_entries);

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
