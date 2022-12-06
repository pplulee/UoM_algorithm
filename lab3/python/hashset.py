from enum import Enum

import config


class hashset:
    def __init__(self):
        # create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.hash_table = [None] * self.hash_table_size
        self.insert_num = 0
        self.occupancy_rate = 0.75

    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while i * i <= n:
            if n % i == 0:
                return False
            i = i + 1
        return True

    def nextPrime(self, n):
        while not self.isPrime(n):
            n = n + 1
        return n

    def gethash(self, value):
        sum = 0
        for char in value:
            sum += ord(char)
        if self.mode in [0,1,2,3]:
            # modular division
            return sum % self.hash_table_size
        elif self.mode in [4,5,6,7]:
            # random linear and polynomial
            # use sum as key
            a = self.nextPrime(ord(value[0]))
            b = self.nextPrime(ord(value[-1]))
            return (a * sum + b) % self.hash_table_size

    def insert(self, value):
        if self.mode in [0,4]:  # linear probing
            pos = self.gethash(value)
            # insert behind pos
            for i in range(pos, self.hash_table_size):
                if self.hash_table[i] is None:
                    self.hash_table[i] = value
                    self.insert_num += 1
                    return True
                elif self.hash_table[i] == value:
                    return True
                # back to start
            for i in range(0, pos):
                if self.hash_table[i] is None:
                    self.hash_table[i] = value
                    self.insert_num += 1
                    return True
                elif self.hash_table[i] == value:
                    return True
        elif self.mode in [1,5]:  # quadratic probing
            for i in range(self.hash_table_size):
                pos = (self.gethash(value) + i * i) % self.hash_table_size
                if self.hash_table[pos] is None:
                    self.hash_table[pos] = value
                    self.insert_num += 1
                    return True
                elif self.hash_table[pos] == value:
                    return True
            # insert failed, need to resize
            self.resize()
            return self.insert(value)
        # table occupation rate check
        self.resize()

    def find(self, value):
        if self.mode in [0,4]:  # linear probing
            pos = self.gethash(value)
            for i in range(pos, self.hash_table_size):
                if self.hash_table[i] == value:
                    return True
            for i in range(0, pos):
                if self.hash_table[i] == value:
                    return True
        elif self.mode in [1,5]: # quadratic probing
            for i in range(self.hash_table_size):
                pos = (self.gethash(value) + i * i) % self.hash_table_size
                if self.hash_table[pos] == value:
                    return True
                elif self.hash_table[pos] is None:
                    return False
        return False

    def print_set(self):
        for i in range(0, self.hash_table_size):
            if self.hash_table[i] is not None:
                print(f"{i + 1}: {self.hash_table[i]}")

    def resize(self):
        if self.insert_num / self.hash_table_size > self.occupancy_rate:
            print("Resizing hash table")
            self.insert_num = 0
            temp = self.hash_table
            self.hash_table_size = self.nextPrime(self.hash_table_size * 2)
            self.hash_table = [None] * self.hash_table_size
            for i in range(len(temp)):
                if temp[i] is not None:
                    self.insert(temp[i])

    def print_stats(self):
        elements = 0
        collisions = 0
        for i in range(self.hash_table_size):
            if self.hash_table[i] is not None:
                elements += 1
                if self.gethash(self.hash_table[i]) != i:
                    collisions += 1
        print(f"Hash table size: {self.hash_table_size}")
        print(f"Hash table contains {elements} elements")
        print(f"Hash table has {collisions} collisions")
        print(f"Hash table load factor: {elements / self.hash_table_size}")
        print(f"Insertion operation number: {self.insert_num}")

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
    HASH_1_LINEAR_PROBING = 0
    HASH_1_QUADRATIC_PROBING = 1
    HASH_1_DOUBLE_HASHING = 2
    HASH_1_SEPARATE_CHAINING = 3
    HASH_2_LINEAR_PROBING = 4
    HASH_2_QUADRATIC_PROBING = 5
    HASH_2_DOUBLE_HASHING = 6
    HASH_2_SEPARATE_CHAINING = 7
