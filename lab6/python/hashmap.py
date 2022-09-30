from enum import Enum
import general

DOUBLE_HASH_Q = 7919
    
class hashmap_t:
    def __init__(self, size, mode):
        if (size < 5):
            size = 5
        size = self.nextPrime(size)
        
        if (self.isDoubleHashing(mode) and size <= DOUBLE_HASH_Q):
            assert(self.isPrime(DOUBLE_HASH_Q))
            size = self.nextPrime(DOUBLE_HASH_Q + 1)
        
        self.size = size
        self.cells = self.initialise_cell_array()
        self.mode = mode
        
    def initialise_cell_array(self):
        self.num_entries = 0
        self.collision = 0
        cells = []

        for i in range(self.size):
            new_cell = cell()
            new_cell.state = state.empty
            cells.append(new_cell)
        return cells
        
                
    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while (i * i < n):
            if (n % i == 0):
                return False
            i = i + 1
        return True
        
    def nextPrime(self, n):
        while (not self.isPrime(n)):
            n = n + 1
        return n
        
    def hashFunc(self, k, N):
        temp = 1
        a = 41
        string_len = len(k)
        h = 0
        i = string_len - 1
        while i >= 0:
            h = h + ord(k[i]) * temp
            temp = temp * a
            i = i - 1
            
        h = abs(h) % N
        return h
        
    def isLinearProbing(self, mode):
        return (mode == HashingModes.HASH_1_LINEAR_PROBING or mode == HashingModes.HASH_2_LINEAR_PROBING)
        
    def isQuadraticProbing(self, mode):
        return (mode == HashingModes.HASH_1_QUADRATIC_PROBING or mode == HashingModes.HASH_2_QUADRATIC_PROBING)
        
    def isDoubleHashing(self, mode):
        return (mode == HashingModes.HASH_1_DOUBLE_HASHING or mode == HashingModes.HASH_2_DOUBLE_HASHING)
    
    def hashmap_get_size(self):
        return self.num_entries
        
    # insertion
    
    def insertCell(self, k, v, pos):
        self.cells[pos].key = k
        self.cells[pos].value = v
        self.cells[pos].state = state.in_use
        self.num_entries = self.num_entries + 1
        
    def rehash(self):
        N = self.size
        newSize = self.nextPrime(2 * N)
        self.size = newSize
        old_cells = self.cells.copy()
        
        self.cells = self.initialise_cell_array()
        for i in range(N):
            if (old_cells[i].state == state.in_use):
                self.hashmap_insert(old_cells[i].key,old_cells[i].value)
                        

    def hashmap_insert(self, key, value):
        if self.hashmap_contains(key):
            general.error("Duplicate key %s", key) # detect duplicate
            
        N = self.size
        if (self.num_entries >= N or (self.isQuadraticProbing(self.mode) and self.num_entries >= N/2)):
            self.rehash()
        N = self.size
            
        pos = self.hashFunc(key, N)
        
        # insert into empty cell
        if (self.cells[pos].state != state.in_use):
            self.insertCell(key, value, pos)
        else:
            if self.isLinearProbing(self.mode): # linear probing: A[(i + j)mod N]
                for j in range(1, N):
                    look = (pos + j) % N
                    self.collision = self.collision + 1
                    if (self.cells[look].state != state.in_use):
                        self.insertCell(key, value, look)
                        break
            elif self.isQuadraticProbing(self.mode): # quadratic probing : A[(i + j^2)mod N]
                for j in range (1, N):
                    look = (pos + j*j) % N
                    self.collision = self.collision + 1
                    if (self.cells[look].state != state.in_use):
                        self.insertCell(key, value, look)
                        break
            elif self.isDoubleHashing(self.mode): # double hash: A[(i+j*h'(k))mod N] h'(k)=q-(k mod q)
                q = DOUBLE_HASH_Q # q<N a prime number
                assert(q<N)
                temp = q - pos % q
                
                for j in range(1, N):
                    look = (pos + j * temp) % N
                    self.collision = self.collision + 1
                    if (self.cells[look].state != state.in_use):
                        self.insertCell(key, value, look)
                        break
        
    def hashmap_lookup(self, key):
        N = self.size
        pos = self.hashFunc(key, N)
        
        value = None
        
        if (self.cells[pos].state == state.in_use and self.cells[pos].key == key):
            if (value == None):
                value = self.cells[pos].value
                return value;
            
        elif self.isLinearProbing(self.mode):
            for j in range(1, N):
                look = (pos + j) % N
                if (self.cells[look].state == state.empty):
                    return None
                if (self.cells[look].state == state.in_use and self.cells[look].key == key):
                    if (value == None):
                        value = self.cells[look].value
                        return value
        elif self.isQuadraticProbing(self.mode):
            for j in range(1, N):
                look = (pos + j*j) % N
                if (self.cells[look].state == state.empty):
                    return None
                if (self.cells[look].state == state.in_use and self.cells[look].key == key):
                    if (value == None):
                        value = self.cells[look].value
                        return value
        elif self.isDoubleHashing(self.mode):
            q = DOUBLE_HASH_Q
            temp = q - pos % q
            assert(q<N)
            for j in range(1, N):
                look = (pos + j*temp) % N
                if (self.cells[look].state == state.empty):
                    return None
                if (self.cells[look].state == state.in_use and self.cells[look].key == key):
                    if (value == None):
                        value = self.cells[look].value
                        return value
        return value
    
    def hashmap_contains(self, key):
        if (not self.hashmap_lookup(key) == None):
            return True
        return False
        
    def hashmap_print_set(self):
        for i in range(self.size):
            if self.cells[i].state == state.in_use:
                print("Cell %5d: %s => %d" % (i,  self.cells[i].key, self.cells[i].value))
            if (self.cells[i].state == state.empty):
                print("Cell %5d: empty" % i)
            if (self.cells[i].state == state.deleted):
                print("Cell %5d: deleted" % i)
        
    def hashmap_print_stats(self):
        print("Collision times: %d\n" % self.collision)
        print("Entry number: %d\n" % self.num_entries)
        print("Average collisions per access: %lf\n" % (self.collision/self.num_entries))
        
# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining
class cell:
    def __init__(self):
        pass
        
class state(Enum):
    empty = 0
    in_use = 1
    deleted = 2
        
# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING=0
    HASH_1_QUADRATIC_PROBING=1
    HASH_1_DOUBLE_HASHING=2
    HASH_1_SEPARATE_CHAINING=3
    HASH_2_LINEAR_PROBING=4
    HASH_2_QUADRATIC_PROBING=5
    HASH_2_DOUBLE_HASHING=6
    HASH_2_SEPARATE_CHAINING=7
