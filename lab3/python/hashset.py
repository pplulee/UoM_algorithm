from enum import Enum

import config


class hashset:
    def __init__(self):
        # create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.hash_table = [None] * self.hash_table_size

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
        if self.mode == 0 or self.mode == 1:
            # modular division
            return sum % self.hash_table_size
        elif self.mode == 4:
            # random linear and polynomial
            # use sum as key
            a = self.nextPrime(ord(value[0]))
            b = self.nextPrime(ord(value[-1]))
            return (a * sum + b) % self.hash_table_size

    def insert(self, value):
        if self.mode == 0 or self.mode == 4:  # linear probing
            pos = self.gethash(value)
            if self.hash_table[pos] == value:
                return True
            for i in range(pos, self.hash_table_size):
                if self.hash_table[i] is None:
                    self.hash_table[i] = value
                    return True
            for i in range(0, pos):
                if self.hash_table[i] is None:
                    self.hash_table[i] = value
                    return True
        elif self.mode == 1:  # quadratic probing
            for i in range(self.hash_table_size):
                pos = (self.gethash(value) + i * i) % self.hash_table_size
                if self.hash_table[pos] is None:
                    self.hash_table[pos] = value
                    return True
                elif self.hash_table[pos] == value:
                    return True
        # table is full
        self.resize()
        return self.insert(value)

    def find(self, value):
        if self.mode == 0 or self.mode == 4:  # linear probing
            pos = self.gethash(value)
            for i in range(pos, self.hash_table_size):
                if self.hash_table[i] == value:
                    return True
            for i in range(0, pos):
                if self.hash_table[i] == value:
                    return True
        elif self.mode == 1:
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
        print("Hash table is full, resizing...")
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
        print(f"Hash table contains {elements} elements")
        print(f"Hash table has {collisions} collisions")


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
