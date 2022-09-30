package comp26120;

public class hashmap_t {
    public static class hashmap_value_t {
	int value;
	
	public hashmap_value_t(int i) {
	    value = i;
	}
    }

    public static class hashmap_key_t implements Comparable<hashmap_key_t>{
	String key;

	public hashmap_key_t(String s) {
	    key = s;
	}

	public hashmap_key_t(char[] cs) {
	    key = new String(cs);
	}

	public int compareTo(hashmap_key_t k) {
	    return key.compareTo(k.key);
	}

	public String getString() {
	    return key;
	}
    }
    
    // This is  a cell structure assuming Open Addressing
    public class cell { // hash-table entry
	hashmap_key_t key;
	hashmap_value_t value;
	state state;

	public cell(state s) {
	    state = s;
	}
    }

    public static enum state {
	empty,
	in_use,
	deleted;
    }

    cell[] cells;
    int size;
    int num_entries; // number of cells in_use
    HashingModes mode;

    long collision;

    class hashcode_t {
	int i;
	
	public hashcode_t(int i) {
	    this.i = i;
	}
    }

    int compare_keys(hashmap_key_t a, hashmap_key_t b) {
	return a.compareTo(b);
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
    public hashcode_t hashFunc(String k, int N)
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
	return new hashcode_t(h_int);
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

    int DOUBLE_HASH_Q=7919;

    public hashmap_t(int size, HashingModes mode) {
	if (size < 5) {
	    size = 5;
	}
	size = nextPrime(size);

	if (isDoubleHashing(mode) && size <= DOUBLE_HASH_Q) {
	    assert(isPrime(DOUBLE_HASH_Q));
	    size = nextPrime(DOUBLE_HASH_Q + 1);
	}

	this.cells = new cell[size];
	this.size = size;
	this.num_entries = 0;
	this.collision = 0;
	this.mode = mode;

	for (int i = 0; i < size;  i++) {
	    this.cells[i] = new cell(state.empty);
	}
    }

    public int hashmap_get_size() {
	return this.num_entries;
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

    // insertion

    private void insertCell(hashmap_key_t k, hashmap_value_t v, int pos)
    {
	cells[pos].key = k;
	cells[pos].value = v;
	cells[pos].state = state.in_use;
	num_entries++;
	return;
    }

    private void rehash()
    {
	int N = size;
	int newSize = nextPrime(2*N);
	cell[] old_cells = cells.clone();
	size = newSize;
	cells = initialise_cell_array();
	for(int i = 0; i < N; i++){
	    if(old_cells[i].state == state.in_use) {
		hashmap_insert(old_cells[i].key, old_cells[i].value );
	    }
	}
    }

    public void hashmap_insert (hashmap_key_t key, hashmap_value_t value) 
    {
	if (hashmap_contains(key)) {
	    sp_algorithms.error("Duplicate key " + key); //detect duplicate
	}

	int N = size;

	if ((num_entries >= N) || (isQuadraticProbing(mode) && num_entries >= N/2))
	    rehash();

	N = size;

	// System.out.format("INSERT %s -> %zu\n", key, value);

	hashcode_t pos = hashFunc(key.getString(), N);

	// insert into empty cell
	if(cells[pos.i].state != state.in_use)
	    insertCell(key, value, pos.i);

	else{
	    if(isLinearProbing(mode)) // linear probing: A[(i+j)mod N]
		{
		    for(int j = 1; j < N; j++){
			int look = (pos.i + j) % N;
			collision ++;
			if(cells[look].state != state.in_use){
			    insertCell(key, value, look);
			    break;
			}
		    }
		}
	    else if(isQuadraticProbing(mode)) // quadratic probing: A[(i+j^2)mod N]
		{
		    for(int j = 1; j < N; j++){
			int look = (pos.i + j*j) % N;
			collision ++;
			if(cells[look].state != state.in_use){
			    insertCell(key, value, look);
			    break;
			}
		    }
		}
	    else if(isDoubleHashing(mode)) // double hash: A[(i+j*h'(k))mod N] h'(k)=q-(k mod q)
		{
		    int q = 7919; // q<N a prime number
		    int temp = q - pos.i % q;

		    for(int j = 1; j < N; j++){
			int look = (pos.i + j*temp) % N;
			collision ++;
			if(cells[look].state != state.in_use){
			    insertCell(key, value, look);
			    break;
			}
		    }
		}
	}
    }

    public hashmap_value_t hashmap_lookup(hashmap_key_t key)
    {
	hashmap_value_t value = null;
	int N = size;
	hashcode_t pos = hashFunc(key.getString(), N);

	if(cells[pos.i].state == state.in_use
	   && (cells[pos.i].key.compareTo(key) == 0))
	    {
		if (value == null) {
		    value = cells[pos.i].value;
		    return value;
		}
	    }
	else if(isLinearProbing(mode)) // linear probing
	    {
		for(int j = 1; j < N; j++){
		    int look = (pos.i + j) % N;
		    if(cells[look].state == state.empty)
			return null;
		    if(cells[look].state == state.in_use
		       && (cells[look].key.compareTo(key) == 0)){
			if (value == null) {
			    value = cells[look].value;
			    return value;
			}

		    }
		}
	   }
       else if(isQuadraticProbing(mode)) // quadratic probing
	   {
	       for(int j = 1; j < N; j++){
		   int look = (pos.i + j*j) % N;
		   if(cells[look].state == state.empty)
		       return null;
		   if(cells[look].state == state.in_use &&
		      (cells[look].key.compareTo(key) == 0)){
			if (value == null) {
			    value = cells[look].value;
			    return value;
			}

		   }
	       }
	   }
       else if(isDoubleHashing(mode)) // double hash
	   {
	       int q = DOUBLE_HASH_Q;
	       int temp = q - pos.i % q;

	       for(int j = 1; j < N; j++){
		   int look = (pos.i + j*temp) % N;
		   if(cells[look].state == state.empty)
		       return null;
		   if(cells[look].state == state.in_use &&
		      (cells[look].key.compareTo(key) == 0)){
			if (value == null) {
			    value = cells[look].value;
			    return value;
			}
		   }
	       }
	   }

	return value;
    }

    public boolean hashmap_contains(hashmap_key_t key) {
	if (hashmap_lookup(key) != null) {
	    return true;
	}
	return false;
    }

    public void hashmap_print_set ()
    {
	 for(int i = 0; i < size; i++){
	     if(cells[i].state == state.in_use)
		 System.out.format("Cell %zu: %s=>%zu\n", i, cells[i].key, cells[i].value);
	     if(cells[i].state == state.empty)
		 System.out.format("Cell %zu: empty\n", i);
	     if(cells[i].state == state.deleted)
		 System.out.format("Cell %zu: deleted\n", i);
	 }
    }

    public void hashmap_print_stats ()
    {
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
