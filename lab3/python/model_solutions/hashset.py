from enum import Enum
import config

class hashset:
    def __init__(self):
        # TODO: create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.cells = self.initialise_cell_array()
        
    def initialise_cell_array(self):
        self.num_entries = 0
        self.collision = 0
        cells = []

        for i in range(self.hash_table_size):
            if (not self.isSeparateChaining(self.mode)):
                new_cell = cell()
                new_cell.state = state.empty
            else:
                new_cell = cell_chain()
            cells.append(new_cell)
        return cells
        
                
    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while (i * i <= n):
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
        

    def hashFunc2(self, k, N):
        string_len = len(k)
        h = 0
        i = string_len - 1
        while i >= 0:
            h = h + ord(k[i]) 
            i = i - 1
            
        h = abs(h) % N
        return h
        
    # def size(self):
            # return self.num_entries
        
    # insertion
    
    def insertCell(self, k, pos):
        self.cells[pos].element = k
        self.cells[pos].state = state.in_use
        self.num_entries = self.num_entries + 1
        
    def rehash(self):
        N = self.hash_table_size
        newSize = self.nextPrime(2 * N)
        if (self.verbose > 2):
            print("Rehashing")
            print("Current Set")
            self.print_set()
        self.hash_table_size = newSize
        old_cells = self.cells.copy()
        
        self.cells = self.initialise_cell_array()
        for i in range(N):
            if (not self.isSeparateChaining(self.mode)):
               if (old_cells[i].state == state.in_use):
                 self.insert(old_cells[i].element)
            else:
               if (old_cells[i].value != None):
                   cell = old_cells[i]
                   self.insert(cell.value)
                   while (cell.link != None):
                       cell = cell.link
                       self.insert(cell.value)
        if (self.verbose > 2):
            print("New Set")
            self.print_set()
                
    def isLinearProbing(self, mode):
        return (mode == HashingModes.HASH_1_LINEAR_PROBING.value or mode == HashingModes.HASH_2_LINEAR_PROBING.value)
        
    def isQuadraticProbing(self, mode):
        return (mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or mode == HashingModes.HASH_2_QUADRATIC_PROBING.value)
        
    def isDoubleHashing(self, mode):
        return (mode == HashingModes.HASH_1_DOUBLE_HASHING.value or mode == HashingModes.HASH_2_DOUBLE_HASHING.value)

    def isSeparateChaining(self, mode):
        return (mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or mode == HashingModes.HASH_2_SEPARATE_CHAINING.value)
        

    def insert(self, value):
        if self.find(value): # detect duplicate
            return
            
        N = self.hash_table_size
        if (self.num_entries >= N/2): # check full table
            self.rehash()
            
        N = self.hash_table_size
        pos = self.hashFunc(value, N)
        
        # insert into empty cell
        if (not self.isSeparateChaining(self.mode)):
            if (self.cells[pos].state != state.in_use):
                self.insertCell(value, pos)
            else:
                if self.isLinearProbing(self.mode): # linear probing: A[(i + j)mod N]
                    for j in range(1, N):
                       look = (pos + j) % N
                       self.collision = self.collision + 1
                       if (self.cells[look].state != state.in_use):
                          self.insertCell(value, look)
                          break
                       if (self.cells[look].element == value):
                          break
                elif self.isQuadraticProbing(self.mode): # quadratic probing : A[(i + j^2)mod N]
                   for j in range (1, N):
                       look = (pos + j*j) % N
                       self.collision = self.collision + 1
                       if (self.cells[look].state != state.in_use):
                           self.insertCell(value, look)
                           break
                       if (self.cells[look].element == value):
                          break
                elif self.isDoubleHashing(self.mode): # double hash: A[(i+j*h'(k))mod N] 
                   temp = self.hashFunc2(value, N)
                
                   for j in range(1, N):
                      look = (pos + j * temp) % N
                      self.collision = self.collision + 1
                      if (self.cells[look].state != state.in_use):
                         self.insertCell(value, look)
                         break
                      if (self.cells[look].element == value):
                         break
        else:
            self.cells[pos].insert(value)
            self.num_entries += self.num_entries + 1
            
        
    def find(self, value):
        N = self.hash_table_size
        pos = self.hashFunc(value, N)

        if (not self.isSeparateChaining(self.mode)):
            if (self.cells[pos].state == state.in_use and self.cells[pos].element == value):
               return True
            
            elif self.isLinearProbing(self.mode):
               for j in range(1, N):
                  look = (pos + j) % N
                  if (self.cells[look].state == state.empty):
                     return False
                  if (self.cells[look].state == state.in_use and self.cells[look].element == value):
                     return True
            elif self.isQuadraticProbing(self.mode):
               for j in range(1, N):
                 look = (pos + j*j) % N
                 if (self.cells[look].state == state.empty):
                    return False
                 if (self.cells[look].state == state.in_use and self.cells[look].element == value):
                    return True
            elif self.isDoubleHashing(self.mode):
              temp = self.hashFunc2(value, N)
              for j in range(1, N):
                look = (pos + j*temp) % N
                if (self.cells[look].state == state.empty):
                    return False
                if (self.cells[look].state == state.in_use and self.cells[look].element == value):
                    return True
        else:
            return self.cells[pos].find(value)
            
        return False
        
    def print_set(self):
        for i in range(self.hash_table_size):
            if (not self.isSeparateChaining(self.mode)):
               if self.cells[i].state == state.in_use:
                  print("Cell %5d: %s" % (i,  self.cells[i].element))
               if (self.cells[i].state == state.empty):
                  print("Cell %5d: empty" % i)
               if (self.cells[i].state == state.deleted):
                  print("Cell %5d: deleted" % i)
            else:
                print("Cell %5d: %s"% (i, self.cells[i].print_chain()))
        
    def print_stats(self):
        print("Collision times: %d\n" % self.collision)
        print("Entry number: %d\n" % self.num_entries)
        print("Average collisions per access: %lf\n" % (self.collision/self.num_entries))
        
# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining
class cell:
    def __init__(self):
        pass

# Alternative data-structure for separate chaining
class cell_chain:
    def __init__(self, value=None):
        self.value = value
        self.link = None

    def insert(self, value):
        if (self.value == None):
            self.value = value
        elif (self.value == value):
            pass
        elif (self.link == None):
            self.link = cell_chain(value)
        else:
            self.collisions += 1
            self.link.insert(value)

    def find(self, value):
        if (self.value == value):
            return True
        if (self.link == None):
            return False
        return self.link.find(value)

    def print_chain(self):
        if (self.link == None):
            return self.value 
        else:
            return self.value + ", " + self.link.print_chain()
        
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
