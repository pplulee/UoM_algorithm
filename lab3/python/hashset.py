from enum import Enum

import config


class hashset:
    def __init__(self,size=0):
        # create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size if size == 0 else size
        self.hash_table = [None] * self.hash_table_size
        self.insert_num = 0
        self.resize_count = 0
        self.occupancy_rate = 0.5
        self.insert_stat = []
        self.find_stat = []

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

    def doublehash(self, value):
        hash = self.gethash(value)
        hash2 = hash*len(value)+1
        return hash, hash2

    def gethash(self, value):
        sum = 0
        for char in value:
            sum += ord(char)**3
        if self.mode in [0, 1, 2, 3]:
            # modular division
            return (sum*len(value)) % self.hash_table_size
        elif self.mode in [4, 5, 6, 7]:
            # random linear and polynomial
            # use sum as key
            a = ord(value[0])**2
            b = ord(value[-1])**3
            return (a * sum + b) % self.hash_table_size

    def insert(self, value):
        # table occupation rate check
        if self.insert_num / self.hash_table_size > self.occupancy_rate:
            self.resize()
        if self.mode in [0, 4]:  # linear probing
            pos = self.gethash(value)
            # insert behind pos
            for i in range(pos, self.hash_table_size):
                if self.hash_table[i] is None:
                    self.hash_table[i] = value
                    self.insert_num += 1
                    self.insert_stat.append(i - pos + 1)
                    return True
                elif self.hash_table[i] == value:
                    self.insert_stat.append(i - pos + 1)
                    return True
                # back to start
            for i in range(0, pos):
                if self.hash_table[i] is None:
                    self.hash_table[i] = value
                    self.insert_num += 1
                    self.insert_stat.append(self.hash_table_size - pos + i + 1)
                    return True
                elif self.hash_table[i] == value:
                    self.insert_stat.append(self.hash_table_size - pos + i)
                    return True
        elif self.mode in [1, 5]:  # quadratic probing
            for i in range(self.hash_table_size):
                pos = (self.gethash(value) + i * i) % self.hash_table_size
                if self.hash_table[pos] is None:
                    self.hash_table[pos] = value
                    self.insert_num += 1
                    self.insert_stat.append(i + 1)
                    return True
                elif self.hash_table[pos] == value:
                    self.insert_stat.append(i)
                    return True
            # insert failed, need to resize
            self.resize()
            return self.insert(value)
        elif self.mode in [2, 6]:  # double hashing
            hash1, hash2 = self.doublehash(value)
            for i in range(self.hash_table_size):
                pos = (hash1 + i * hash2) % self.hash_table_size
                if self.hash_table[pos] is None:
                    self.hash_table[pos] = value
                    self.insert_num += 1
                    self.insert_stat.append(i + 1)
                    return True
                elif self.hash_table[pos] == value:
                    self.insert_stat.append(i)
                    return True
            self.resize()
            return self.insert(value)
        print("insert failed")
        return False

    def find(self, value):
        if self.mode in [0, 4]:  # linear probing
            pos = self.gethash(value)
            for i in range(pos, self.hash_table_size):
                if self.hash_table[i] == value:
                    self.find_stat.append(i - pos + 1)
                    return True
                elif self.hash_table[i] is None:
                    self.find_stat.append(i - pos + 1)
                    return False
            for i in range(0, pos):
                if self.hash_table[i] == value:
                    self.find_stat.append(self.hash_table_size - pos + i + 1)
                    return True
                elif self.hash_table[i] is None:
                    self.find_stat.append(i - pos + 1)
                    return False
            self.find_stat.append(self.hash_table_size)
            return False
        elif self.mode in [1, 5]:  # quadratic probing
            for i in range(self.hash_table_size):
                pos = (self.gethash(value) + i * i) % self.hash_table_size
                if self.hash_table[pos] == value:
                    self.find_stat.append(i + 1)
                    return True
                elif self.hash_table[pos] is None:
                    self.find_stat.append(i + 1)
                    return False
        elif self.mode in [2, 6]:  # double hashing
            hash1, hash2 = self.doublehash(value)
            for i in range(self.hash_table_size):
                pos = (hash1 + i * hash2) % self.hash_table_size
                if self.hash_table[pos] == value:
                    self.find_stat.append(i + 1)
                    return True
                elif self.hash_table[pos] is None:
                    self.find_stat.append(i + 1)
                    return False
        return False

    def print_set(self):
        for i in range(0, self.hash_table_size):
            if self.hash_table[i] is not None:
                print(f"{i + 1}: {self.hash_table[i]}")

    def resize(self):
        print("Resizing hash table")
        self.resize_count += 1
        self.insert_num = 0
        temp = self.hash_table
        self.hash_table_size = self.nextPrime(self.hash_table_size * 2)
        self.hash_table = [None] * self.hash_table_size
        for i in range(len(temp)):
            if temp[i] is not None:
                self.insert(temp[i])
        del temp

    def get_collision(self):
        collisions = 0
        for i in range(self.hash_table_size):
            if self.hash_table[i] is not None:
                if i!=self.gethash(self.hash_table[i]):
                    collisions += 1
        return collisions

    def get_max_insert(self):
        return max(self.insert_stat)

    def get_avg_insert(self):
        return sum(self.insert_stat) / len(self.insert_stat)

    def get_max_find(self):
        return max(self.find_stat)

    def get_avg_find(self):
        return sum(self.find_stat) / len(self.find_stat)

    def print_stats(self):
        print(f"Current mode: {self.mode}")
        elements = 0
        collisions = 0
        for i in range(self.hash_table_size):
            if self.hash_table[i] is not None:
                elements += 1
                if self.mode in [0,4]:
                    if self.gethash(self.hash_table[i]) != i:
                        collisions += 1
                elif self.mode in [1,2,5,6]:
                    if self.gethash(self.hash_table[i])%self.hash_table_size != i:
                        collisions += 1
        print(f"Hash table size: {self.hash_table_size}")
        print(f"Hash table contains {elements} elements")
        print(f"Hash table has {collisions} collisions")
        print(f"Hash table has been resized {self.resize_count} times")
        print(f"Hash table load factor: {elements / self.hash_table_size}")
        print(f"Insert operation number: {self.insert_num}")
        if len(self.insert_stat) > 0:
            print(f"Insert operation average: {sum(self.insert_stat) / len(self.insert_stat)}")
        print(f"Highest insert operation steps: {max(self.insert_stat)}")
        if len(self.find_stat) > 0:
            print(f"Average find operation cost: {sum(self.find_stat) / len(self.find_stat)}")
        print(f"Highest find operation steps: {max(self.find_stat)}")


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
